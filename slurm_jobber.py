from __future__ import print_function

### NOTE: Currently only for GPU jobs ###

# job params ----------------------------

TEST_MODE = True
VERBOSE = 2      # 0, 1, or 2

# python script to run and argument grid
py_fn = 'return_args.py'
arg_grid = {
                'int'         : [1,2,3], 
                'float'       : [0.1, 0.2, 0.3],
                'str'         : ['a','b','c'],
                'include_flag': [True, False] 
            }

# sbatch parameters (overrides defaults)
sbatch_args = {
    'minutes': 1
}


# basic error checks ---------------------
# make sure valid py file is given
if '.py' not in py_fn:
    print("ERROR -- '"+py_fn+"' not a python file")    
    exit()

# do all importing here ------------------    
import os
from itertools import product

# helper functions -----------------------

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

def get_sbatch_cmd(py_params,
                   minutes=60, n_gpus=1, 
                   mem=17000, email=''):

    """ Create sbatch command; return as
        a large string object.
    """    
    cmd = 'sbatch '

    # hardware specs
    cmd += '-p all '
    cmd += '-N 1 '
    cmd += '--ntasks-per-node=1 '
    if n_gpus > 0:
        cmd += '--gres=gpu:' + str(n_gpus) + ' '
    cmd += '--mem=' + str(mem) + ' '

    # time limit
    cmd += '--time=' + str(minutes) + ' '

    # email commands
    if email != '':
        cmd += '--mail-type=begin,end '        
        cmd += '--mail-user=' + email + ' '

    # .out filenames made from python arg combos
    out_fn = ''
    for arg in py_params.keys():
        value = params[arg]
        if len(str(value)) < 10:
            out_fn += arg + '_' + str(value) + '_' 
    out_fn += '.out'
    cmd += '--output ' + out_fn

    return cmd



# basic start of the command 
cmd = 'python '
cmd += py_fn + ' '

# flatten the grid so we can iterate
# through params with one loop
flat_grid = flatten_grid(arg_grid)

for params in flat_grid:
    # the current command is the base plus
    # the current param set
    py_cmd = cmd

    for arg in params.keys():
        value = params[arg]
        if not is_bool(value):
            py_cmd += '--'+arg + ' ' + str(value) + ' '
        else:
            if value: py_cmd += '--'+arg + ' '    
            
    #if VERBOSE > 1: print(py_cmd)

    sbatch_cmd = get_sbatch_cmd(params, **sbatch_args) 
    #if VERBOSE > 1: print(sbatch_cmd)

    full_cmd = sbatch_cmd
    full_cmd += ' --wrap "'
    full_cmd += py_cmd[:-1] + '"'
    
    if VERBOSE > 1: 
        print('')
        print(full_cmd)

    if not TEST_MODE: os.system(full_cmd)












#