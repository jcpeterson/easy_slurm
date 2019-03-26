from __future__ import print_function
import os
import json
#import math
import argparse
from datetime import datetime

from utils import *

id_format = '%Y-%m-%d_%H-%M-%S'
search_id = datetime.now().strftime(id_format)

parser = argparse.ArgumentParser()
parser.add_argument(
    "-c", 
    "--config", 
    type=str,
    default="config.json"
)
args = parser.parse_args()

# load config from json file
with open(args.config) as f:
    config = json.load(f)

# script params -------------------------

TEST_MODE = config['test_mode']                # submit jobs or just observe output
VERBOSE = config['verbose']                    # 0, 1, or 2
MODE = config['mode']                          # wrap, array, multiprog (only wrap works for now)
MP_BATCH_SIZE = config['multiprog_batch_size']

# job params ----------------------------

ROOT = ''
OUT_DIR = search_id

# python script its argument grid
py_fn = config['python_script']
arg_grid = config['argument_grid']

# sbatch param (override defaults)
sbatch_args = config['sbatch_args']

# core functions -----------------------

def expand_py_flags(cmd, params):
    for arg in params.keys():
        value = params[arg]
        if not is_bool(value):
            cmd = "{} --{} {}".format(cmd, arg, value)
        else:
            if value: cmd = "{} --{}".format(cmd, arg)
    return cmd

def update_cmd(curr_cmd, new_cmd, 
               mode=MODE, space=True):
    end = ' '
    if not space: 
        end = ''

    if mode=='wrap':
        return curr_cmd + new_cmd + end

    elif mode=='multiprog':
        return curr_cmd + ['#SBATCH {}{}'.format(new_cmd, end)]

def get_sbatch_cmd(n_tasks=1,
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
        # n_tasks / ntasks seem reversed here
        cmd = update_cmd(cmd, '-N {}'.format(n_tasks))
        cmd = update_cmd(cmd, '-c {}'.format(cores))
        cmd = update_cmd(cmd, '--ntasks-per-node=1')
    elif mode == 'multiprog':
        cmd = update_cmd(cmd, '-n {}'.format(n_tasks))  

    if n_gpus > 0:
        cmd = update_cmd(cmd, '--gres=gpu:{}'.format(n_gpus))
    if mem > 0: 
        cmd = update_cmd(cmd, '--mem={}'.format(mem))

    # time limit
    cmd = update_cmd(cmd, '-t {}'.format(minutes))

    # email commands
    if email != '':
        cmd = update_cmd(cmd, '--mail-type=begin,end')
        cmd = update_cmd(cmd, '--mail-user={}'.format(email))

    return cmd

def get_out_fn(py_params, mode=MODE, 
               root=ROOT, out_dir=OUT_DIR,
               just_fn=False, mpid=None):
    """ Create slurm .out filename from python
        flags. If more than one flag value in
        py_params dict, all are included.
    """

    if mode == 'wrap':
        out_fn = ''
    elif mode == 'multiprog':
        if mpid is None: 
            mpid = ''
        else:
            mpid = str(mpid)
            out_fn = '{}_multiprog{}_'.format(py_fn[:-3], mpid)

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
script_path = os.path.join(ROOT, py_fn)
py_cmd_base = 'python -u {}'.format(script_path)

# flatten the grid so we can iterate
# through params with one loop
flat_grid = flatten_grid(arg_grid)
n_jobs = len(flat_grid)

if VERBOSE > 0:
    print('Submitting', n_jobs, 'jobs...')

# create output dir if needed
if (not os.path.exists(OUT_DIR) and
    not TEST_MODE):
    os.makedirs(OUT_DIR)

######################################
# MAIN LOOP: construct each job/task #
######################################

for i, params in enumerate(flat_grid):

    # create python command with flags for these params
    py_cmd = py_cmd_base
    py_cmd = expand_py_flags(py_cmd, params)

    if MODE == 'wrap':
        full_cmd = get_sbatch_cmd() + get_out_fn(params)
        full_cmd = '{} --wrap "{}"'.format(full_cmd, py_cmd)
    
        if VERBOSE > 1:
            print('JOB', str(i+1)+':', full_cmd)
            print('')

        if not TEST_MODE: 
            os.system(full_cmd)

    if MODE == 'multiprog':

        if i % MP_BATCH_SIZE == 0:
            if i != 0:
                if not TEST_MODE:
                    list2txt(curr_sbatch_cmd, 
                        os.path.join(OUT_DIR, 'RUN_'+str(file_idx)+'.cmd'))
                    list2txt(py_cmd_list, 
                        os.path.join(OUT_DIR, conf_fn))
                    os.system('sbatch ' + os.path.join(OUT_DIR, 'RUN_'+str(file_idx)+'.cmd'))

            file_idx = int(i / MP_BATCH_SIZE)

            out_fn = get_out_fn(arg_grid, mpid=file_idx)
            conf_fn = get_out_fn(arg_grid, just_fn=True, mpid=file_idx) + '.conf'

            curr_sbatch_cmd = get_sbatch_cmd(n_tasks=MP_BATCH_SIZE,
                                             **sbatch_args)
            curr_sbatch_cmd = update_cmd(curr_sbatch_cmd, out_fn)
            curr_sbatch_cmd.append('') 
            curr_sbatch_cmd.append('srun --wait 0 --multi-prog ' + os.path.join(OUT_DIR, conf_fn))

            py_cmd_list = []
            py_cmd_list.append(str(i % MP_BATCH_SIZE) + ' ' + py_cmd)
        else:
            py_cmd_list.append(str(i % MP_BATCH_SIZE) + ' ' + py_cmd)

if len(flat_grid) % MP_BATCH_SIZE != 0:
    if not TEST_MODE:
        curr_sbatch_cmd = get_sbatch_cmd(n_tasks=len(flat_grid) - (MP_BATCH_SIZE*file_idx),
                                         **sbatch_args)
        curr_sbatch_cmd = update_cmd(curr_sbatch_cmd, out_fn)
        curr_sbatch_cmd.append('') 
        curr_sbatch_cmd.append('srun --wait 0 --multi-prog ' + os.path.join(OUT_DIR, conf_fn))

        list2txt(curr_sbatch_cmd, 
            os.path.join(OUT_DIR, 'RUN_'+str(file_idx)+'.cmd'))
        list2txt(py_cmd_list, 
            os.path.join(OUT_DIR, conf_fn))
        os.system('sbatch ' + os.path.join(OUT_DIR, 'RUN_'+str(file_idx)+'.cmd'))

if VERBOSE > 0:
    print('Submitted', n_jobs, 'jobs.')