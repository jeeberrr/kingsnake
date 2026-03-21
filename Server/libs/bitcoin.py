import requests

#sorry but i didnt know how to do this shit so this is ai. i didnt feel like reading all the docs for it plus its nothing super sensitive its just an api
def get_transaction(sender: str, recipient: str) -> int | None:
    tx_res = requests.get(f"https://mempool.space/api/address/{sender}/txs")
    tx_res.raise_for_status()
    txs = tx_res.json()

    match = None
    for tx in txs:
        sender_is_input = any(
            inp.get("prevout", {}).get("scriptpubkey_address") == sender
            for inp in tx["vin"]
        )
        recipient_is_output = any(
            out.get("scriptpubkey_address") == recipient
            for out in tx["vout"]
        )
        if sender_is_input and recipient_is_output:
            match = tx
            break

    if not match:
        return None

    received_sats = sum(
        out["value"]
        for out in match["vout"]
        if out.get("scriptpubkey_address") == recipient
    )
    btc_amount = received_sats / 1e8

    price_res = requests.get(
        "https://api.coingecko.com/api/v3/simple/price",
        params={"ids": "bitcoin", "vs_currencies": "usd"}
    )
    price_res.raise_for_status()
    btc_price_usd = price_res.json()["bitcoin"]["usd"]

    return int(btc_amount * btc_price_usd)