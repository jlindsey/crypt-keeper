Crypt Keeper
============

![](http://vignette2.wikia.nocookie.net/uncyclopedia/images/c/c4/CryptKeeper.gif/revision/latest?cb=20100602135927)

A very simple tool for managing encrypted secrets stored in Redis.

This tool is designed to be used as part of a SaltStack external pillar, but the CLI
component can be used on its own if desired.

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

Run these commands as a privileged user and make sure no other users have read or
write access to the files within your key directory. CryptKeeper will look in
`/etc/crypt-keeper` by default, but you can put your keys anywhere and run
`crypt-keeper` with the `--dir=DIRECTORY` option.

External Pillar
---------------

This tool was developed to function as an external pillar for SaltStack, and contains
a module to aid in this. A very simple external pillar module and config can be found
[in this Gist](https://gist.github.com/jlindsey/fd8ec324560f3cbb2e65).

When creating secrets using the `crypt-keeper` tool for use with Salt, you should
add an extra key to the entry called `__minions__`. This should be a comma-delimited
set of minion id globs that have access to this secret, in the same way you would
configure a normal pillar `top.sls` file.

For example, an AWS credential secret might look like this:

```json
{
  "__minions__": "app*,worker*",
  "aws_access_key_id": "XXX",
  "aws_secret_access_key": "XXX"
}
```

If the `__minions__` key is omitted, the secret will be available to all minions (as though
the secret had a `"__minions__": "*"` entry).

