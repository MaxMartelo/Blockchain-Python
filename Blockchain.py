# Definition of the list blockchain and of the genesis block 
MINING_REWARD = 10

genesis_block = {
        'previous_hash': '', 
        'index': 0, 
        'transactions': []
        }
blockchain = [genesis_block]
open_transactions = []
owner = 'Max' # In realty it is a pseudo like zorufdshfdhgnsdoiusjd
participants = {'Max'} # At the beginning, I am the only participant 


def hash_block(block):
    return '-'.join([str(block[key]) for key in block]) # Join is used to join stg between elements 

def get_balance(participant):
    tx_sender = [[tx['amount'] for tx in block['transactions'] if tx['sender'] == participant] for block in blockchain]
    open_tx_sender = [tx['amount'] for tx in open_transactions if tx['sender'] == participant]
    tx_sender.append(open_tx_sender)
    amount_sent = 0
    for tx in tx_sender:
        if len(tx) > 0:
             amount_sent += tx[0]

    tx_recipient = [[tx['amount'] for tx in block['transactions'] if tx['recipient'] == participant] for block in blockchain]
    amount_received = 0
    for tx in tx_recipient:
        if len(tx) > 0:
             amount_received += tx[0]
    return amount_received - amount_sent


# Function that initialized the first value at -1
def get_last_blockchain_value():
    if len(blockchain) < 1 : # Case where the blockchain is empty 
        return None
    return blockchain[-1]

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

    transaction = {
        'sender': sender, 
        'recipient' : recipient, 
        'amount' : amount
    }
    if verify_transaction(transaction) : 
        open_transactions.append(transaction)
        participants.add(sender) #with a set if we add a name which already exists, nothing happend
        participants.add(recipient)
        return True 
    return False 

def mine_block():
    # Blockchain [-1] gives us the last element of the blockchain 
    last_block = blockchain [-1]
    hashed_block = hash_block(last_block) # it is the same as our for loop behind 
    # for is used to convert last_block into  a hashed_block as a string so that we can read it 
    """ for key in last_block:
        value = last_block[key]
        hashed_block += str(value) """

    reward_transaction = { #to reward mining 
        'sender' : 'MINING',
        'recipient':  owner,
        'amount' : MINING_REWARD
    }
    open_transactions.append(reward_transaction)

    # hashing algorithm
    block = {
        'previous_hash': hashed_block, 
        'index': len(blockchain), 
        'transactions': open_transactions
        }
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
    user_input = input('Your choice: ')
    return user_input

# Output the blockchain list to the console
def print_blockchain():
    for block in blockchain:
        print('Outputting Block ')
        print(block)
    else:
        print('-' * 20)

def verify_chain():
    #verify the current blockchain and return True if it's valid, False otherwise 
    for (index, block) in enumerate(blockchain): # enumerate gives us a Tuple of informations
            if index == 0:
                continue 
            if block['previous_hash'] != hash_block(blockchain[index - 1]):
                return False
    return True


waiting_for_input = True
while waiting_for_input:
    print('Please choose: ')
    print('1: Add a new transaction value ')
    print('2: Mine a new block ')
    print('3: Output the blockchain blocks ')
    print('4: Output participants ')
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
    elif user_choice == '3' :
        print_blockchain()
    elif user_choice == '4' :
        print(participants)
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
    print(get_balance('Max'))
else: 
    print('User left!')



