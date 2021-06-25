import bcrypt
password = b"super secret password"
# Hash uma senha pela primeira vez, com um sal gerado aleatoriamente
hashed = bcrypt.hashpw(password, bcrypt.gensalt(8))
# Verifique se uma senha sem hash corresponde a uma que foi anteriormente
if bcrypt.checkpw(password, hashed):
    print("It Matches!")
else:
    print("It Does not Match :(")
