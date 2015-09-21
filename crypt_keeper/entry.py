from __future__ import print_function
import sys
import os
import tempfile
import subprocess
import json
import redis
from crypt_keeper.crypter import Crypter


__key_namespace__ = "crypt-keeper"


class Entry(object):
    key = None
    value = None

    def __init__(self, key=None, crypt_dir=None):
        self.redis = redis.Redis(host="localhost", port="6379", db=0)
        self.key = "%s:%s" % (__key_namespace__, key)
        self.crypter = Crypter(crypt_dir)
        self._fetch()

    def _fetch(self):
        val = self.redis.get(self.key)
        if val is not None:
            self.value = self.crypter.decrypt(val)

    def _save(self):
        print("Saving to `%s'" % self.key)
        return self.redis.set(self.key, self.crypter.encrypt(self.value))

    @staticmethod
    def keys():
        r = redis.Redis(host="localhost", port="6379", db=0)
        return r.keys("%s:*" % __key_namespace__)

    @staticmethod
    def list_keys():
        keys = Entry.keys()
        if len(keys()) == 0:
            print("No keys found", file=sys.stderr)
            return 1
        else:
            print("\n".join([key.replace("%s:" % __key_namespace__, "") for key in keys]))
        return 0

    def edit(self):
        temp = tempfile.NamedTemporaryFile(suffix=".json", delete=False)

        with temp.file as f:
            val = self.value if self.value is not None else {}
            f.write(json.dumps(val, indent=2, separators=(",", ": ")))

        try:
            subprocess.call([os.environ["EDITOR"], temp.name])
        except subprocess.CalledProcessError as e:
            print("Unable to open your EDITOR: ", e, file=sys.stderr)
            return 1

        with open(temp.name, "r") as f:
            try:
                self.value = json.loads(f.read())
            except ValueError as e:
                print("Unable to parse JSON from file: ", e, file=sys.stderr)
                return 1

        self._save()
        return 0

    def delete(self):
        return self.redis.delete(self.key)

    def view(self):
        if self.value is None:
            print("Key not found", file=sys.stderr)
            return 1
        else:
            print(self.value)
            return 0
