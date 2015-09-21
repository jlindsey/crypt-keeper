import json
from keyczar import keyczar

__default_crypt_dir__ = "/etc/crypt-keeper"


class Crypter(object):
    def __init__(self, key_path=None):
        if key_path is None:
            key_path = __default_crypt_dir__
        self.crypt = keyczar.Crypter.Read(key_path)

    def encrypt(self, obj):
        return self.crypt.Encrypt(json.dumps(obj))

    def decrypt(self, s):
        return json.loads(self.crypt.Decrypt(s))
