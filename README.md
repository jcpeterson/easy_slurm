# easy_slurm
easily run slurm jobs with a python dictionary of argument values to gridsearch

Specify whether to test or submit jobs (`TEST_MODE`), verbosity level `VERBOSE`, the python script `py_fn` and its arguments `arg_grid`, and non-default arguments (`sbatch_args`) for the slurm jobs in `slurm_jobber.py`:
```python
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
```

Example output:
```
sbatch -p all -N 1 --ntasks-per-node=1 --gres=gpu:1 --mem=17000 --time=1 --output float_0.1_include_flag_True_int_1_str_a_.out --wrap "python return_args.py --float 0.1 --include_flag --int 1 --str a"
sbatch -p all -N 1 --ntasks-per-node=1 --gres=gpu:1 --mem=17000 --time=1 --output float_0.1_include_flag_True_int_1_str_b_.out --wrap "python return_args.py --float 0.1 --include_flag --int 1 --str b"
sbatch -p all -N 1 --ntasks-per-node=1 --gres=gpu:1 --mem=17000 --time=1 --output float_0.1_include_flag_True_int_1_str_c_.out --wrap "python return_args.py --float 0.1 --include_flag --int 1 --str c"
sbatch -p all -N 1 --ntasks-per-node=1 --gres=gpu:1 --mem=17000 --time=1 --output float_0.1_include_flag_True_int_2_str_a_.out --wrap "python return_args.py --float 0.1 --include_flag --int 2 --str a"
sbatch -p all -N 1 --ntasks-per-node=1 --gres=gpu:1 --mem=17000 --time=1 --output float_0.1_include_flag_True_int_2_str_b_.out --wrap "python return_args.py --float 0.1 --include_flag --int 2 --str b"
sbatch -p all -N 1 --ntasks-per-node=1 --gres=gpu:1 --mem=17000 --time=1 --output float_0.1_include_flag_True_int_2_str_c_.out --wrap "python return_args.py --float 0.1 --include_flag --int 2 --str c"
sbatch -p all -N 1 --ntasks-per-node=1 --gres=gpu:1 --mem=17000 --time=1 --output float_0.1_include_flag_True_int_3_str_a_.out --wrap "python return_args.py --float 0.1 --include_flag --int 3 --str a"
sbatch -p all -N 1 --ntasks-per-node=1 --gres=gpu:1 --mem=17000 --time=1 --output float_0.1_include_flag_True_int_3_str_b_.out --wrap "python return_args.py --float 0.1 --include_flag --int 3 --str b"
sbatch -p all -N 1 --ntasks-per-node=1 --gres=gpu:1 --mem=17000 --time=1 --output float_0.1_include_flag_True_int_3_str_c_.out --wrap "python return_args.py --float 0.1 --include_flag --int 3 --str c"
sbatch -p all -N 1 --ntasks-per-node=1 --gres=gpu:1 --mem=17000 --time=1 --output float_0.1_include_flag_False_int_1_str_a_.out --wrap "python return_args.py --float 0.1 --int 1 --str a"
sbatch -p all -N 1 --ntasks-per-node=1 --gres=gpu:1 --mem=17000 --time=1 --output float_0.1_include_flag_False_int_1_str_b_.out --wrap "python return_args.py --float 0.1 --int 1 --str b"
sbatch -p all -N 1 --ntasks-per-node=1 --gres=gpu:1 --mem=17000 --time=1 --output float_0.1_include_flag_False_int_1_str_c_.out --wrap "python return_args.py --float 0.1 --int 1 --str c"
sbatch -p all -N 1 --ntasks-per-node=1 --gres=gpu:1 --mem=17000 --time=1 --output float_0.1_include_flag_False_int_2_str_a_.out --wrap "python return_args.py --float 0.1 --int 2 --str a"
sbatch -p all -N 1 --ntasks-per-node=1 --gres=gpu:1 --mem=17000 --time=1 --output float_0.1_include_flag_False_int_2_str_b_.out --wrap "python return_args.py --float 0.1 --int 2 --str b"
sbatch -p all -N 1 --ntasks-per-node=1 --gres=gpu:1 --mem=17000 --time=1 --output float_0.1_include_flag_False_int_2_str_c_.out --wrap "python return_args.py --float 0.1 --int 2 --str c"
sbatch -p all -N 1 --ntasks-per-node=1 --gres=gpu:1 --mem=17000 --time=1 --output float_0.1_include_flag_False_int_3_str_a_.out --wrap "python return_args.py --float 0.1 --int 3 --str a"
sbatch -p all -N 1 --ntasks-per-node=1 --gres=gpu:1 --mem=17000 --time=1 --output float_0.1_include_flag_False_int_3_str_b_.out --wrap "python return_args.py --float 0.1 --int 3 --str b"
sbatch -p all -N 1 --ntasks-per-node=1 --gres=gpu:1 --mem=17000 --time=1 --output float_0.1_include_flag_False_int_3_str_c_.out --wrap "python return_args.py --float 0.1 --int 3 --str c"
sbatch -p all -N 1 --ntasks-per-node=1 --gres=gpu:1 --mem=17000 --time=1 --output float_0.2_include_flag_True_int_1_str_a_.out --wrap "python return_args.py --float 0.2 --include_flag --int 1 --str a"
sbatch -p all -N 1 --ntasks-per-node=1 --gres=gpu:1 --mem=17000 --time=1 --output float_0.2_include_flag_True_int_1_str_b_.out --wrap "python return_args.py --float 0.2 --include_flag --int 1 --str b"
sbatch -p all -N 1 --ntasks-per-node=1 --gres=gpu:1 --mem=17000 --time=1 --output float_0.2_include_flag_True_int_1_str_c_.out --wrap "python return_args.py --float 0.2 --include_flag --int 1 --str c"
sbatch -p all -N 1 --ntasks-per-node=1 --gres=gpu:1 --mem=17000 --time=1 --output float_0.2_include_flag_True_int_2_str_a_.out --wrap "python return_args.py --float 0.2 --include_flag --int 2 --str a"
sbatch -p all -N 1 --ntasks-per-node=1 --gres=gpu:1 --mem=17000 --time=1 --output float_0.2_include_flag_True_int_2_str_b_.out --wrap "python return_args.py --float 0.2 --include_flag --int 2 --str b"
sbatch -p all -N 1 --ntasks-per-node=1 --gres=gpu:1 --mem=17000 --time=1 --output float_0.2_include_flag_True_int_2_str_c_.out --wrap "python return_args.py --float 0.2 --include_flag --int 2 --str c"
sbatch -p all -N 1 --ntasks-per-node=1 --gres=gpu:1 --mem=17000 --time=1 --output float_0.2_include_flag_True_int_3_str_a_.out --wrap "python return_args.py --float 0.2 --include_flag --int 3 --str a"
sbatch -p all -N 1 --ntasks-per-node=1 --gres=gpu:1 --mem=17000 --time=1 --output float_0.2_include_flag_True_int_3_str_b_.out --wrap "python return_args.py --float 0.2 --include_flag --int 3 --str b"
sbatch -p all -N 1 --ntasks-per-node=1 --gres=gpu:1 --mem=17000 --time=1 --output float_0.2_include_flag_True_int_3_str_c_.out --wrap "python return_args.py --float 0.2 --include_flag --int 3 --str c"
sbatch -p all -N 1 --ntasks-per-node=1 --gres=gpu:1 --mem=17000 --time=1 --output float_0.2_include_flag_False_int_1_str_a_.out --wrap "python return_args.py --float 0.2 --int 1 --str a"
sbatch -p all -N 1 --ntasks-per-node=1 --gres=gpu:1 --mem=17000 --time=1 --output float_0.2_include_flag_False_int_1_str_b_.out --wrap "python return_args.py --float 0.2 --int 1 --str b"
sbatch -p all -N 1 --ntasks-per-node=1 --gres=gpu:1 --mem=17000 --time=1 --output float_0.2_include_flag_False_int_1_str_c_.out --wrap "python return_args.py --float 0.2 --int 1 --str c"
sbatch -p all -N 1 --ntasks-per-node=1 --gres=gpu:1 --mem=17000 --time=1 --output float_0.2_include_flag_False_int_2_str_a_.out --wrap "python return_args.py --float 0.2 --int 2 --str a"
sbatch -p all -N 1 --ntasks-per-node=1 --gres=gpu:1 --mem=17000 --time=1 --output float_0.2_include_flag_False_int_2_str_b_.out --wrap "python return_args.py --float 0.2 --int 2 --str b"
sbatch -p all -N 1 --ntasks-per-node=1 --gres=gpu:1 --mem=17000 --time=1 --output float_0.2_include_flag_False_int_2_str_c_.out --wrap "python return_args.py --float 0.2 --int 2 --str c"
sbatch -p all -N 1 --ntasks-per-node=1 --gres=gpu:1 --mem=17000 --time=1 --output float_0.2_include_flag_False_int_3_str_a_.out --wrap "python return_args.py --float 0.2 --int 3 --str a"
sbatch -p all -N 1 --ntasks-per-node=1 --gres=gpu:1 --mem=17000 --time=1 --output float_0.2_include_flag_False_int_3_str_b_.out --wrap "python return_args.py --float 0.2 --int 3 --str b"
sbatch -p all -N 1 --ntasks-per-node=1 --gres=gpu:1 --mem=17000 --time=1 --output float_0.2_include_flag_False_int_3_str_c_.out --wrap "python return_args.py --float 0.2 --int 3 --str c"
sbatch -p all -N 1 --ntasks-per-node=1 --gres=gpu:1 --mem=17000 --time=1 --output float_0.3_include_flag_True_int_1_str_a_.out --wrap "python return_args.py --float 0.3 --include_flag --int 1 --str a"
sbatch -p all -N 1 --ntasks-per-node=1 --gres=gpu:1 --mem=17000 --time=1 --output float_0.3_include_flag_True_int_1_str_b_.out --wrap "python return_args.py --float 0.3 --include_flag --int 1 --str b"
sbatch -p all -N 1 --ntasks-per-node=1 --gres=gpu:1 --mem=17000 --time=1 --output float_0.3_include_flag_True_int_1_str_c_.out --wrap "python return_args.py --float 0.3 --include_flag --int 1 --str c"
sbatch -p all -N 1 --ntasks-per-node=1 --gres=gpu:1 --mem=17000 --time=1 --output float_0.3_include_flag_True_int_2_str_a_.out --wrap "python return_args.py --float 0.3 --include_flag --int 2 --str a"
sbatch -p all -N 1 --ntasks-per-node=1 --gres=gpu:1 --mem=17000 --time=1 --output float_0.3_include_flag_True_int_2_str_b_.out --wrap "python return_args.py --float 0.3 --include_flag --int 2 --str b"
sbatch -p all -N 1 --ntasks-per-node=1 --gres=gpu:1 --mem=17000 --time=1 --output float_0.3_include_flag_True_int_2_str_c_.out --wrap "python return_args.py --float 0.3 --include_flag --int 2 --str c"
sbatch -p all -N 1 --ntasks-per-node=1 --gres=gpu:1 --mem=17000 --time=1 --output float_0.3_include_flag_True_int_3_str_a_.out --wrap "python return_args.py --float 0.3 --include_flag --int 3 --str a"
sbatch -p all -N 1 --ntasks-per-node=1 --gres=gpu:1 --mem=17000 --time=1 --output float_0.3_include_flag_True_int_3_str_b_.out --wrap "python return_args.py --float 0.3 --include_flag --int 3 --str b"
sbatch -p all -N 1 --ntasks-per-node=1 --gres=gpu:1 --mem=17000 --time=1 --output float_0.3_include_flag_True_int_3_str_c_.out --wrap "python return_args.py --float 0.3 --include_flag --int 3 --str c"
sbatch -p all -N 1 --ntasks-per-node=1 --gres=gpu:1 --mem=17000 --time=1 --output float_0.3_include_flag_False_int_1_str_a_.out --wrap "python return_args.py --float 0.3 --int 1 --str a"
sbatch -p all -N 1 --ntasks-per-node=1 --gres=gpu:1 --mem=17000 --time=1 --output float_0.3_include_flag_False_int_1_str_b_.out --wrap "python return_args.py --float 0.3 --int 1 --str b"
sbatch -p all -N 1 --ntasks-per-node=1 --gres=gpu:1 --mem=17000 --time=1 --output float_0.3_include_flag_False_int_1_str_c_.out --wrap "python return_args.py --float 0.3 --int 1 --str c"
sbatch -p all -N 1 --ntasks-per-node=1 --gres=gpu:1 --mem=17000 --time=1 --output float_0.3_include_flag_False_int_2_str_a_.out --wrap "python return_args.py --float 0.3 --int 2 --str a"
sbatch -p all -N 1 --ntasks-per-node=1 --gres=gpu:1 --mem=17000 --time=1 --output float_0.3_include_flag_False_int_2_str_b_.out --wrap "python return_args.py --float 0.3 --int 2 --str b"
sbatch -p all -N 1 --ntasks-per-node=1 --gres=gpu:1 --mem=17000 --time=1 --output float_0.3_include_flag_False_int_2_str_c_.out --wrap "python return_args.py --float 0.3 --int 2 --str c"
sbatch -p all -N 1 --ntasks-per-node=1 --gres=gpu:1 --mem=17000 --time=1 --output float_0.3_include_flag_False_int_3_str_a_.out --wrap "python return_args.py --float 0.3 --int 3 --str a"
sbatch -p all -N 1 --ntasks-per-node=1 --gres=gpu:1 --mem=17000 --time=1 --output float_0.3_include_flag_False_int_3_str_b_.out --wrap "python return_args.py --float 0.3 --int 3 --str b"
sbatch -p all -N 1 --ntasks-per-node=1 --gres=gpu:1 --mem=17000 --time=1 --output float_0.3_include_flag_False_int_3_str_c_.out --wrap "python return_args.py --float 0.3 --int 3 --str c"
```
