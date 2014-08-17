import pylint.lint as pyl
import sys
import os.path
import os
from tree import Tree

def call_pylint(filename):
    """
    runs pylint and see package files are error free
    """
    pyl.lint(filename)
    #Run(['--errors-only', 'myfile.py']) 


def get_proj_file_tree(root):
    """
    Returns a tree representing the entire project.
    The in-order traversal of this tree will generate the graph 
    for the entire project

    @params:
        root- the absolute path to the root directory of the project
            e.x. "/home/user1/some_proj"
            
    """
    if not os.path.isdir(root):
        print "root is not a dir"
        sys.exit(1)
    
    #root_ptr = Tree()
    ptr = {}
    for subdir, dirs, files in os.walk(root):
        #subdir is own path
        #dirs is child dirs
        #files is child files
        
        #for file in files:
        #        print subdir+'/'+file
       
        ptr[subdir] = files
    
    print ptr.keys() 


if __name__ == "__main__":
    #TODO: Get path to package from CL arg
    t_data = "/Users/spandan/Documents/pproj/stat/test_data/"
    #path ="/Users/spandan/Documents/pproj/stat/test_data/requests/requests"
    path = t_data + "tst"

    #TODO: call pylint and check for errors
    #call_pylint(path)
    
    #Checks whether path exists
    if not os.path.exists(path):
        sys.exit(1)
        print "Path {} does not exists".format(path)

    #FIX: should also accept path to single file,
    #   for now assumes path is to a package

    pkg_tree = get_proj_file_tree(path)

    
