# Contains helper functions for your apps!
from os import listdir, remove

# If the io following files are in the current directory, remove them!
# 1. 'currency_pair.txt'
# 2. 'currency_pair_history.csv'
# 3. 'trade_order.p'
def check_for_and_del_io_files():
    # Your code goes here.
    for path in ["currency_pair.txt", "currency_pair_history.csv", "trade_order.p"]:
        if path in listdir():
            remove(path)
    pass # nothing gets returned by this function, so end it with 'pass'.