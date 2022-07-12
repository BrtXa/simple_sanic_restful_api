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


@transaction_bp.route("/tx", methods={"GET"})
@doc.tag("Wallet")
@doc.summary("Create wallet")
@doc.consumes(doc.String(name="hash"), location="query")
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
    # demo_trans = db.db["test"].find_one()
    # demo_trans["_id"] = str(demo_trans["_id"])
    # return json(demo_trans)

