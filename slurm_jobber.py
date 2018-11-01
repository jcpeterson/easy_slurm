from __future__ import print_function
# -- JOB PARAMS -------------------------
# ----------------------------------------

VERBOSE = 2 # can be 0, 1, or 2

py_fn = 'return_args.py'
arg_grid = {
                '--int'         : [1,2,3], 
                '--float'       : [0.1, 0.2, 0.3],
                #'--bool'       : [True, False],
                '--str'         : ['a','b','c'],
                '--include_flag': [True, False] 
            }

# ----------------------------------------
# ----------------------------------------

# basic error checks

# make sure valid py file is given
if '.py' not in py_fn:
    print("ERROR -- '"+py_fn+"' not a python file")    
    exit()
    
# make sure boolean args are coded using the 
# store_true convention and not with strings
#for key in arg_grid.keys():
#    for item in arg_grid[key]:
#        if isinstance(item, bool):
#            print("ERROR -- '"+key+"' contains bools!")
#            exit()

import os
from itertools import product

# helper functions

def is_bool(object):
    return isinstance(object, bool)

def flatten_grid(grid):
    """ Flatten grid into iterable list
        of parameter combinations. Adapted from
        scikit-learn's ParameterGrid class. 
    """
    flat_grid = []

    # sort the keys of a dictionary for reproducibility
    items = sorted(grid.items())

    keys, values = zip(*items)
    for v in product(*values):
        params = dict(zip(keys, v))
        flat_grid.append(params)

    return flat_grid

# basic start of the command 
cmd = 'python '
cmd += py_fn + ' '

# flatten the grid so we can iterate
# through params with one loop
flat_grid = flatten_grid(arg_grid)

for params in flat_grid:
    # the current command is the base plus
    # the current param set
    curr_cmd = cmd

    for arg in params.keys():
        value = params[arg]
        if not is_bool(value):
            curr_cmd += arg + ' ' + str(value) + ' '
        else:
            if value: curr_cmd += arg + ' '    
            
    if VERBOSE > 1: print(curr_cmd)
    os.system(curr_cmd)












#