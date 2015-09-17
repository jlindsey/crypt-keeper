import json
from keyczar import keyczar


class Crypter(object):
    def __init__(self, key_path):
        self.crypt = keyczar.Crypter.Read(key_path)

    def encrypt(self, obj):
        return self.crypt.Encrypt(json.dumps(obj))

    def decrypt(self, s):
        return json.loads(self.crypt.Decrypt(s))
