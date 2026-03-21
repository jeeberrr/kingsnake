# Kingsnake
Kingsnake is a simple ransomware written in python.

# THIS IS FOR EDUCATIONAL AND RESEARCH PURPOSES ONLY, I (JEEBERRR, THE AUTHOR) AM NOT RESPONSIBLE FOR ANY ILLEGAL USAGE OR DAMAGE, USE AT YOUR OWN RISK

## EVERYTHING HERE IS CONFIRMED TO WORK, EXCEPT FOR THE RANSOM FUNCTIONALITY WHICH WILL BE TESTED IN THE UPCOMING DAYS ON VIRTUAL MACHINES. THE ONLY OS THAT WILL REMAIN UNTESTED IS MACOS

Kingsnake is a proof of concept ransomware that includes a builder, server, and asymetric encryption keygen. It includes functionalities such as linking a discord webhook to it aswell.

## HOW IT WORKS (CLIENT SIDE):

On the client side, kingsnake is ran and then reaches out to the command and control server listed in the config.ini file made in the builder. It gets your public key from that server, and then generates a symmetrical encryption key using Fernet. It then recursively encrypts every file on the drive except for the specific ignored directories listed in the decryptor.py and payload.py files (for system preservation, this isnt a system bricking tool), along with their subdirectories. Afterwards, it creates a ransom note on the desktop, moves the decryptor.py file onto the desktop, moves the config.ini file to the local appdata folder (depending on the operating system) along with the public key encrypted symmetrical key, and then self destructs the entire directory the payload.py file is in.

After the decryptor is ran, it launches a ui that delivers another ransom note with customized instructions to send a specific ammount of money to a specific bitcoin address (all configured in builder.py), and a button to confirm payment. After clicking confirm payment, it send a request back to the command and control server with their bitcoin address they input along with the ammount of money they have to pay, and if the payment is confirmed it returns the symmetrical key decrypted and it then fully decrypts the drive.

## HOW IT WORKS (SERVER SIDE):

On the server side, keys are generated using keygen.py in the Server folder, and then the payload is built using the options given in builder.py in the Client folder. Afterwards, the server is run and waits for victims.

## USAGE (for help screen, more detailed usage info there):

First install requirements.txt

```pip install -r requirements.txt```

builder.py:

```python3 builder.py```

keygen.py:

```python3 keygen.py -h``` 

server.py:

```python3 server.py -h```
