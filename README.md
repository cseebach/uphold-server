uphold-server
=============

The master console for Uphold, a Windows administrative aid.

## Usage

Uphold is intended for deployment as two frozen Python executables. This one is a command-line program that adds commands to be run to the Redis server, which are then run by the client whenever the client checks Redis.

### Configuration

Uphold requires just information on where the Redis server is located. All other configuration is kept there.

That configuration information is currently supplied via a file in the working directory called `uphold.txt`. That file looks like this:

    redis:
        host: 192.168.1.35
        port: 6379

If this file is absent, Uphold will crash. `localhost` will be the default host and `6379` the default port if either or both or the `redis` block are missing.

### Commands

    uphold list

List all the computers by name that are subscribed. These are the computers that will receive added commands.

    uphold logs

Retrieve reports of all the tasks that have completed or failed since the last time that logs was run. Note that this currently removes these reports from Redis, so save them somewhere if you need them.

    uphold add msi {msi path}

Add a task that runs the msi file at {msi path}. {msi path} must be accessible from client computers. 

    uphold add putfile {file} {into}

Add a task that puts a copy of {file} into the directory at {into}. {file} must be accessible from client computers.

## History

I had a need for a simple way to install updates and do other administrative tasks across a network - and System Center was not an option.

So I wrote Uphold! It's currently quite simple, but it does a lot of what I need already: installing MSI files quietly and putting files on individual computers.

This is not really a "server" - Uphold installations get their commands from a Redis server on your network or elsewhere. But for historical reasons, I may sometimes refer to it as the server, when really the words "master console" are more appropriate.