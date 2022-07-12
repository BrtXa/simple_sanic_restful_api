from sanic import Blueprint
from sanic_openapi.openapi2 import doc
from bson import ObjectId
from databases.db_config import DBConfig
from databases.pymongo import MongoDB
from sanic.response import json
from constants.db_constants import MongoCollection

# Database.
db = MongoDB(DBConfig.MongoDB_URI, DBConfig.MongoDB_DB_NAME)

transaction_bp = Blueprint("transaction_blueprint", url_prefix="")


@transaction_bp.get("/tx")
@doc.tag("Transaction")
@doc.consumes(doc.String(name="hash"), location="query")
@doc.response(200, {"message": str}, description="OK")
@doc.response(400, {"message": str}, description="Bad Request")
@doc.response(401, {"message": str}, description="Unauthorized")
@doc.response(404, {"message": str}, description="Not Found")
async def create_tx(request):
    hash = request.args.get("hash")
    print("Console out: ", hash)
    transaction = db.read_data(MongoCollection.transactions, {"hash": hash})

    if not transaction:
        return json({"error": "Cannot find transaction"}, status=404)

    return json(transaction)

