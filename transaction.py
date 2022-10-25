from collections import OrderedDict
from utility.printable import Printable
class Transaction(Printable): 
    def __init__(self, sender, recipient, signature, amount):
        """A transaction wich can be added to a block in the blockchain

        Args:
            sender : The sender of coins.
            recipient : The Recipient of coins.
            signature : The signature of the transaction.
            amount : The amount of coins sent. 
        """
        self.sender = sender
        self.recipient = recipient
        self.amount = amount
        self.signature = signature

    def to_ordered_dict(self):
        return OrderedDict([('sender', self.sender), ('recipient', self.recipient), ('amount', self.amount)])