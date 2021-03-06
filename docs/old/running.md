
# Deploying your services

### The main script

There is a very comprehensive `do` script to manage the docker stack.

You may find it inside the repository root directory.

To see what you can do with it, ask for help:

```bash
$ ./do help
# ############################################ #
        EUDAT HTTP API development
# ############################################ #

Available commands:

init:       Startup your repository code, containers and volumes
graceful:   Try to bring up only missing containers
restart:    (Re)Launch the Docker stack
irestart:   Restart the main iRODS iCAT service instance
addiuser:   Add a new certificated user to irods

check:  Check the stack status
stop:   Freeze your containers stack
remove: Remove all containers
clean:  Remove containers and volumes (BE CAREFUL!)

irods_shell:    Open a shell inside the iRODS iCAT server container
server_shell:   Open a shell inside the Flask server container
client_shell:   Open a shell to test API endpoints
api_test:   Run tests with nose (+ coverage)

push:   Push code to github
update: Pull updated code and images```

### Run the final services

Following the previous section everything should be properly configured.
You can launch postgresql & irods - from now on - with this simple comand:

```bash
$ ./do graceful

(re)Boot Docker stack
Starting eudatapi_certshare_1
eudatapi_graphdb_1 is up-to-date
eudatapi_sql_1 is up-to-date
eudatapi_icat_1 is up-to-date
eudatapi_rest_1 is up-to-date
Stack processes:
---------------------------
eudatapi_certshare_1   echo Data volume on              Exit 0
eudatapi_graphdb_1     /docker-entrypoint.sh neo4j      Up       7473/tcp, 0.0.0.0:9090->7474/tcp
eudatapi_icat_1        /bootup                          Up       1247/tcp
eudatapi_rest_1        ./boot                           Up       0.0.0.0:8080->5000/tcp
eudatapi_sql_1         /docker-entrypoint.sh postgres   Up       5432/tcp
Updating certificates in /etc/ssl/certs...```

### Verify services and ports

Checking processes with compose must say that both containers are up:
```bash
./do check

Stack status:
--------------------
eudatapi_certshare_1   echo Data volume on              Exit 0
eudatapi_graphdb_1     /docker-entrypoint.sh neo4j      Up       7473/tcp, 0.0.0.0:9090->7474/tcp
eudatapi_icat_1        /bootup                          Up       1247/tcp
eudatapi_rest_1        ./boot                           Up       0.0.0.0:8080->5000/tcp
eudatapi_sql_1         /docker-entrypoint.sh postgres   Up       5432/tcp```

### Opening a shell inside the iRODS iCat server

```bash
./do irods_shell

irods@rodserver:~$ ils
/tempZone/home/rods:
```

### Restarting the irods server

```bash
$ ./do irestart

[sudo] password for irods:
Stopping iRODS server...
Starting iRODS server...
Confirming catalog_schema_version... Success
Validating [/home/irods/.irods/irods_environment.json]... Success
Validating [/etc/irods/server_config.json]... Success
Validating [/etc/irods/hosts_config.json]... Success
Validating [/etc/irods/host_access_control_config.json]... Success
Validating [/etc/irods/database_config.json]... Success
```

### Accessing your irods server from outside the Docker network

1) Remove comments from this lines inside `docker-compose.yml`:

```yaml
    # ports:
    #     - 1247:1247
```

2) Access the irods host as `rodserver`

e.g. you have your host ip as 130.1.2.10, add this line to `/etc/hosts`:
```
130.1.2.10 rodserver
```

3) Be sure you open port 1247 on every firewall your host works behind

### Connecting to irods with another container as a client

You may launch a new container using the same docker image.
This will allow you to access the latest icommands to test
a connection from outside.

```bash

# See the irods container name:
$ docker ps | grep _icat_ | awk '{print $NF}'
eudatapi_icat_1

# Link it
$ docker run -it --link eudatapi_icat_1:rodserver eudatb2safe/irods bash
# then from inside the new container...

# See what is the current passw
echo $IRODS_PASS

# Use the defaults values
$ iinit
Enter the host name (DNS) of the server to connect to: rodserver
Enter the port number: 1247
Enter your irods user name: rods
Enter your irods zone: tempZone
Enter your current iRODS password: # the one above
```

You can now go to [next chapter](client.md).

*A security note*:

The main password is saved as an environment variable for development purpose.

You may (and should) change it inside the `docker-compose.yml` file.

Note that security for containers is best reached by avoiding connections/launching containers from outside your net/LAN.
