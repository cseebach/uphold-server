uphold-server
=============

The master console for Uphold, a Windows administrative aid.

## Usage

Uphold is intended for deployment as two frozen Python executables. This one is a command-line program that adds commands to be run to the Redis server, which are then run by the client whenever the client checks Redis.

### Commands

    uphold list

List all the computers that are subscribed by name. These are the computers that will receive added commands.

    uphold logs

Retrieve reports of all the tasks that have completed or failed since the last time that logs was run. Note that this currently removes these reports from Redis, so save them somewhere if you need them.

    uphold add msi {msi path}

Add a task that runs the msi file at {msi path}. 

    uphold add putfile {file} {into}

Add a task that puts a copy of {file} into the directory at {into}.

## History

I had a need for a simple way to install updates and do other administrative tasks across a network - and System Center was not an option.

So I wrote Uphold! It's currently quite simple, but it does a lot of what I need already: installing MSI files quietly and putting files on individual computers.

This is not really a "server" - Uphold installations get their commands from a Redis server on your network or elsewhere. But for historical reasons, I may sometimes refer to it as the server, when really the words "master console" are more appropriate.