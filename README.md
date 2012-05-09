# Secret Service Chart Server
##### Version: 0.1.0
### Authors: Ryan McGowan, Boyan Alexandrov and Josh Spector

## Description

Secret Service Chat Server (SSCS) is the server-side application for our CSE 651
project.  The server is an endpoint for clients to store and access encrypted
messages.

This project uses [semantic versioning](http://http://semver.org/).

### Technologies Used:

* Python
    * Flask
* MongoDB

--------
## Setup

### Web Application (Python/Flask) Setup

This application is compatible with Heroku/cedar. See the Heroku website for
[instructions on how to deploy a Python - Flask app to
Heroku](http://devcenter.heroku.com/articles/python).

To get the app running locally you just need to run a few commands. (Most of
these are covered in the Heroku instructions referenced above).

1.  Install *pip* on your computer (if it isn't already installed). This may change
    depending on your distribution, so you might want to look this up on your
    own.

    Since Flask is not compatible with Python 3 you should make sure that your
    *pip* excutable is using Python 2.x not Python 3.x. On [Arch
    Linux](http://www.archlinux.org) this means you have to run 'pip-2.7' instead
    of 'pip'.

2.  Install *virtualenv*

        $ pip install virtualenv

    You might need to run the above command as sudo depending on your setup.

3.  Setup and initialize *virtualenv*.

        $ cd /path/to/this/project/
        $ virtualenv env
        $ source env/bin/activate

    If you are using bash you can replace the last command with: 

        $ . env/bin/activate

4.  Install Flask and other dependencies.

        $ pip install -r requirements.txt

5.  Before we can run the application we must make it aware of the database.
    Copy the `config-example.yml` file to `config.yml` with the following
    commands and edit it accordingly. *NOTE: Pay attention to what python
    database adapter you use. You might have better luck using different ones on
    your system*

        $ cp config-example.yml config.yml
        $ $EDITOR config.yml

    Installing on heroku requires that all of your files on the heroku server
    being controlled by git. That means you would have to version control your
    `config.yml` file. This can be a security issue.  Since this is the case you
    can also configure the application with environment variables.

6.  Once that's done you can now either use the application:

        $ python web.py
 
    Or if you have foreman installed (`gem install foreman`):

        $ foreman start web
