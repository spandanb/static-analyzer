"""
This module contains utility functions that perform 
tasks such as checking whether whether a file is a python 
module to getting an absolute path from a relative path.
"""
    
def abspath(parent, child):
    """ 
    Calculates the absolute path given the parent dir 
    and child
    
    Arguments:-
        parent: path to the parent dir 
        child: sub-dir or file
    
    Returns: the absolute path
    """
    if parent[-1] == "/":
        return parent + child
    else:
        return parent + "/" + child

def is_module(fileleaf):
    """
    Determines whether a FileLeaf obj represents a 
    python module
    
    Arguments:-
        fileleaf: a FileLeaf object
    
    Returns: (True| False)
    """
    return fileleaf.path[-3:] == ".py"

