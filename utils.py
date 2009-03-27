# -*- coding: utf-8 -*-
from os import urandom
from base64 import b64encode, b64decode
from Crypto.Cipher import ARC4

class Password():
    SALT_SIZE = 8
    SECRET_KEY = '91$15(#!k2iv#lqbr8&rn7of(%v3$#te8+levssi%7*e6d7tb9'

    @staticmethod
    def encrypt(plaintext):
        salt = urandom(Password.SALT_SIZE)
        arc4 = ARC4.new(salt + Password.SECRET_KEY)
        plaintext = "%3d%s%s" % (len(plaintext), plaintext, urandom(256-len(plaintext)))
        return "%s$%s" % (b64encode(salt), b64encode(arc4.encrypt(plaintext)))
 
    @staticmethod
    def decrypt(ciphertext):
        salt, ciphertext = map(b64decode, ciphertext.split('$'))
        arc4 = ARC4.new(salt + Password.SECRET_KEY)
        plaintext = arc4.decrypt(ciphertext)
        return plaintext[3:3+int(plaintext[:3].strip())]
 
p = Password()
plain = 'teste'
print 'plain: %s' % plain

enc = p.encrypt(plain)
print 'enc: %s ' % enc

dec = p.decrypt(enc)
print 'dec: %s' % dec
