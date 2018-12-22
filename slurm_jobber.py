from __future__ import print_function
import os
from itertools import product

#########################################
# script params -------------------------

TEST_MODE = True      # submit jobs or just observe output
VERBOSE = 2           # 0, 1, or 2
MODE = 'wrap'         # wrap, array, multiprog (only wrap works for now)

# job params ----------------------------

# if no root given, replace with os.getcwd()
ROOT = ''
if ROOT == '': ROOT = os.getcwd()

OUT_DIR = 'out_files'

# python script its argument grid
py_fn = 'return_args.py'
arg_grid = {
                'int'         : [1,2], 
                'float'       : [0.1, 0.2],
                'str'         : ['a','b'],
                'include_flag': [True, False] 
            }

# sbatch param (override defaults) ------
sbatch_args = {
    'minutes': 1
}
#########################################

# basic error checks ---------------------
# make sure valid py file is given
if '.py' not in py_fn:
    print('ERROR -- '+py_fn+' not a python file')    
    exit()

# helper functions -----------------------

def is_bool(object):
    return isinstance(object, bool)

def list2txt(lines, filename):
    """ Save each item in a list to a
        separate line in a text file.
    """
    with open(filename, 'w') as f:
        for line in lines:
            f.write("%s\n" % line)

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

# main functions -----------------------

def expand_py_flags(cmd, params):
    for arg in params.keys():
        value = params[arg]
        if not is_bool(value):
            cmd += '--'+ arg + ' ' + str(value) + ' '
        else:
            if value: cmd += '--'+ arg + ' ' 
    return cmd

def update_cmd(curr_cmd, new_cmd, 
               mode=MODE, space=True):
    end = ' '
    if not space: 
        end = ''

    if mode=='wrap':
        return curr_cmd + new_cmd + end
    elif mode=='multiprog':
        return curr_cmd + ['#SBATCH ' + new_cmd + end]

def get_sbatch_cmd(grid,
                   mode=MODE,
                   email='',
                   minutes=60,
                   n_gpus=1,
                   mem=17000,
                   cores=1):

    """ Create sbatch command; return as
        a large string object.
    """
    if mode == 'multiprog':
        cmd = ['#!/bin/bash']
    else:
        cmd = update_cmd('', 'sbatch')

    # hardware specs
    if mode == 'wrap':
        cmd = update_cmd(cmd, '-N 1')
        cmd = update_cmd(cmd, '--ntasks-per-node=1')
        cmd = update_cmd(cmd, '--cpus-per-task=' + str(cores))
    elif mode == 'multiprog':
        cmd = update_cmd(cmd, '-n ' + str(len(grid)))    

    if n_gpus > 0:
        cmd = update_cmd(cmd, '--gres=gpu:' + str(n_gpus))
    if mem > 0: 
        cmd = update_cmd(cmd, '--mem=' + str(mem))

    # time limit
    cmd = update_cmd(cmd, '-t ' + str(minutes))

    # email commands
    if email != '':
        cmd = update_cmd(cmd, '--mail-type=begin,end')
        cmd = update_cmd(cmd, '--mail-user=' + email)

    return cmd

def get_out_fn(py_params, mode=MODE, 
               root=ROOT, out_dir=OUT_DIR,
               just_fn=False):
    """ Create slurm .out filename from python
        flags. If more than one flag value in
        py_params dict, all are included.
    """

    if mode == 'wrap':
        out_fn = ''      
    elif mode == 'multiprog':
        out_fn = py_fn[:-3] + '_multiprog_'

    for k, key in enumerate(py_params.keys()):

        if mode == 'wrap':
            value = py_params[key]
            if len(str(value)) < 10:
                out_fn += key + '_' + str(value)

        elif mode == 'multiprog':
            values = py_params[key]
            out_fn += key + '_'
            for value in values:
                if len(str(value)) < 10:
                    out_fn += str(value) + ','
            out_fn = out_fn[:-1]

        if k != len(py_params.keys()) - 1:
            out_fn += '_'

    if not just_fn:
        out_fn += '.out'
        out_fn = os.path.join(root, 
                              out_dir, 
                              out_fn)
        return '--output ' + out_fn
    else:
        return out_fn

# basic start of the command
py_cmd_base = 'python -u '
py_cmd_base += os.path.join(ROOT, py_fn) + ' '

# flatten the grid so we can iterate
# through params with one loop
flat_grid = flatten_grid(arg_grid)
n_jobs = len(flat_grid)

if VERBOSE > 0:
    print('Submitting', n_jobs, 'jobs...')

sbatch_cmd = get_sbatch_cmd(flat_grid, **sbatch_args)

if MODE == 'multiprog':
    out_fn = get_out_fn(arg_grid)
    sbatch_cmd = update_cmd(sbatch_cmd, out_fn)
    conf_fn = get_out_fn(arg_grid, just_fn=True) + '.conf'
    sbatch_cmd.append('srun --multi-prog '+conf_fn)
    print('')
    if VERBOSE > 0:
        for line in sbatch_cmd: print(line)

######################################
# MAIN LOOP: construct each job/task #
######################################

if MODE == 'multiprog':
    py_cmd_list = []
    print('')

for i, params in enumerate(flat_grid):

    # create python command with flags for these params
    py_cmd = py_cmd_base
    py_cmd = expand_py_flags(py_cmd, params)

    if MODE == 'wrap':
        full_cmd = sbatch_cmd + get_out_fn(params)
        full_cmd += ' --wrap "'
        full_cmd += py_cmd[:-1] + '"'
    
        if VERBOSE > 1:
            print('JOB', str(i+1)+':', full_cmd)
            print('')

        if not TEST_MODE: 
            os.system(full_cmd)

    if MODE == 'multiprog':
        py_cmd_list.append(str(i) + ' ' + py_cmd)
        if VERBOSE > 1:
            print(str(i) + ' ' + py_cmd)

if not TEST_MODE:
    if MODE == 'multiprog':
        list2txt(sbatch_cmd, 'RUN.cmd')
        list2txt(py_cmd_list, conf_fn)
    if VERBOSE > 0:
        print('Submitted', n_jobs, 'jobs.')