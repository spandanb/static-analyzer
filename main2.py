import sys
import os
import os.path
import utils as ut
import argparse
import pylint as pyl



def create_bins(module):
    """
    Creates a dictionary of entity type to lists
    
    Arguments:
        module:- a FileLeaf object representing a py module
    
    Returns: a dictionary of entity type to lists 
    """

    

def create_file_tree(rootdir):
    """Creates a k-tree that takes the dir hierarchy and
    parent-child relationships and turns it into package-module
    and package - sub-package relationship.
    
    Arguments:
        rootdir:- path to rootdir of project being analyzed.
    
    Returns: The file tree
    """
    
    if not os.path.isdir(rootdir):
        error("root is not a dir")
    
    root = ut.FileTree(rootdir)
    pathmap = {}
    ptr =  None
    this = None
    for selfpath, dirs, files in os.walk(rootdir):
        #selfpath is own path
        #dirs is child dirs
        #files is child files
        this = pathmap.get(selfpath, root)
        for d in dirs:
            path = ut.abspath(selfpath, d)
            ptr = this.add_child_dir(path)
            pathmap[path] = ptr
        
        for f in files:
            path = ut.abspath(selfpath, f)
            ptr = this.add_child_file(path)
            pathmap[path] = ptr
            if f == "__init__.py":
                this.set_package(True)
    #print root
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
    for package in proj_file_tree.package_list():
        for module in package.module_list():
            bins = create_bins(module)
#            m = create_module_obj(bins)
