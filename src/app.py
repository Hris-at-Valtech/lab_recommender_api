import os
import logging

from flask import Flask, jsonify, make_response, send_file, request, abort
from flask_caching import Cache
import snowflake.connector
from snowflake.connector import DictCursor

logging.basicConfig(level=logging.INFO)

app = Flask(__name__)

# use in-memory cache, defaulted to 3min
app.config['CACHE_TYPE'] = 'SimpleCache'
app.config['CACHE_DEFAULT_TIMEOUT'] = 180

cache = Cache(app)

# connect to Snowflake using internal SPCS token
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

# endpoint for querying the hybrid table
@app.route('/customer/<cust_id>')
@cache.memoize(timeout=180)
def get_customer(cust_id):
    sql_string = '''
        SELECT
            USER_ID,
            RECOMMENDATIONS
        FROM api.data.hybrid_product_recommendations
        WHERE USER_ID in ({cust_id});
    '''
    sql = sql_string.format(cust_id=cust_id)
    try:
        res = conn.cursor(DictCursor).execute(sql)
        return make_response(jsonify(res.fetchall()))
    except:
        abort(500, "Error reading from Snowflake. Check the QUERY_HISTORY for details.")

@app.route("/")
def default():
    return make_response(jsonify(result='Nothing to see here'))

# test HTML page
@app.route("/test")
def tester():
    return send_file("api_test.html")

@app.errorhandler(404)
def resource_not_found(e):
    return make_response(jsonify(error='Not found!'), 404)

if __name__ == '__main__':
    app.run(port=8001, host='0.0.0.0')
