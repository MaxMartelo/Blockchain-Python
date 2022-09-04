from hash_util import hash_string_256, hash_block

class Verification:
    def valid_proof(self, transactions, last_hash, proof): 
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

    def verify_chain(self, blockchain):
        """ Verify the current blockchain and return True if it's valid, False otherwise."""
        for (index, block) in enumerate(blockchain): # enumerate gives us a Tuple of informations
            if index == 0:
                continue
            if block.previous_hash != hash_block(blockchain[index - 1]):
                return False
            if not self.valid_proof(block.transactions[:-1], block.previous_hash, block.proof): #[:-1] to exclude the reward transaction or it will not work
                print("Proof of work is invalid")
                return False

        return True

    def verify_transaction(self, transaction, get_balance):
        """Verify a transaction by checking whether the sender has sufficient credit 

        Args:
            transaction : The transaction that should be verified
            get_balance : =the balance of the sender 

        """
        sender_balance = get_balance()
        return sender_balance >= transaction.amount # = Does the sender have enough money to do the transaction ?

    def verify_transactions(self, open_transactions, get_balance):
        """verify all open transactions."""
        return all([self.verify_transaction(tx, get_balance) for tx in open_transactions])


   