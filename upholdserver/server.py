import argparse
import datetime
import json

import redis
import yaml

def list_subscribed(args):
    print "Subscribed Computers:"
    print "---------------------"
    for computer in sorted(args.redis.smembers("subscriptions")):
        print computer


def print_logs(args):
    print "Logged Tasks:"
    print "-------------"
    logged_json = args.redis.lpop("tasklog")
    while logged_json:
        logged = json.loads(logged_json)
        if "error" in logged:
            print logged["computer"], u"failed:"
        else:
            print logged["computer"], u"completed:"
        for key in sorted(logged["task"]):
            print u" ", key+u":", unicode(logged["task"][key])
        logged_json = args.redis.lpop("tasklog")


def push_task(r, task):
    task["time"] = datetime.datetime.utcnow().isoformat()
    task_json = json.dumps(task)
    for computer in sorted(r.smembers("subscriptions")):
        args.redis.rpush("tasks:"+computer, task_json)
        print "Pushed to", computer


def msi(args):
    print "Adding msi task: "
    print args.path
    print "----------------"

    push_task(args.redis, {"msi":args.path})


def putfile(args):
    print "Adding putfile task:"
    print args.file
    print args.into
    print "--------------------"
    
    push_task(args.redis, {"file":args.file, "into":args.into})


if __name__ == "__main__":
    with open("uphold.txt") as config_file:
        config = yaml.load(config_file)

    redis_config = config.get("redis", {"host":"localhost", "port":6379})
    
    r = redis.StrictRedis(
        host=redis_config.get("host", "localhost"),
        port=redis_config.get("port", 6379))

    parser = argparse.ArgumentParser(
        description="Publish to or maintain an Uphold installation")
    parser.set_defaults(redis=r)
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
    

    

    
    