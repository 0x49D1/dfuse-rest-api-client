#!/usr/bin/python


import requests
import redis
import json
import time

redis_db = redis.StrictRedis(host="localhost", port=6379, db=0)


def get_token(api_key):
    global redis_db
    token = redis_db.get(f'get_token{api_key}')
    if token is None or token == '':
        print("Getting token from auth.dfuse.io")
        response = requests.post(
            "https://auth.dfuse.io/v1/auth/issue", json={"api_key": f"{api_key}"})
        token = response.text
        redis_db.set(f'get_token{api_key}', token, ex=(json.loads(token)["expires_at"] - int(time.time()) - 60*60))  # get the real expiration and "minus one more hour"

    return json.loads(token)


# if __name__ == "__main__":
#     token = get_token("server_test_key_here")
#     print(token)
