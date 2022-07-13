from sanic_openapi.openapi2 import doc


class DecodedInput:
    from_address = doc.String()
    to_address = doc.String()
    asset_address = doc.String()
    value = doc.Integer()


class RelatedAddressBalance:
    DecodedInput.asset_address = doc.Float()


class RelatedAddress:
    address = doc.String()
    balance = doc.Object(RelatedAddressBalance)


class Transaction:
    _id = doc.String()
    type = doc.String()
    hash = doc.String()
    nonce = doc.Integer()
    transaction_index = doc.Integer()
    from_address = doc.String()
    to_address = doc.String()
    value = doc.String()
    gas = doc.String()
    gas_price = doc.String()
    input = doc.String()
    block_timestamp = doc.Integer()
    block_number = doc.Integer()
    block_hash = doc.String()
    receipt_cumulative_gas_used = doc.String()
    receipt_gas_used = doc.String()
    receipt_contract_address = doc.String()
    receipt_root = doc.String()
    receipt_status = doc.Integer()
    item_timestamp = doc.String()
    decoded_input = doc.Object(DecodedInput)
    # related_addresses = doc.List(
    #     items=[doc.Object(RelatedAddress), doc.Object(RelatedAddress)]
    # )
    transaction_type = doc.String()

