Crypt Keeper
============

A very simple tool for managing encrypted secrets stored in Redis.

Installation
------------

```
$ git clone https://github.com/jlindsey/crypt-keeper.git
$ cd crypt-keeper
$ python setup.py install
$ crypt-keeper -h
```

### Keyczar

Crypt Keeper uses Google's [keyczar](https://github.com/google/keyczar) library for
encryption and decryption. You must initialize a key directory yourself first before
using Crypt Keeper. The `keyczart` tool should already be installed as a dependency
if you've installed Crypt Keeper first.

```
$ keyczart create --location=/etc/crypt-keeper --purpose=crypt
$ keyczart addkey --location=/etc/crypt-keeper --status=primary --size=256
$ chmod 0600 /etc/crypt-keeper/*
```

Run these commands as a privileged use and make sure no other users have read or
write access to the files within your key directory. CryptKeeper will look in
`/etc/crypt-keeper` by default, but you can put your keys anywhere and run
`crypt-keeper` with the `--dir=DIRECTORY` option.

