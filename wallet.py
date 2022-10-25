from Crypto.PublicKey import RSA
from Crypto.Signature import PKCS1_v1_5 # special algo to generate signatures
from Crypto.Hash import SHA256 

import Crypto.Random 
import binascii


class Wallet: 
    def __init__(self):
        """The constructor sets the privateand public key to k ow so that we have the coice to create or load our keys 
        """
        self.private_key = None
        self.public_key = None
    
    def create_keys(self):
        private_key, public_key = self.generate_keys()
        self.private_key = private_key
        self.public_key = public_key
        
    def save_keys(self):
        if self.public_key != None and self.private_key != None:
            try:
                with open('wallet.txt', mode='w') as f: #to write the key in a file 
                    f.write(self.public_key)
                    f.write('\n')
                    f.write(self.private_key)
            except(IOError, IndexError):
                print('Sabing wallet failed...')

    def load_keys(self):
        try:
            with open('wallet.txt', mode='r') as f: #to read the keys from the file 
                keys = f.readlines()
                pubic_key = keys[0][:-1] #we had [:-1] to not have the '\n' at the end of our public key 
                private_key = keys[1]
                self.public_key = pubic_key
                self.private_key = private_key
        except(IOError, IndexError):
            print('Loading wallet failed...')

    def generate_keys(self):
        """Generate a Private key of 1024 bits.
        Thanks to this private key, we can generate a public key
        returns a string representation of our key
        """
        private_key = RSA.generate(1024, Crypto.Random.new().read) 
        public_key = private_key.publickey()
        return (binascii.hexlify(private_key.exportKey(format='DER')).decode('ascii'), binascii.hexlify(public_key.exportKey(format='DER')).decode('ascii')) 

    def sign_transaction(self, sender, recipient, amount):
        """ Create the signature using the private key and the algo PKCS1 + creating a hash taking as parameter the seder, recipient and amount

        Returns:
            string: return the signature 
        """
        signer = PKCS1_v1_5.new(RSA.importKey(binascii.unhexlify(self.private_key))) #import the private key and transform it into bin and pass it to PK.. algo
        h = SHA256.new((str(sender) + str(recipient) + str(amount)).encode('utf8')) # creates an hash 
        signature = signer.sign(h) # create a signature which is made from signer and the hash
        return binascii.hexlify(signature).decode('ascii') # returns the signature as a string 

    @staticmethod
    def verify_transaction(transaction):
        """check if a signature is valid
        No need to check if the sender if the one mining 
        """
        public_key = RSA.importKey(binascii.unhexlify(transaction.sender))
        verifier = PKCS1_v1_5.new(public_key)
        h = SHA256.new((str(transaction.sender) + str(transaction.recipient) + str(transaction.amount)).encode('utf8')) 
        return verifier.verify(h, binascii.unhexlify(transaction.signature))