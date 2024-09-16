import os

import snowflake.connector
from snowflake.connector import DictCursor
from flask import Blueprint, request, abort, jsonify, make_response

# Make the Snowflake connection

def connect() -> snowflake.connector.SnowflakeConnection:
    if os.path.isfile("/snowflake/session/token"):
        creds = {
            'host': os.getenv('SNOWFLAKE_HOST'),
            'port': os.getenv('SNOWFLAKE_PORT'),
            'protocol': "https",
            'account': os.getenv('SNOWFLAKE_ACCOUNT'),
            'authenticator': "oauth",
            'token': open('/snowflake/session/token', 'r').read(),
            'warehouse': os.getenv('SNOWFLAKE_WAREHOUSE'),
            'database': os.getenv('SNOWFLAKE_DATABASE'),
            'schema': os.getenv('SNOWFLAKE_SCHEMA'),
            'client_session_keep_alive': True
        }
    else:
        creds = {
            'account': os.getenv('SNOWFLAKE_ACCOUNT'),
            'user': os.getenv('SNOWFLAKE_USER'),
            'password': os.getenv('SNOWFLAKE_PASSWORD'),
            'warehouse': os.getenv('SNOWFLAKE_WAREHOUSE'),
            'database': os.getenv('SNOWFLAKE_DATABASE'),
            'schema': os.getenv('SNOWFLAKE_SCHEMA'),
            'client_session_keep_alive': True
        }
    return snowflake.connector.connect(**creds)

conn = connect()

# Make the API endpoints
connector = Blueprint('connector', __name__)

@connector.route('/customer')
def get_customer():
    try:
        cust_id = str(request.args.get('id'))
    except:
        abort(400, "Invalid request")

    sql_string = '''
        SELECT
            C_CUSTOMER_SK,
            C_CUSTOMER_ID,
            C_CURRENT_CDEMO_SK,
            C_CURRENT_HDEMO_SK,
            C_CURRENT_ADDR_SK,
            C_FIRST_SHIPTO_DATE_SK,
            C_FIRST_SALES_DATE_SK,
            C_SALUTATION,
            C_FIRST_NAME,
            C_LAST_NAME,
            C_PREFERRED_CUST_FLAG,
            C_BIRTH_DAY,
            C_BIRTH_MONTH,
            C_BIRTH_YEAR,
            C_BIRTH_COUNTRY,
            C_LOGIN,
            C_EMAIL_ADDRESS,
            C_LAST_REVIEW_DATE
        FROM hybrid_db.data.hybrid_customer
        WHERE C_CUSTOMER_SK in ({cust_id});
    '''
    sql = sql_string.format(cust_id=cust_id)
    try:
        res = conn.cursor(DictCursor).execute(sql)
        return make_response(jsonify(res.fetchall()))
    except:
        abort(500, "Error reading from Snowflake. Check the logs for details, but also here was sql: " + sql)