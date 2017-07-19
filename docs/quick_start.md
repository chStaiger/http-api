
# Quick start (FIXME: update to 0.5.2)

This is a reference page to quick start the HTTP API project.


## first steps

If you want to run in production the very first step should be to modify the configuration file with the relative path: 
`projects/eudat/project_configuration.yaml`


## deploy

A minimum set of operations to start developing within this repository.

Note that installations with the python package manager (`pip`) may require administration permissions. You may try to avoid this with the option `--user`.

```bash

###############
# begin working from the latest release
git clone https://github.com/EUDAT-B2STAGE/http-api.git
cd http-api

###############
# OPTIONAL: use a virtual environment 
# (this 'best practice' could avoid packages version conflicts)
(sudo) pip3 install virtualenv
virtualenv b2stage
source b2stage/bin/activate

###############
# complete first start

# install and use the rapydo controller
(sudo) pip3 install --upgrade -r projects/eudat/requirements.txt
# init and run containers in background
rapydo init
rapydo start && sleep 15 && echo "booted"
# init all datas (e.g. authorization database) 
rapydo shell backend --user developer --command 'restapi tests --initialize'
```

### DEVELOPMENT

Follow this paragraph only if you plan to develop new features on the HTTP API.

```bash
# activate the restful http-api server 
rapydo shell backend --user developer
$ restapi launch

# now you may access a client from another shell and test the server
rapydo shell restclient --user developer
```

The client shell will give you instructions on how to test the server

In case you want to log with the only existing admin user:

- username: user@nomail.org
- password: test


### PRODUCTION

Follow this paragraph only if you plan to deploy the HTTP API server in production.

1. Before going into production you should kill all resources (if any) from development mode, which was used to initialize the container data volumes:

```bash
# erase all containers currently running
rapydo remove
# Note: this will not delete the persistent data inside docker volumes
```

2. Usually in production you have a domain name associated to your host IP (e.g. `b2stage.cineca.it` to 240.bla.bla.bla).
You can just use 'localhost' if this is not the case.

```bash
DOMAIN='b2stage.cineca.it'
# launch production mode
rapydo --host $DOMAIN --mode production start
```

3. Now may access your IP or your domain and the HTTP API endpoints are online, protected by a proxy server. You can test this with:

```bash
open $DOMAIN/api/status
```

4. The current proxy certificate is self signed and is 'not secure' for all applications.
This is why we need to produce one with the free `letsencrypt` service.

Note: this step is possible only if you have a real domain associated to your host IP.


```bash
# produce certificate with letsencrypt
rapydo --host $DOMAIN --mode production ssl-certificate
```

If you check again the server should now be correctly certificated.

Last thing missing is giving the b2handle library real credentials to resolve PIDs. You can do so by copying such files into the dedicated directory:

```bash
cp PATH/TO/YOUR/CREDENTIALS/FILES/* data/b2handle/
```

At this point the service should be completely functional.

In case at some point you want to stop or remove containers you need to use the right 'mode' or thing would not work as expected:

```bash
rapydo --mode production remove
# Note, the default option mimics 'rapydo --mode debug remove'
```


## other operations

More helpers in debugging/developing the project

### launch interfaces

To explore data and query parameters there are few other services as options:

```bash
SERVER=localhost  # or your IP / Domain
PORT=8080

# access a swagger web ui
rapydo interfaces swagger
# access the webpage:
open http://$SERVER/swagger-ui/?url=http://$SERVER:$PORT/api/specs

# SQL admin web ui
rapydo interfaces sqlalchemy
# access the webpage:
open http://$SERVER:81/adminer
```


### destroy all

If you need to clean everything you have in docker from this project

```bash
rapydo clean --rm-volumes  # very DANGEROUS!
```


### squash branch

A better practice before pull requesting is to squash commits into a single one. Here's a guide on how to do so with git cli:

```bash
MYEXISTINGBRANCH='v0.1.0'
BASEBRANCH='master'

# start from the base branch (usually it's master)
git checkout $BASEBRANCH
# create a new branch for squashing
git checkout -b ${MYEXISTINGBRANCH}-squashed
# squash the differences between now and the feature branch
git merge --squash $MYEXISTINGBRANCH
# commit message will contain all commit messages so far
git commit
# you may/should change the content, at least top title and description
```

### hack the certificates volume

This hack is necessary if you want to raw copy a CA certificate if your VM DN was produced with an internal certification authority.

```bash
path=`docker inspect $(docker volume ls -q | grep sharedcerts) | jq -r ".[0].Mountpoint"`
sudo cp /PATH/TO/YOUR/CA/FILES/CA-CODE.* $path/simple_ca

```