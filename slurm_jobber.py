from __future__ import print_function
import os
from itertools import product

# script params -------------------------

TEST_MODE = True
VERBOSE = 2      # 0, 1, or 2
TYPE = 'wrap'    # wrap, array, multiprog (only wrap works for now)

# job params ----------------------------

# if no root given, replace with os.getcwd()
root = ''
if root == '': 
    root = os.getcwd()

# python script its argument grid
py_fn = 'return_args.py'
arg_grid = {
                'int'         : [1,2,3], 
                'float'       : [0.1, 0.2, 0.3],
                'str'         : ['a','b','c'],
                'include_flag': [True, False] 
            }

# sbatch param (override defaults) ------
sbatch_args = {
    'minutes': 1
}

# basic error checks ---------------------
# make sure valid py file is given
if '.py' not in py_fn:
    print("ERROR -- '"+py_fn+"' not a python file")    
    exit()


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

def get_sbatch_cmd(py_params, email='',
                   minutes=60, n_gpus=1,
                   mem=17000, cores=1):

    """ Create sbatch command; return as
        a large string object.
    """
    cmd = 'sbatch '

    # hardware specs
    cmd += '-p all '
    cmd += '-N 1 '
    cmd += '--ntasks-per-node=1 '
    cmd += '--cpus-per-task=' + str(cores) + ' '
    if n_gpus > 0:
        cmd += '--gres=gpu:' + str(n_gpus) + ' '
    if mem != 0: cmd += '--mem=' + str(mem) + ' '

    # time limit
    cmd += '--time=' + str(minutes) + ' '

    # email commands
    if email != '':
        cmd += '--mail-type=begin,end '
        cmd += '--mail-user=' + email + ' '

    # .out filenames made from python arg combos
    out_fn = 'out_files/'
    for arg in py_params.keys():
        value = params[arg]
        if len(str(value)) < 10:
            out_fn += arg + '_' + str(value) + '_'
    out_fn += '.out'
    cmd += '--output ' + out_fn

    return cmd



# basic start of the command
cmd = 'python -u ./'
cmd += py_fn + ' '

# flatten the grid so we can iterate
# through params with one loop
flat_grid = flatten_grid(arg_grid)
n_jobs = len(flat_grid)

if VERBOSE > 0:
    print('Submitting', n_jobs, 'jobs...')

# loop to construct each job/task
for i, params in enumerate(flat_grid):
    # the current command is the base plus
    # the current param set
    py_cmd = cmd

    for arg in params.keys():
        value = params[arg]
        if not is_bool(value):
            py_cmd += '--'+arg + ' ' + str(value) + ' '
        else:
            if value: py_cmd += '--'+arg + ' '    
    
    sbatch_cmd = get_sbatch_cmd(params, **sbatch_args)

    full_cmd = sbatch_cmd
    full_cmd += ' --wrap "'
    full_cmd += py_cmd[:-1] + '"'
    
    if VERBOSE > 1:
        print('')
        print('Job', i+1)
        print(full_cmd)

    if not TEST_MODE: os.system(full_cmd)

print('Submitted', n_jobs, 'jobs')