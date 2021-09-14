import hashlib

def hashPassword(password):
    encodedWord = password.encode()
    hashedPass = hashlib.md5(encodedWord)
    hashedPass = hashedPass.hexdigest()

    return hashedPass
