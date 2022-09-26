"""Provides verification helper methodes."""

from utility.hash_util import hash_string_256, hash_block

class Verification:
    # It's not accessing anything from the class so great use case for static method
    @staticmethod
    def valid_proof(transactions, last_hash, proof): 
        """generate a new hash and check if it fulfill our difficulty criteria 

        Args:
            transactions : transactions in our block
            last_hash : the last hash
            proof : a random number (proof) we are testing 
        """
        #Create a string with all the hash inputs
        guess = (str([tx.to_ordered_dict() for tx in transactions]) + str(last_hash) + str(proof)).encode() #use encode to encode to UTF 
        guess_hash = hash_string_256(guess) #calculating the hash
        #print(guess_hash)
        return guess_hash[0:2] == '00' #our condition for a valid hash : it can be different


    # here it is a class method and not a static because it is accessing to valid proof
    @classmethod
    def verify_chain(cls, blockchain):
        """ Verify the current blockchain and return True if it's valid, False otherwise."""
        for (index, block) in enumerate(blockchain): # enumerate gives us a Tuple of informations
            if index == 0:
                continue
            if block.previous_hash != hash_block(blockchain[index - 1]):
                return False
            if not cls.valid_proof(block.transactions[:-1], block.previous_hash, block.proof): #[:-1] to exclude the reward transaction or it will not work
                print("Proof of work is invalid")
                return False

        return True


    @staticmethod
    def verify_transaction(transaction, get_balance):
        """Verify a transaction by checking whether the sender has sufficient credit 

        Args:
            transaction : The transaction that should be verified
            get_balance : =the balance of the sender 

        """
        sender_balance = get_balance()
        return sender_balance >= transaction.amount # = Does the sender have enough money to do the transaction ?


    @classmethod
    def verify_transactions(cls, open_transactions, get_balance):
        """verify all open transactions."""
        return all([cls.verify_transaction(tx, get_balance) for tx in open_transactions])


   