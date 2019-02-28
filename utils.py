from itertools import product

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