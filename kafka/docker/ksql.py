import requests

KSQLDB_SERVER_URL = 'http://localhost:8088'

def ksqldb_query(query):
    headers = {
        'Content-Type': 'application/vnd.ksql.v1+json; charset=utf-8'
    }
    payload = {
        'ksql': query,
        'streamsProperties': {}
    }
    response = requests.post(f'{KSQLDB_SERVER_URL}/ksql', headers=headers, json=payload)
    return response.json()

# Example query
query = "SELECT * FROM orders EMIT CHANGES;"
response = ksqldb_query(query)
print(response)
