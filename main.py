import json
from json import JSONEncoder
import jwt
from pathlib import Path
from fireblocks_sdk import FireblocksSDK, TransferPeerPath, DestinationTransferPeerPath, VAULT_ACCOUNT, INTERNAL_WALLET, EXTERNAL_WALLET

# Fireblocks API
apiSecret = open('secret/fireblocks_secret.key', 'r').read()
apiKey = 'ce70c95f-6dc7-d25a-0994-53abd6d29419'
fireblocks = FireblocksSDK(apiSecret, apiKey)

# Validator Private Key
f1 = Path("secret/private.pem")
if f1.is_file(): validator_privateKey = f1.read_bytes()

# Function Declaration
def create_transaction(**kwargs):
    # Get Source Address
    source_address = get_source_address(kwargs["source"], kwargs["asset_id"])
    if source_address != "":
        kwargs["sourceAddress"] = source_address

    # Get Destination Address
    destination_address = get_destination_address(kwargs["destination"], kwargs["asset_id"])
    if destination_address != "":
        kwargs["destinationAddress"] = destination_address

    # Encrypt Transaction JSON and store in Note
    kwargs["note"] = encrypt_transaction(**kwargs)

    # Remove arguments not required by Fireblocks
    kwargs.pop("sourceAddress")
    kwargs.pop("destinationAddress")

    return fireblocks.create_transaction(**kwargs)


def get_source_address(source: TransferPeerPath, asset_id):
    if source.type == VAULT_ACCOUNT:
        address_list = fireblocks.get_deposit_addresses(source.id, asset_id)
        for a in address_list:
            if a['type'] == 'Permanent':
                return a['address']
    return ""


def get_destination_address(destination: DestinationTransferPeerPath, asset_id):
    if destination.type == VAULT_ACCOUNT:
        address_list = fireblocks.get_deposit_addresses(destination.id, asset_id)
        for a in address_list:
            if a['type'] == 'Permanent':
                return a['address']

    if destination.type == INTERNAL_WALLET:
        wallet_asset = fireblocks.get_internal_wallet_asset(destination.id, asset_id)
        return wallet_asset['address']

    if destination.type == EXTERNAL_WALLET:
        wallet_asset = fireblocks.get_external_wallet_asset(destination.id, asset_id)
        return wallet_asset['address']

    return ""


def encrypt_transaction(**kwargs):
    transactionJsonData = json.loads(json.dumps(kwargs, cls=TransactionEncoder))
    return jwt.encode(transactionJsonData, validator_privateKey, algorithm="RS256")


# subclass JSONEncoder
class TransactionEncoder(JSONEncoder):
        def default(self, o):
            return o.__dict__

# Main Program
source = TransferPeerPath(VAULT_ACCOUNT, "0")
#dest = DestinationTransferPeerPath(VAULT_ACCOUNT, "1")
#dest = DestinationTransferPeerPath(INTERNAL_WALLET, "da4072dd-5729-831a-1382-52b72ab5487c")
dest = DestinationTransferPeerPath(EXTERNAL_WALLET, "bce2a50c-d390-0edb-5f04-08f2aba7dc52")
create_transaction(asset_id='ETH_TEST', amount="0.001", source=source, destination=dest)