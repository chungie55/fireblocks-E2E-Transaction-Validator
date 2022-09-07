# Fireblocks End to End Transaction Validator (Transaction Submission)
[![Python](https://www.python.org/static/community_logos/python-powered-h-50x65.png)](https://www.python.org/)

This is an example of a transaction set up which will accept transaction details 
as documented by Fireblocks SDK. The transaction details will be encrypted and signed by 
a customer generated private key and then stored in the "Note" field before calling the 
Fireblocks' Create Transaction endpoint.

Customer can then validate the transaction details by implementing a callback handler.

# Setup
1. Install Python v3.9+
2. Install required packages
```sh
$ pip install -r requirements.txt
```
3. Update ```/secret``` directory with correct key files



