
# Documentation to handle services

Available services:
- sqlalchemy
- irods
- neo4j
- mongodb
- celery
- elasticsearch

## MongoDB

The admin ui is based on [mongo express](https://www.npmjs.com/package/mongo-express) and its [docker image](https://hub.docker.com/r/_/mongo-express/).

To launch it (only in debug mode):
```bash
$ ./do DEBUG sql_admin
```

Then access http://localhost:8081
