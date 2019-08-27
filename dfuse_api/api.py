#!/usr/bin/python

import configparser
import os
import sys
import logging
import logging.config
import requests
import issue_token

# https://docs.dfuse.io

config = configparser.ConfigParser()
config.read(f"{os.path.dirname(__file__)}/../eos_service.ini")
app_key = config["Keys"]["dfuse_api_key"]
api_url = config["General"]["dfuse_api_mainnet_url"]

logging.config.fileConfig(f"{os.path.dirname(__file__)}/../logging.ini")
logger = logging.getLogger("main")

headers = {}


def generate_authorization_header():
    global headers
    if headers is None or len(headers) == 0:
        token = issue_token.get_token(app_key)["token"]
        headers = {"Authorization": f"Bearer {token}"}


generate_authorization_header()


def get_info():
    response = requests.post(
        f"{api_url}/v1/chain/get_info", data={}, headers=headers)
    logger.info(response.json())


def get_account(account_name):
    response = requests.post(f"{api_url}/v1/chain/get_account",
                             json={"account_name": account_name}, headers=headers, timeout=10)
    logger.info(response.json())
    return response.json()


def get_currency_balance(account_name, symbol = "EOS"):  
    """Gets token balance from standard chain requests!"""
    response = requests.post(f"{api_url}/v1/chain/get_currency_balance",
                             json={"code": "eosio.token", "account": account_name, "symbol":symbol}, headers=headers, timeout=10)
    logger.info(response.json())
    return response.json()

def get_account_balance(account_name):
    """ONLY EOS token restriction in this case!"""
    balance_string = get_currency_balance(account_name)[0].split(' ')
    symbol = balance_string[1]
    balance = balance_string[0]
    if (symbol == "EOS"):
        return balance
    else: 
        return 0

def search_received_transactions(account_name, limit=10):
    # print(headers)
    response = requests.get(f"{api_url}/v0/search/transactions", params={"sort": "desc", "limit": limit,
                                                                         "q": f"receiver:eosio.token action:transfer data.to:{account_name}"}, headers=headers, timeout=10)
    logger.info(f"From search/transactions RECEIVED {response.json()}")
    return response.json()


def search_sent_transactions(account_name, limit=10):
    # print(headers)
    response = requests.get(f"{api_url}/v0/search/transactions", params={"sort": "desc", "limit": limit,
                                                                         "q": f"receiver:eosio.token action:transfer data.from:{account_name}"}, headers=headers, timeout=10)
    logger.info(f"From search/transactions SENT {response.json()}")
    return response.json()

def get_transaction(transactionid):
    # print(headers)
    response = requests.get(f"{api_url}/v0/transactions/{transactionid}", headers=headers, timeout=10)
    logger.info(f"Get transaction response {response.json()}")
    return response.json()        



if __name__ == "__main__":
    get_account("mycoinsdepo1")
    get_account_balance("mycoinsdepo1")
