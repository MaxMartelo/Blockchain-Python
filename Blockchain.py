import functools 
import hashlib as hl

import json
import pickle


from utility.hash_util import hash_block
from utility.verification import Verification
from block import Block
from transaction import Transaction 


# Definition of the list blockchain and of the genesis block
mining_reward = 10
class Blockchain: 
    def __init__(self, hosting_node_id):
        """Constructor
        """
        #genesis block is the first block created for the blockchain
        genesis_block = Block(0, '', [], 100, 0)
        #initialized our blockchain list
        self.chain = [genesis_block]
        #Unhandled transactions
        self.__open_transactions = []
        self.load_data()
        self.hosting_node = hosting_node_id

    @property #creation of getter
    def chain(self):
        return self.__chain[:]

    @chain.setter #creation of a setter
    def chain(self, val):
        self.__chain = val

    def get_open_transactions(self):
        return self.__open_transactions[:]

# owner = 'Max' # In realty it is a pseudo like zorufdshfdhgnsdoiusjd
# participants = {'Max'} # At the beginning, I am the only participant


    def load_data(self):
        """read the file containing the data of the blockchain : here it is an instance method
        """
        # global blockchain #tells to the algo that the function behind are the global function and not something else 
        # global open_transactions

        try: #to handle exception with except
            with open('blockchain.txt', mode='r') as f: #.txt for json and .p for pickle, r for json and rb for pickle
                #using json : 
                file_content = f.readlines()
                blockchain = json.loads(file_content[0] [:-1]) #convert a string json format into a json, we use :-1 to not read the \n
                updated_blockchain = []
                for block in blockchain:
                    converted_tx = [Transaction(tx['sender'], tx['recipient'], tx['amount']) for tx in block['transactions']]
                    updated_block = Block(block['index'], block['previous_hash'], converted_tx, block['proof'], block['timestamp'])
                    #updtaed a block with out a class 
                    # updated_block = {
                    #     'previous_hash': block['previous_hash'],
                    #     'index': block['index'],
                    #     'proof': block['proof'],
                    #     'transactions': [OrderedDict(
                    #         [('sender', tx['sender']), ('recipient', tx['recipient']), ('amount', tx['amount'])]) for tx in block['transactions']]
                    #     }
                    updated_blockchain.append(updated_block)
                self.chain = updated_blockchain #to store the loade chain

                open_transactions = json.loads(file_content[1])
                updated_transactions =[]
                for tx in open_transactions:
                    updated_transaction = Transaction(tx['sender'], tx['recipient'], tx['amount'])
                    updated_transactions.append(updated_transaction)
                self.__open_transactions = updated_transactions #to store the loaded transactions

                #using pickle
                # file_content = pickle.loads(f.read())#use pickle.loads to load when using pickle
                # global blockchain #tells to the algo that the function behind are the global function and not something else 
                # global open_transactions
                # blockchain = file_content['chain']
                # open_transactions = file_content['ot']

        except (IOError, IndexError): #can have different type error like ValueError 
            #print('Handled exception')
            pass
        finally:
            print('Cleanup!')


    def save_data(self):
        """save_data function : opens a file blockchain.txt and write in it so that if we shut down the blockchain, we do not lose any information : here it is an instance method
        """
        try:
            with open('blockchain.txt', mode='w') as f: # .txt for json and .p for pickle, w for json and wb for pickle
                saveable_chain = [block.__dict__ for block in [Block(block_el.index, block_el.previous_hash, [tx.__dict__ for tx in block_el.transactions], block_el.proof, block_el.timestamp) for block_el in self.__chain]]
                #using json
                f.write(json.dumps(saveable_chain)) #convert my list(blockchain) into a str as a json format : it is different than doing str(blockchain)
                f.write('\n')
                saveable_tx = [tx.__dict__ for tx in self.__open_transactions]
                f.write(json.dumps(saveable_tx)) 

                #using pickle
                # save_data = {
                #     'chain': blockchain,
                #     'ot': open_transactions
                # }
                # f.write(pickle.dumps(save_data)) #use pickle to convert into binary data 
        except IOError:
            print('saving failed!')
        


    def proof_of_work(self):
        """maj of the proof number : here it is an instance method
        """
        last_block = self.__chain[-1]
        last_hash = hash_block(last_block)
        proof = 0
        #try different PoW numbers and return the first valid one
        while not Verification.valid_proof(self.__open_transactions, last_hash, proof):
            proof += 1
        return proof 



    def get_balance(self):
        """calculate and return the balance for a participant (take what the participant has send and what he has received and check the result) : : here it is an instance method

        Args:
            participant: The person from whom to caculate the balance 

        Returns:
            int: balance of the participant
        """
        participant = self.hosting_node
        #Fetch a list of all sent coin amounts for the given person 
        #This fetches sent amounts of transactions that were already included in block
        tx_sender = [[tx.amount for tx in block.transactions if tx.sender == participant] for block in self.__chain] #return amount send in the previous block

        #Fetch a list of all sent coin amounts for the given person 
        #This fetches sent amounts of open transactions (to avoid double spend)
        open_tx_sender = [tx.amount for tx in self.__open_transactions if tx.sender == participant] #return the amount send in the open_transaction list
        tx_sender.append(open_tx_sender)

        amount_sent = functools.reduce(lambda tx_sum, tx_amt: tx_sum + sum(tx_amt) if len(tx_amt) > 0 else tx_sum + 0, tx_sender, 0) #equivalent to lines behind
        # amount_sent = 0
        # for tx in tx_sender:
        #     if len(tx) > 0:
        #          amount_sent += tx[0]

        tx_recipient = [[tx.amount for tx in block.transactions if tx.recipient == participant] for block in self.__chain]

        amount_received = functools.reduce(lambda tx_sum, tx_amt: tx_sum + sum(tx_amt) if len(tx_amt) > 0 else tx_sum + 0, tx_recipient, 0) #reducing lines behind : sum(tx_amt) => to sum all the transactions made  
        # amount_received = 0
        # for tx in tx_recipient:
        #     if len(tx) > 0:
        #          amount_received += tx[0]

        #return the total balance
        return amount_received - amount_sent 


    def get_last_blockchain_value(self):
        """Returns the last value of the current blockchain."""
        if len(self.__chain) < 1 : # Case where the blockchain is empty
            return None
        return self.__chain[-1]


    def add_transaction(self, recipient, sender, amount = 1.0):
        """ Append a new value as well as the last blockchain value to the blockchain (Add a value to the list : the transaction ammount + the last transaction)

        Arguments:
            : Sender : The sender of the coins.
            : Recipient : The recipient of the coins
            : Amount : The amount of coins sent with the transaction(default = 1.0) """

        # transaction = {
        #     'sender': sender,
        #     'recipient' : recipient,
        #     'amount' : amount
        # }
        transaction = Transaction(sender, recipient, amount)
        if Verification.verify_transaction(transaction, self.get_balance):
            self.__open_transactions.append(transaction)
            self.save_data() #to save the block into a file
            return True
        return False


    def mine_block(self):
        """Create a new block and add open transactions to it."""
        last_block = self.__chain [-1] # Blockchain [-1] gives us the last element of the blockchain
        hashed_block = hash_block(last_block) # it is the same as our for loop behind
        proof = self.proof_of_work() #give us a number for a valid hash
        # for is used to convert last_block into  a hashed_block as a string so that we can read it
        """ for key in last_block:
            value = last_block[key]
            hashed_block += str(value) """
        # reward_transaction = { #to reward mining
        #     'sender' : 'MINING',
        #     'recipient':  owner,
        #     'amount' : mining_reward
        # }

        # we need to have an ordered dict of reward transaction otherwise it can change the hash of the PoW and lead to an error
        reward_transaction = Transaction('MINING', self.hosting_node, mining_reward)
        #here we can copy all the open transaction thaks to [:] 
        copied_transactions = self.__open_transactions[:] 
        copied_transactions.append(reward_transaction)


        # hashing algorithm
        block = Block(len(self.__chain), hashed_block, copied_transactions, proof)
        # block = {
        #     'previous_hash': hashed_block,
        #     'index': len(blockchain),
        #     'transactions': copied_transactions,
        #     'proof': proof
        #     }
        self.__chain.append(block)
        #reset my open transactions
        self.__open_transactions = []
        self.save_data()

        return True











