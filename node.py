from uuid import uuid4 #to generate unique ID

from Blockchain import Blockchain

from verification import Verification
class Node: 
    def __init__(self):
        """Constructor of node class
        """
        #self.id = str(uuid4())
        self.id = 'Max'
        self.blockchain = Blockchain(self.id)
        
    # Ask to the user a digit (transaction amount)
    def get_transaction_value(self):
        """Returns the input of the user (a new transaction amount) as a float."""
        # Get the user input, transforme it to a float and store it in user_input
        tx_recipient = input('Enter the recipient of the transaction: ')
        tx_amount = float(input('Your transaction amount please: '))
        return (tx_recipient, tx_amount)


    def get_user_choice(self):
        """Prompts the user for its choice and return it."""
        user_input = input('Your choice: ')
        return user_input


    def print_blockchain(self):
        """Output all blocks of the blockchain"""
        for block in self.blockchain.chain:
            print('Outputting Block ')
            print(block)
        else:
            print('-' * 20)

    def listen_for_input(self):
        waiting_for_input = True
 
        while waiting_for_input:
            print('Please choose: ')
            print('1: Add a new transaction value ')
            print('2: Mine a new block ')
            print('3: Output the blockchain blocks ')
            print('4: Check transaction validity ')
            # print('h: Manipulate the chain')
            print('q: Quit')
            user_choice = self.get_user_choice()
            if user_choice == '1':
                tx_data = self.get_transaction_value()
                recipient, amount = tx_data
                # Add the transaction amount to the blockchain
                if self.blockchain.add_transaction(recipient,self.id, amount=amount): #amount = amount to skip the sender para
                    print('Added transaction')
                else :
                    print('Transaction failed')
                print(self.blockchain.open_transactions)
            elif user_choice == '2' :
                self.blockchain.mine_block()  
            elif user_choice == '3' :
                self.print_blockchain()
            elif user_choice == '4' :
                verifier = Verification()
                if verifier.verify_transactions(self.blockchain.open_transactions, self.blockchain.get_balance):
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
            verifier = Verification()
            if  not verifier.verify_chain(self.blockchain.chain):
                print("Invald Blockchain")
                self.print_blockchain()
                break
            print('Balance of {}: {:6.2f}'.format(self.id, self.blockchain.get_balance()))# format the amount to 6 digits and 2 after point
        else:
            print('User left!')


#to start the program
node = Node()
node.listen_for_input()