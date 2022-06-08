import hashlib as hl
import json


def hash_string_256(string):
    return hl.sha256(string).hexdigest() #haslib.sha256 is used to create a hash of 64 character and hexdigest method si used to conert the bit hash into a string


def hash_block(block):
    """Hashes a block and returns a sring representation of it.

    Args:
        block : The block that should be hashed
    """
    #return '-'.join([str(block[key]) for key in block]) :  .join is used to join stg between elements : not secure
    return hash_string_256(json.dumps(block, sort_keys=True).encode()) #json.dumps is used to transform dict to string 
    #sort_key is used to sort the keys of the dict before dumping it to a string so even if the order changed, it is not a problem 
