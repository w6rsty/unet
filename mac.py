import hashlib


def encrypt_mac_address(mac_address):
    sha256 = hashlib.sha256()
    sha256.update(mac_address.encode())
    encrypted_mac = sha256.hexdigest()
    encrypted_mac = encrypted_mac.replace("a", "w")
    encrypted_mac = encrypted_mac.replace("b", "l")
    encrypted_mac = encrypted_mac.replace("c", "a")
    encrypted_mac = encrypted_mac.replace("d", "o")
    encrypted_mac = encrypted_mac.replace("e", "y")
    encrypted_mac = encrypted_mac.replace("f", "u")
    encrypted_mac = encrypted_mac.replace("g", "n")
    encrypted_mac = encrypted_mac.replace("h", "s")
    encrypted_mac = encrypted_mac.replace("i", "0417")
    encrypted_mac = encrypted_mac.replace("j", "0524")
    encrypted_mac = encrypted_mac.replace("k", "b")
    encrypted_mac = encrypted_mac.replace("l", "f")
    encrypted_mac = encrypted_mac.replace("m", "e")
    encrypted_mac = encrypted_mac.replace("n", "c")
    encrypted_mac = encrypted_mac.replace("w", "accde")
    encrypted_mac = encrypted_mac.replace("l", "bxcty")
    encrypted_mac = encrypted_mac.replace("1", "sdlkajhgfjkhsdfj")
    encrypted_mac = encrypted_mac.replace("2", "1l23e12qv")
    encrypted_mac = encrypted_mac.replace("3", "fjduslahf214451asdfslaij")
    return encrypted_mac
print(encrypt_mac_address("5CD121TQ05"))