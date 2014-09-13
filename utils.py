"""
This module contains utility functions that perform 
tasks such as checking whether whether a file is a python 
module to getting an absolute path from a relative path.
"""
    
def abspath(parent, child):
    """ 
    Calculates the absolute path given the parent dir 
    and child
    
    Argument:-
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

#TODO: remove
def is_top_head(line):
    """
    Determines whether a line represents the head 
    of a top level entity. Does this by checking
    indentation is 0

    Argument:-
        line: str representing a text line in a module

    Returns: (True|False)
    """
    stripped = line.lstrip()
    return len(stripped) > 0 and len(stripped) == len(line) 

#TODO: remove
def is_closer(line):
    """
    Determines whether a line is a closing entity, in which
    case it should not be treated as a new entity 
    """
    strp = line.strip()
    if strp == '"""' or  strp == "'''" or strp =='[' \
        or strp == 
    
