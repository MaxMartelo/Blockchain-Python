import hashlib as hl
import json

# __all__ = ['hash_string_256', 'hash_block'] : to kind of make the other import kind of private

def hash_string_256(string):
    """Create a SHA256 hash for a given input string

    Args:
        string : The string which should be hashed 
    Returns:
        string : The hash 
    """
    return hl.sha256(string).hexdigest() #haslib.sha256 is used to create a hash of 64 character and hexdigest method is used to convert the bit hash into a string


def hash_block(block):
    """Hashes a block and returns a string representation of it.

    Args:
        block : The block that should be hashed
    """
    hashable_block = block.__dict__.copy() #dict version of the block, the copy is used to not change the original thing  
    hashable_block['transactions'] = [tx.to_ordered_dict() for tx in hashable_block['transactions']]
    #return '-'.join([str(block[key]) for key in block]) :  .join is used to join stg between elements : not secure
    return hash_string_256(json.dumps(hashable_block, sort_keys=True).encode()) #json.dumps is used to transform dict to string 
    #sort_key is used to sort the keys of the dict before dumping it to a string so even if the order changed, it is not a problem 
