import functools 
import hashlib as hl

import json
import pickle

from hash_util import hash_string_256, hash_block
from block import Block
from transaction import Transaction 


# Definition of the list blockchain and of the genesis block
mining_reward = 10
blockchain = [] #initialized blockchain in our load_data fn 
open_transactions = []
owner = 'Max' # In realty it is a pseudo like zorufdshfdhgnsdoiusjd
participants = {'Max'} # At the beginning, I am the only participant

def load_data():
    """read the file containing the data of the blockchain
    """
    global blockchain #tells to the algo that the function behind are the global function and not something else 
    global open_transactions
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
            blockchain = updated_blockchain

            open_transactions = json.loads(file_content[1])
            updated_transactions =[]
            for tx in open_transactions:
                updated_transaction = Transaction(tx['sender'], tx['recipient'], tx['amount'])
                updated_transactions.append(updated_transaction)
            open_transactions = updated_transactions

            #using pickle
            # file_content = pickle.loads(f.read())#use pickle.loads to load when using pickle
            # global blockchain #tells to the algo that the function behind are the global function and not something else 
            # global open_transactions
            # blockchain = file_content['chain']
            # open_transactions = file_content['ot']

    except (IOError, IndexError): #can have different type error like ValueError 
        #genesis block is the first block created by the blockchain
        genesis_block = Block(0, '', [], 100, 0)
        #create the genesis block without a class
        # genesis_block = {
        #         'previous_hash': '',
        #         'index': 0,
        #         'transactions': [],
        #         'proof': 100
        #         }

        blockchain = [genesis_block]
        open_transactions = []


load_data()


def save_data():
    """save_data function : opens a file blockchain.txt and write in it so that if we shut down the blockchain, we do not lose any information
    """
    try:
        with open('blockchain.txt', mode='w') as f: # .txt for json and .p for pickle, w for json and wb for pickle
            saveable_chain = [block.__dict__ for block in [Block(block_el.index, block_el.previous_hash, [tx.__dict__ for tx in block_el.transactions], block_el.proof, block_el.timestamp) for block_el in blockchain]]
            #using json
            f.write(json.dumps(saveable_chain)) #convert my list(blockchain) into a str as a json format : it is different than doing str(blockchain)
            f.write('\n')
            saveable_tx = [tx.__dict__ for tx in open_transactions]
            f.write(json.dumps(saveable_tx)) 

            #using pickle
            # save_data = {
            #     'chain': blockchain,
            #     'ot': open_transactions
            # }
            # f.write(pickle.dumps(save_data)) #use pickle to convert into binary data 
    except IOError:
        print('saving failed!')
        


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


def proof_of_work():
    """maj of the proof number
    """
    last_block = blockchain[-1]
    last_hash = hash_block(last_block)
    proof = 0
    #try different PoW numbers and return the first valid one
    while not valid_proof(open_transactions, last_hash, proof):
        proof += 1
    return proof 



def get_balance(participant):
    """get the balance of a participant
    take what the participant has send and what he has received and check the result

    Args:
        participant (_type_): The person from whom to caculate the balance 

    Returns:
        int: balance of the participant
    """
    #Fetch a list of all sent coin amounts for the given person 
    #This fetches sent amounts of transactions that were already included in block
    tx_sender = [[tx.amount for tx in block.transactions if tx.sender == participant] for block in blockchain] #return amount send in the previous block

    #Fetch a list of all sent coin amounts for the given person 
    #This fetches sent amounts of open transactions (to avoid double spend)
    open_tx_sender = [tx.amount for tx in open_transactions if tx.sender == participant] #return the amount send in the open_transaction list
    tx_sender.append(open_tx_sender)

    amount_sent = functools.reduce(lambda tx_sum, tx_amt: tx_sum + sum(tx_amt) if len(tx_amt) > 0 else tx_sum + 0, tx_sender, 0) #equivalent to lines behind
    # amount_sent = 0
    # for tx in tx_sender:
    #     if len(tx) > 0:
    #          amount_sent += tx[0]

    tx_recipient = [[tx.amount for tx in block.transactions if tx.recipient == participant] for block in blockchain]

    amount_received = functools.reduce(lambda tx_sum, tx_amt: tx_sum + sum(tx_amt) if len(tx_amt) > 0 else tx_sum + 0, tx_recipient, 0) #reducing lines behind : sum(tx_amt) => to sum all the transactions made  
    # amount_received = 0
    # for tx in tx_recipient:
    #     if len(tx) > 0:
    #          amount_received += tx[0]

    #return the total balance
    return amount_received - amount_sent 


# Function that initialized the first value at -1
def get_last_blockchain_value():
    """Returns the last value of the current blockchain."""
    if len(blockchain) < 1 : # Case where the blockchain is empty
        return None
    return blockchain[-1]


def verify_transaction(transaction):
    sender_balance = get_balance(transaction.sender)
    return sender_balance >= transaction.amount # = Does the sender have enough money to do the transaction ?


# Add a value to the list : the transaction ammount + the last transaction
def add_transaction(recipient, sender = owner, amount = 1.0):
    """ Append a new value as well as the last blockchain value to the blockchain

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
  
    if verify_transaction(transaction):
        open_transactions.append(transaction)
        save_data() #to save the block into a file
        return True
    return False


def mine_block():
    """Create a new block and add open transactions to it."""
    last_block = blockchain [-1] # Blockchain [-1] gives us the last element of the blockchain
    hashed_block = hash_block(last_block) # it is the same as our for loop behind
    proof = proof_of_work() #give us a number for a valid hash
    # for is used to convert last_block into  a hashed_block as a string so that we can read it
    """ for key in last_block:
        value = last_block[key]
        hashed_block += str(value) """
    # reward_transaction = { #to reward mining
    #     'sender' : 'MINING',
    #     'recipient':  owner,
    #     'amount' : mining_reward
    # }
    reward_transaction = Transaction('MINING', owner, mining_reward) #we need to have an ordered dict of reward transaction otherwise it can change the hash of the PoW and lead to an error
    copied_transactions = open_transactions[:] #here we can copy all the open transaction thaks to [:]
    copied_transactions.append(reward_transaction)


    # hashing algorithm
    block = Block(len(blockchain), hashed_block, copied_transactions, proof)
    # block = {
    #     'previous_hash': hashed_block,
    #     'index': len(blockchain),
    #     'transactions': copied_transactions,
    #     'proof': proof
    #     }
    blockchain.append(block)
    return True


# Ask to the user a digit (transaction amount)
def get_transaction_value():
    """Returns the input of the user (a new transaction amount) as a float."""
    # Get the user input, transforme it to a float and store it in user_input
    tx_recipient = input('Enter the recipient of the transaction: ')
    tx_amount = float(input('Your transaction amount please: '))
    return (tx_recipient, tx_amount)


def get_user_choice():
    """Prompts the user for its choice and return it."""
    user_input = input('Your choice: ')
    return user_input


def print_blockchain():
    """Output all blocks of the blockchain"""
    for block in blockchain:
        print('Outputting Block ')
        #print(block)
    else:
        print('-' * 20)


def verify_chain():
    """ Verify the current blockchain and return True if it's valid, False otherwise."""
    for (index, block) in enumerate(blockchain): # enumerate gives us a Tuple of informations
            if index == 0:
                continue
            if block.previous_hash != hash_block(blockchain[index - 1]):
                return False
            if not valid_proof(block.transactions[:-1], block.previous_hash, block.proof): #[:-1] to exclude the reward transaction or it will not work
                print("Proof of work is invalid")
                return False

    return True


def verify_transactions():
    """verify all open transactions."""
    return all([verify_transaction(tx) for tx in open_transactions])


waiting_for_input = True
while waiting_for_input:
    print('Please choose: ')
    print('1: Add a new transaction value ')
    print('2: Mine a new block ')
    print('3: Output the blockchain blocks ')
    print('4: Output participants ')
    print('5: Check transaction validity ')
    # print('h: Manipulate the chain')
    print('q: Quit')
    user_choice = get_user_choice()
    if user_choice == '1':
        tx_data = get_transaction_value()
        recipient, amount = tx_data
        # Add the transaction amount to the blockchain
        if add_transaction(recipient, amount=amount): #amount = amount to skip the sender para
            print('Added transaction')
        else :
            print('Transaction failed')
        print(open_transactions)
    elif user_choice == '2' :
        if mine_block():
            open_transactions = []
            save_data() #to save the block into a file
    elif user_choice == '3' :
        print_blockchain()
    elif user_choice == '4' :
        print(participants)
    elif user_choice == '5' :
        if verify_transactions():
            print("All transactions are valid")
        else :
            print("There are invalid transactions")
    # elif user_choice == 'h':
    #     # Make sure that you don't try to "hack" the blockchain if it's empty
    #     if len(blockchain) >= 1:
    #         blockchain[0] = {
    #             'previous_hash': '',
    #             'index': 0,
    #             'transactions': [{'sender': 'Chris', 'recipient': 'Max', 'amount': 100.0}]
    #         }
    elif user_choice == 'q':
        # This will lead to the loop exist because it's running condition
        waiting_for_input = False
    else:
        print("Input was invalid, please pick a value from the list!")
    if  not verify_chain():
        print("Invald Blockchain")
        print_blockchain()
        break
    print('Balance of {}: {:6.2f}'.format('Max', get_balance('Max')))# format the amount to 6 digits and 2 after point
else:
    print('User left!')
