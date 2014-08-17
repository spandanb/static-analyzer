import sys
import os
import os.path
import utils as ut
import argparse
import pylint as pyl


def create_file_tree(rootdir):
    """Creates and returns k-tree that represents the dir hierarchy and
    parent child relationships. Very similar to 
    
    Arguments:
        rootdir:- path to rootdir of project being analyzed.
    """
    
    if not os.path.isdir(rootdir):
        error("root is not a dir")
    
    root = ut.FileTree(rootdir)
    pathmap = {}
    ptr =  None
    this = None
    for selfpath, dirs, files in os.walk(rootdir):
        #this is own path
        #dirs is child dirs
        #files is child files
        this = pathmap.get(selfpath, root)
        for d in dirs:
            path = selfpath + '/' + d
            ptr = this.add_child_dir(path)
            pathmap[path] = ptr
        
        for f in files:
            path = selfpath + '/' + f
            ptr = this.add_child_file(path)
            pathmap[path] = ptr
    
    print root
    return root

def error(msg, errno=-1):
    """Reports error message and exits program
    """
    print "Error: {}".format(msg)
    sys.exit(errno)
    
def sanity_check(rootdir):
    """ Checks whether project passes pylint
    """
    pyl.lint(rootdir)

if __name__ == '__main__':
    #Create argument parser
    parser = argparse.ArgumentParser()
    parser.add_argument("rootdir", help="Root directory location of project to be analyzed") #positional argument
    args = parser.parse_args()
    
    #Error checking
    rootdir = args.rootdir
    if not rootdir or not os.path.exists(rootdir):
        error("Please specify a valid root dir!")
    
    #TODO: Check pylint usage
    #if not sanity_check(rootdir):
    #   error("Sanity check failed")
    
    #"/Users/spandan/Documents/pproj/stat/test_data/tst"
    
    proj_file_tree = create_file_tree(rootdir)
