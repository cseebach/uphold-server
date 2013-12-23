import sqlite3

__version__ = "1.1"

import argparse
import datetime
import json

import redis
import yaml

from upholdserver import database


def list_subscribed(args):
    print "Subscribed Computers:"
    print "---------------------"
    for computer in sorted(args.redis.smembers("subscriptions")):
        print computer


def print_logs(args):
    print "Logged Runs:"
    print "-------------"

    logged_json = args.redis.lpop("tasklog")
    while logged_json:
        print ""
        logged = json.loads(logged_json)

        for key in sorted(logged):
            if key != "task":
                print key + u":", unicode(logged[key])

        if "task" in logged:
            for key in sorted(logged["task"]):
                print u" ", key + u":", unicode(logged["task"][key])

        database.add_log_entry(args.db, logged)

        logged_json = args.redis.lpop("tasklog")


def push_task(r, task):
    task["pushed"] = datetime.datetime.utcnow().isoformat()
    task_json = json.dumps(task)
    for computer in sorted(r.smembers("subscriptions")):
        r.rpush("tasks:" + computer, task_json)
        print "Pushed to", computer


def msi(args):
    print "Adding msi task: "
    print args.path
    print "----------------"

    push_task(args.redis, {"msi": args.path})


def putfile(args):
    print "Adding putfile task:"
    print args.file
    print args.into
    print "--------------------"

    push_task(args.redis, {"file": args.file, "into": args.into})


def main():
    db = sqlite3.connect("logs.db")
    database.setup(db)

    try:
        with open("uphold.txt") as config_file:
            config = yaml.load(config_file)
    except IOError:
        print "No uphold.txt file: exiting."
        return
    except yaml.YAMLError:
        print "uphold.txt not valid YAML: exiting."
        return

    r = redis.StrictRedis.from_url(config.get("redis", "redis://localhost:6379/"))

    parser = argparse.ArgumentParser(
        description="Publish to or maintain an Uphold installation")
    parser.set_defaults(redis=r, db=db)
    parser.add_argument('-v', action='version', version='uphold v' + __version__)
    subparsers = parser.add_subparsers()

    parser_list = subparsers.add_parser(
        "list", help="list subscribed computers")
    parser_list.set_defaults(func=list_subscribed)

    parser_logs = subparsers.add_parser("logs", help="display new logs")
    parser_logs.set_defaults(func=print_logs)

    parser_add = subparsers.add_parser("add",
                                       help="subcommands for adding tasks")
    add_subparsers = parser_add.add_subparsers()

    parser_add_msi = add_subparsers.add_parser("msi", help="add an msi task")
    parser_add_msi.add_argument("path")
    parser_add_msi.set_defaults(func=msi)

    parser_add_putfile = add_subparsers.add_parser("putfile",
                                                   help="add a putfile task")
    parser_add_putfile.add_argument("file")
    parser_add_putfile.add_argument("into")
    parser_add_putfile.set_defaults(func=putfile)

    args = parser.parse_args()

    args.func(args)
    

    

    
    
