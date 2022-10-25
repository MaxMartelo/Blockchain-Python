from uuid import uuid4 #to generate unique ID

from Blockchain import Blockchain

from utility.verification import Verification

from wallet import Wallet
class Node: 
    def __init__(self):
        """Constructor of node class
        """
        #self.id = str(uuid4())
        self.wallet = Wallet()
        self.wallet.create_keys()
        self.blockchain = Blockchain(self.wallet.public_key)
        
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
            print('5: Create wallet')
            print('6: Load wallet')
            print('7: Save keys')
            print('q: Quit')
            user_choice = self.get_user_choice()
            if user_choice == '1':
                tx_data = self.get_transaction_value()
                recipient, amount = tx_data
                # Add the transaction amount to the blockchain
                signature = self.wallet.sign_transaction(self.wallet.public_key, recipient, amount)
                if self.blockchain.add_transaction(recipient,self.wallet.public_key, signature, amount=amount): #amount = amount to skip the sender para
                    print('Added transaction')
                else :
                    print('Transaction failed')
                print(self.blockchain.get_open_transactions())
            elif user_choice == '2' :
                if not self.blockchain.mine_block():
                    print('Mining failed. Got no wallet ?')
            elif user_choice == '3' :
                self.print_blockchain()
            elif user_choice == '4' :
                if Verification.verify_transactions(self.blockchain.get_open_transactions(), self.blockchain.get_balance):
                    print("All transactions are valid")
                else :
                    print("There are invalid transactions")
            elif user_choice == '5':
                self.wallet.create_keys()
                self.blockchain = Blockchain(self.wallet.public_key) # create a new key pair
            elif user_choice == '6':
                self.wallet.load_keys()
                self.blockchain = Blockchain(self.wallet.public_key) # create a new key pair
            elif user_choice == '7':
                self.wallet.save_keys()
            elif user_choice == 'q':
                # This will lead to the loop exist because it's running condition
                waiting_for_input = False
            else:
                print("Input was invalid, please pick a value from the list!")
            if  not Verification.verify_chain(self.blockchain.chain):
                print("Invald Blockchain")
                self.print_blockchain()
                break
            print('Balance of {}: {:6.2f}'.format(self.wallet.public_key, self.blockchain.get_balance()))# format the amount to 6 digits and 2 after point
        else:
            print('User left!')


if __name__ == '__main__':
    #to start the program
    node = Node()
    node.listen_for_input()

