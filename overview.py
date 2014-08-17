class Graph():
    pass

class Tree(Graph):
    """
    Represents a directory structure where
    children can be a Tree (sub-directories) or
    a Leaf (file)
    """
    
    def __init__(self, ):
        self.children = ...
    
    def append_children(self, child ):
        self.children.append(child)
    
class Leaf():
    """
    Represents a file in a directory
    """
    def __init__(self, rel_path):
        self.rel_path = rel_path
    




def get_proj_file_tree(rootdir, proj_type):
    """
    Returns a tree representing the entire project.
    The in-order traversal of this tree will generate the graph 
    for the entire project

    @params:
        rootdir- the absolute path to the root directory of the project
            e.x. "/home/user1/some_proj"
        proj_type- the type of project, i.e. language or framework; 
            currently only supports python 2.x
            e.x. python
            
    """
    map proj_type to file_ending
    proj_tree = glob over file_ending
    return proj_tree

def get_proj_graph(proj_tree):
    """
    Returns a queryable graph object constructed from the proj_tree
    """
    for src_file in proj_tree:
        if py_lint(src_file) == INVALID_PYTHON:
            WARN USER
            exit 1
        for directory in tree:
            is_package = check if directory is a package, i.e check if __init__.py exists
            if not is_package : 
                for src_file in directory:
                    for top level entity in src_file:
                        entity_type = distinguish between (objects, object_methods, functions, global_variables) 
            else:
                resolve package/modules into graph

     return graph

def main():
    #Get a tree object representing project
    proj_file_tree = get_proj_file_tree()
    
    #Navigate through the tree and determine a subtree
    #   representing the module, sub-module tree
    #I.e. look 
    
    


