# Create a Data API for Snowflake Data using Python and Flask
Technologies used: [Snowflake](https://snowflake.com/), [Python](https://www.python.org/), 
[Flask](https://palletsprojects.com/p/flask/), [Docker](https://www.docker.com/)

This project demonstrates how to build a custom REST API, powered by Snowflake, to perform point-lookups in real-time (under ~200ms). 
It uses a simple Python Flask API service running in Snowflake Container Services, as well as a Snowflake Hybrid Table.

## Requirements:
* Snowflake account
* Snowflake user with
  * SELECT access to the `SNOWFLAKE_SAMPLES.TPCH_SF10.ORDERS` table
  * USAGE access on a warehouse

## Getting Started
The main guide to this code is featured as a Snowflake Quickstart, found here:

This QuickStart is best run by forking this repository, and then running in GitHub codespaces.

### Running
To start the server, run the following command updated with your Snowflake Account, User, Password, and Warehouse:
```
docker run -it -d -e SNOWFLAKE_ACCOUNT='<YOUR_SNOWFLAKE_ACCOUNT>' -e SNOWFLAKE_USER='<YOUR_SNOWFLAKE_USER>' -e SNOWFLAKE_PASSWORD='<YOUR_SNOWFLAKE_PASSWORD>' -e SNOWFLAKE_WAREHOUSE='<YOUR_SNOWFLAKE_WAREHOUSE>' -e SNOWFLAKE_DATABASE='SNOWFLAKE_SAMPLE_DATA' -e SNOWFLAKE_SCHEMA='TPCH_SF10' -p 8001:8001 api
```

### Testing
You can test this API using curl or other command-line tools. You can also use a tool such as Postman.

Additionally, the API serves a testing page you can open in a web browser at `https://<INGRESS_URL>/test`.

Finally, to optionally test performance, a jMeter test plan `snow_papi.jmx` is included, along with the `cust_ids.csv`. This will allow you to test 10,000 requests to the API in between 150-200 QPS.

