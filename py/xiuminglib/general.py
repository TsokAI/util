"""
General Utility Functions

Xiuming Zhang, MIT CSAIL
April 2018
"""

import sys
from os.path import abspath
import re
import numpy as np

import config
logger, thisfile = config.create_logger(abspath(__file__))


def find_extrema_in(arr, find_max=True, n=1):
    """
    Find top (or bottom) value(s) in an m-D numpy array

    Args:
        arr: Array
            m-D numpy array
        find_max: Whether to find the maxima or minima
            Boolean
            Optional; defaults to True
        n: Number of values to return
            Positive integer
            Optional; defaults to 1

    Returns:
        ind: Indice(s) that give the extrema
            m-tuple of numpy arrays of n integers
        val: Extremum values, i.e., `arr[ind]`
            Numpy array of length n
    """
    if find_max:
        arr_to_sort = -arr
    else:
        arr_to_sort = arr
    ind = np.argsort(arr_to_sort.flatten())[:n] # linear
    ind = np.unravel_index(ind, arr.shape)
    val = arr[ind]
    return ind, val


def print_attrs(obj, excerpts=None, excerpt_win_size=60, max_recursion_depth=None):
    """
    Print all attributes, recursively, of an object

    Args:
        obj: Object in which we search for the attribute
            Any object
        excerpts: Print only excerpts containing certain attributes
            A single string or a list thereof
            Optional; defaults to None (print all)
        excerpt_win_size: How many characters get printed around a match
            Positive integer
            Optional; defaults to 60
        max_recursion_depth: Maximum recursion depth
            Positive integer
            Optional; defaults to None (no limit)
    """
    import jsonpickle
    import yaml

    logger.name = thisfile + '->print_attrs()'

    if isinstance(excerpts, str):
        excerpts = [excerpts]
    assert isinstance(excerpts, list) or excerpts is None

    try:
        serialized = jsonpickle.encode(obj, max_depth=max_recursion_depth)
    except RecursionError as e:
        logger.error("RecursionError: %s! Please specify a limit to retry",
                     str(e))
        sys.exit(1)

    if excerpts is None:
        # Print all attributes
        logger.info("All attributes:")
        print(yaml.dump(yaml.load(serialized), indent=4))
    else:
        for x in excerpts:
            # For each attribute of interest, print excerpts containing it
            logger.info("Excerpt(s) containing '%s':", x)

            mis = [m.start() for m in re.finditer(x, serialized)]
            if not mis:
                logger.info("%s: No matches! Retry maybe with deeper recursion")
            else:
                for mii, mi in enumerate(mis):
                    # For each excerpt
                    m_start = mi - excerpt_win_size // 2
                    m_end = mi + excerpt_win_size // 2
                    print(
                        "Match %d (index: %d): ...%s\033[0;31m%s\033[00m%s..." % (
                            mii,
                            mi,
                            serialized[m_start:mi],
                            serialized[mi:(mi + len(x))],
                            serialized[(mi + len(x)):m_end],
                        )
                    )
