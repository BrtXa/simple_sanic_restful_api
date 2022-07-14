from sanic import Blueprint
from sanic_openapi.openapi2 import doc
from databases.db_config import DBConfig
from databases.pymongo import MongoDB
from sanic.response import json
from models.transaction_model import Transaction
from constants.db_constants import MongoTransaction


# Database.
db = MongoDB(DBConfig.MongoDB_URI, DBConfig.MongoDB_DB_NAME)

transaction_bp = Blueprint("transaction_blueprint", url_prefix="")


# Retrieve transaction details.
@transaction_bp.get("/tx")
@doc.tag("Transaction")
@doc.consumes(doc.String(name="hash"), location="query")
@doc.response(200, {"message": str}, description="OK")
@doc.response(400, {"message": str}, description="Bad Request")
@doc.response(401, {"message": str}, description="Unauthorized")
@doc.response(404, {"message": str}, description="Not Found")
async def get_tx(request):
    hash = request.args.get("hash")
    print("Console out: ", hash)
    transaction = db.read_data(DBConfig.MongoDB_COL_TX, {"hash": hash})

    if not transaction:
        return json({"error": "Cannot find transaction"}, status=404)

    return json(transaction)


# Create new transaction.
@transaction_bp.post("/create-tx")
@doc.tag("Create transaction")
@doc.consumes(Transaction, location="body")
@doc.response(200, {"message": str}, description="OK")
@doc.response(400, {"message": str}, description="Bad Request")
@doc.response(401, {"message": str}, description="Unauthorized")
@doc.response(404, {"message": str}, description="Not Found")
async def create_tx(request):
    # Use the json variable to get the body of input.
    data = request.json

    # Retrieve data from request and create a dictionary with the same structure as
    # the document in databse.
    transaction = {
        MongoTransaction.id: data["id"],
        MongoTransaction.type: data["type"],
        MongoTransaction.hash: data["hash"],
        MongoTransaction.nonce: data["nonce"],
        MongoTransaction.transaction_index: data["transaction_index"],
        MongoTransaction.from_address: data["from_address"],
        MongoTransaction.to_address: data["to_address"],
        MongoTransaction.value: data["value"],
        MongoTransaction.gas: data["gas"],
        MongoTransaction.gas_price: data["gas_price"],
        MongoTransaction.input: data["input"],
        MongoTransaction.block_timestamp: data["block_timestamp"],
        MongoTransaction.block_number: data["block_number"],
        MongoTransaction.block_hash: data["block_hash"],
        MongoTransaction.receipt_cumulative_gas_used: data[
            "receipt_cumulative_gas_used"
        ],
        MongoTransaction.receipt_gas_used: data["receipt_gas_used"],
        MongoTransaction.receipt_contract_address: data["receipt_contract_address"],
        MongoTransaction.receipt_root: data["receipt_root"],
        MongoTransaction.receipt_status: data["receipt_status"],
        MongoTransaction.item_timestamp: data["item_timestamp"],
        MongoTransaction.decoded_input: {
            MongoTransaction.decoded_input_from_address: data["decoded_input"][
                "from_address"
            ],
            MongoTransaction.decoded_input_to_address: data["decoded_input"][
                "to_address"
            ],
            MongoTransaction.decoded_input_asset_address: data["decoded_input"][
                "asset_address"
            ],
            MongoTransaction.decoded_input_value: data["decoded_input"]["value"],
        },
        MongoTransaction.related_addresses: [
            {
                MongoTransaction.related_address_address: data["related_addresses_0"][
                    "address"
                ],
                MongoTransaction.related_address_balance: {
                    data["to_address"]: data["related_addresses_0"]["balance"],
                },
            },
            {
                MongoTransaction.related_address_address: data["related_addresses_1"][
                    "address"
                ],
                MongoTransaction.related_address_balance: {
                    data["to_address"]: data["related_addresses_1"]["balance"],
                },
            },
        ],
        MongoTransaction.transaction_type: data["transaction_type"],
    }
    db.create_data(DBConfig.MongoDB_COL_TX, transaction)
    return json(transaction)
