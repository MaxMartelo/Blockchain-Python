import functools 
import hashlib as hl
from collections import OrderedDict
import json
import pickle

from hash_util import hash_string_256, hash_block


# Definition of the list blockchain and of the genesis block
mining_reward = 10

#genesis block is the first block created by the blockchain
genesis_block = {
        'previous_hash': '',
        'index': 0,
        'transactions': [],
        'proof': 100
        }
blockchain = [genesis_block]
open_transactions = []
owner = 'Max' # In realty it is a pseudo like zorufdshfdhgnsdoiusjd
participants = {'Max'} # At the beginning, I am the only participant

def load_data():
    """read the file containing the data of the blockchain
    """
    with open('blockchain.txt', mode='r') as f: #.txt for json and .p for pickle, r for json and rb for pickle
        #using json : 
        file_content = f.readlines()
        global blockchain #tells to the algo that the function behind are the global function and not something else 
        global open_transactions
        blockchain = json.loads(file_content[0] [:-1]) #convert a string json format into a json, we use :-1 to not read the \n
        updated_blockchain = []
        for block in blockchain:
            updated_block = {
                'previous_hash': block['previous_hash'],
                'index': block['index'],
                'proof': block['proof'],
                'transactions': [OrderedDict(
                    [('sender', tx['sender']), ('recipient', tx['recipient']), ('amount', tx['amount'])]) for tx in block['transactions']]
            }
            updated_blockchain.append(updated_block)
        blockchain = updated_blockchain

        open_transactions = json.loads(file_content[1])
        updated_transactions =[]
        for tx in open_transactions:
            updated_transaction = OrderedDict(
                    [('sender', tx['sender']), ('recipient', tx['recipient']), ('amount', tx['amount'])])
            updated_transactions.append(updated_transaction)
        open_transactions = updated_transactions

        #using pickle
        # file_content = pickle.loads(f.read())#use pickle.loads to load when using pickle
        # global blockchain #tells to the algo that the function behind are the global function and not something else 
        # global open_transactions
        # blockchain = file_content['chain']
        # open_transactions = file_content['ot']


load_data()


def save_data():
    """save_data function : opens a file blockchain.txt and write in it so that if we shut down the blockchain, we do not lose any information
    """
    with open('blockchain.txt', mode='w') as f: # .txt for json and .p for pickle, w for json and wb for pickle
        #using json
        f.write(json.dumps(blockchain)) #convert my list(blockchain) into a str as a json format : it is different than doing str(blockchain)
        f.write('\n')
        f.write(json.dumps(open_transactions)) 

        #using pickle
        # save_data = {
        #     'chain': blockchain,
        #     'ot': open_transactions
        # }
        # f.write(pickle.dumps(save_data)) #use pickle to convert into binary data 
        


def valid_proof(transactions, last_hash, proof): 
    """generate a new hash and check if it fulfill our diffivulty criteria 

    Args:
        transactions : transactions in our block
        last_hash : the last hash
        proof : a random number
    """
    guess = (str(transactions) + str(last_hash) + str(proof)).encode() #use encode to encode to UTF 
    guess_hash = hash_string_256(guess) #calculating the hash
    #print(guess_hash)
    return guess_hash[0:2] == '00' #our condition for a valid hash : it can be different


def proof_of_work():
    """maj of the proof number
    """
    last_block = blockchain[-1]
    last_hash = hash_block(last_block)
    proof = 0
    while not valid_proof(open_transactions, last_hash, proof):
        proof += 1
    return proof 



def get_balance(participant):
    """get the balance of a participant
    take what the participant has send and what he has received and check the result

    Args:
        participant (_type_): a participant

    Returns:
        int: balance of the participant
    """
    tx_sender = [[tx['amount'] for tx in block['transactions'] if tx['sender'] == participant] for block in blockchain] #return amount send in the previous block
    open_tx_sender = [tx['amount'] for tx in open_transactions if tx['sender'] == participant] #return the amount send in the open_transaction list
    tx_sender.append(open_tx_sender)

    amount_sent = functools.reduce(lambda tx_sum, tx_amt: tx_sum + sum(tx_amt) if len(tx_amt) > 0 else tx_sum + 0, tx_sender, 0) #equivalent to lines behind
    # amount_sent = 0
    # for tx in tx_sender:
    #     if len(tx) > 0:
    #          amount_sent += tx[0]

    tx_recipient = [[tx['amount'] for tx in block['transactions'] if tx['recipient'] == participant] for block in blockchain]

    amount_received = functools.reduce(lambda tx_sum, tx_amt: tx_sum + sum(tx_amt) if len(tx_amt) > 0 else tx_sum + 0, tx_recipient, 0) #reducing lines behind : sum(tx_amt) => to sum all the transactions made  
    # amount_received = 0
    # for tx in tx_recipient:
    #     if len(tx) > 0:
    #          amount_received += tx[0]
    return amount_received - amount_sent 


"""# Function that initialized the first value at -1
def get_last_blockchain_value():
    if len(blockchain) < 1 : # Case where the blockchain is empty
        return None
    return blockchain[-1]"""


def verify_transaction(transaction):
    sender_balance = get_balance(transaction['sender'])
    return sender_balance >= transaction['amount'] # = Does the sender have enough money to do the transaction ?


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
    transaction = OrderedDict([('sender', sender), ('recipient', recipient), ('amount', amount)]) #we need to have an ordered dict of transaction otherwise it can change the hash of the PoW and lead to an error

    if verify_transaction(transaction):
        open_transactions.append(transaction)
        participants.add(sender) #with a set if we add a name which already exists, nothing happend
        participants.add(recipient)
        save_data() #to save the block into a file
        return True
    return False


def mine_block():
    # Blockchain [-1] gives us the last element of the blockchain
    last_block = blockchain [-1]
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
    reward_transaction = OrderedDict([('sender', 'MINING'), ('recipient', owner), ('amount', mining_reward)]) #we need to have an ordered dict of reward transaction otherwise it can change the hash of the PoW and lead to an error
    copied_transactions = open_transactions[:] #here we can copy all the open transaction thaks to [:]
    copied_transactions.append(reward_transaction)


    # hashing algorithm
    block = {
        'previous_hash': hashed_block,
        'index': len(blockchain),
        'transactions': copied_transactions,
        'proof': proof
        }
    blockchain.append(block)
    return True


def verify_chain():
    #verify the current blockchain and return True if it's valid, False otherwise
    for (index, block) in enumerate(blockchain): # enumerate gives us a Tuple of informations
            if index == 0:
                continue
            if block['previous_hash'] != hash_block(blockchain[index - 1]):
                return False
            if not valid_proof(block['transactions'][:-1], block['previous_hash'], block['proof']): #[:-1] to exclude the reward transaction or it will not work
                print("Proof of work is invalid")
                return False

    return True


def verify_transactions():
    return all([verify_transaction(tx) for tx in open_transactions])


def get_user_choice():
    user_input = input('Your choice: ')
    return user_input


# Ask to the user a digit (transaction amount)
def get_transaction_value():
    """Returns the input of the user (a new transaction amount) as a float."""
    # Get the user input, transforme it to a float and store it in user_input
    tx_recipient = input('Enter the recipient of the transaction: ')
    tx_amount = float(input('Your transaction amount please: '))
    return (tx_recipient, tx_amount)


# Output the blockchain list to the console
def print_blockchain():
    for block in blockchain:
        print('Outputting Block ')
        #print(block)
    else:
        print('-' * 20)


waiting_for_input = True
while waiting_for_input:
    print('Please choose: ')
    print('1: Add a new transaction value ')
    print('2: Mine a new block ')
    print('3: Output the blockchain blocks ')
    print('4: Output participants ')
    print('5: Check transaction validity ')
    print('h: Manipulate the chain')
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
    elif user_choice == 'h':
        # Make sure that you don't try to "hack" the blockchain if it's empty
        if len(blockchain) >= 1:
            blockchain[0] = {
                'previous_hash': '',
                'index': 0,
                'transactions': [{'sender': 'Chris', 'recipient': 'Max', 'amount': 100.0}]
            }
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
