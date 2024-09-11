import json
import random
import time
import base64

import stellar_sdk
from stellar_sdk import Keypair,Server, TransactionBuilder, Network, Signer, Asset, xdr
import requests


secret_key='SDW5NLCZJEXYK3RNXVZLAPZDMKQNYRVPKZUOFUYBNH4SYNSCJWECSISD'
acc=Keypair.from_secret(secret_key)
print(acc.public_key)



# Set up the Stellar server
server = Server("https://horizon.stellar.org")

# Define the account to monitor
account_id = acc.public_key

# Function to check if a transaction is suspicious
def is_suspicious(transaction):
    # Define criteria for suspicious transactions
    # For example, transactions above a certain amount or to certain addresses
    suspicious_amount = 1000  # Consider transactions above 1000 XLM as suspicious
    suspicious_destinations = ["GABC...", "GDEF..."]  # Add any known suspicious addresses

    for operation in transaction['operations']:
        if operation['type'] == 'payment':
            if float(operation['amount']) > suspicious_amount:
                return True
            if operation['to'] in suspicious_destinations:
                return True
    return False

# Fetch and analyze transactions
def analyze_transactions():
    suspicious_txs = []
    transactions = server.transactions().for_account(account_id).order(desc=True).limit(200).call()['_embedded']['records']

    for tx in transactions:
        if tx['source_account'] == account_id:  # Only outgoing transactions
            if is_suspicious(tx):
                suspicious_txs.append({
                    'id': tx['id'],
                    'created_at': tx['created_at'],
                    'memo': tx.get('memo', 'No memo'),
                    'operations': tx['operations']
                })

    return suspicious_txs

# Run the analysis
suspicious_transactions = analyze_transactions()

# Print the results
print(f"Found {len(suspicious_transactions)} suspicious outward transactions:")
for tx in suspicious_transactions:
    print(f"Transaction ID: {tx['id']}")
    print(f"Created at: {tx['created_at']}")
    print(f"Memo: {tx['memo']}")
    print("Operations:")
    for op in tx['operations']:
        print(f"  Type: {op['type']}")
        if op['type'] == 'payment':
            print(f"  Amount: {op['amount']} {op['asset_type']}")
            print(f"  Destination: {op['to']}")
    print("---")
