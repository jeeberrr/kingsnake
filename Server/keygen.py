from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization, hashes
import sys, getpass, os

def keygen(password):
    private = rsa.generate_private_key(public_exponent=65537, key_size=2048)
    pub = private.public_key()
    
    if not os.path.exists("keys"):
        os.makedirs("keys")

    if password != "":
        with open("keys/private.key", "wb") as f:
            f.write(private.private_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PrivateFormat.PKCS8,
                encryption_algorithm=serialization.BestAvailableEncryption(password)
            ))
    else:
        with open("keys/private.key", "wb") as f:
            f.write(private.private_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PrivateFormat.PKCS8,
                encryption_algorithm=serialization.NoEncryption()
            ))

    with open("keys/public.key", "wb") as f:
        f.write(pub.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        ))

if __name__ == "__main__":
    arg = sys.argv[1] if len(sys.argv) > 1 else ""

    if arg == "-h" or arg == "--help":
        print("\nUSAGE: python3 keygen.py [args]\n\nARGS:\n\n" \
                "-np --nopassword : disables password prompting.\n" \
                "-p --password [password] : manually enter password.")
    
    elif arg == "-np" or arg == "--nopassword":
        keygen("")
    elif arg == "-p" or arg == "--password":
        pass_val = sys.argv[2] if len(sys.argv) > 2 else ""
        keygen(pass_val.encode("utf-8"))
    elif arg == "":
        while True:
            password = getpass.getpass("Enter password: ")
            confpasswd = getpass.getpass("Confirm password: ")
            if password != confpasswd:
                print("Passwords do not match. Try again.\n")
                continue
            break
        keygen(password.encode("utf-8"))
    else:
        print("Invalid argument, use -h or --help to see help page.")
