"""
This module contains the functions and classes that analyze
the code or directly help in the analysis.
"""
import ast
import tree
import consts
import pprint

"""
Create an intra connection graph that maps how functions and other entities,
declared within the module are used/modified within the module
Use entity table to keep track of top level entities

functional analysis:- treat everything as a black box
    with an input and output.
    Try and infer types of these
    
Then do same analysis between modules

"""
def create_intraconn_graph(module):
    """
    Creates graph that maps connections
    within module
    """
    pass

def create_interconnection_graph(mod_vect):
    """
    Arguments:-
        mod_vect: list of module objects
    
    Returns: an object representing the 
        interconnection between modules
    """
    pass


class NodeVisitor(ast.NodeVisitor):
    def generic_visit(self, node):
        print "In generic_visit"
        print type(node).__name__
        ast.NodeVisitor.generic_visit(self, node)

    def visit_Name(self, node):
        print 'Name :', node.id

    def visit_Num(self, node):
        print 'Num :', node.__dict__['n']

    def visit_Str(self, node):
        print "Str :", node.s

    def visit_Print(self, node):
        print "Print :"
        ast.NodeVisitor.generic_visit(self, node)

    def visit_Assign(self, node):
        print "Assign :"
        ast.NodeVisitor.generic_visit(self, node)

    def visit_Expr(self, node):
        print "Expr :"
        ast.NodeVisitor.generic_visit(self, node)    

class AllNames(ast.NodeVisitor):
    def visit_Module(self, node):
        self.names = set()
        self.generic_visit(node)
        print sorted(self.names)
    def visit_Name(self, node):
        self.names.add(node.id)

class AllNames(ast.NodeVisitor):
    def visit_Module(self, node):
        self.names = set()
        self.generic_visit(node)
        print sorted(self.names)
    def visit_Name(self, node):
        print node.lineno, node.id, node.col_offset
        print node
        print dir(node)
        print " "
        self.names.add(node.id)



def getNode(filename):
    """
    Returns a AST node object corresponding to argument file
    
    Arguments:- filename
        name of file to converted

    Return: AST node object
    """
    f = open(filename, "r")
    lines = "".join(f.readlines())
    f.close()
    
    node = ast.parse(lines)
    return node

def prettyPrint(self_map):
    pprint.pprint(self_map)


def getTopLevelObjs(self_map):
    """
    Returns dict of top level entity types to list of names
    """
    head = lambda double: double[0]
    top_level_objs = {}
    for entity_type, entity_vect  in self_map.iteritems():
        vect = map(head, entity_vect)
        if vect:
            top_level_objs[entity_type] = vect

    return top_level_objs


def getTopLevelObjs2(self_map):
    """
    Returns list of doubles of name and entity types
    """
    head = lambda double: double[0]
    top_level_objs = []
    for entity_type, entity_vect  in self_map.iteritems():
        for entity in entity_vect:
            top_level_objs.append((head(entity), entity_type))
    
    return top_level_objs

node_type = lambda node: node.__class__.__name__

class NodeVisitor(ast.NodeVisitor):
    """Class that implements NodeVisitor functionality
    The methods visit, generic_visit copied from ast.py and
    lightly modified. 
    
    The attributes i.e. name, arg, decorators etc. are 
    properties of the node obj. The attributes vary depending on
    the specific node obj, i.e. a function has an arg, whereas a 
    class does not.
    
    """ 
    def visit(self, node, node_map):
        """Visit a node."""
        node_type = node.__class__.__name__
        method = 'visit_' + node_type 
        visitor = getattr(self, method, self.generic_visit)
        
        """
        If visitor method does not exist, calls generic visit
        i.e. the following statement is either visit_FOO(...) 
        or generic_visit(...)
        """
        return visitor(node, node_map)

    def generic_visit(self, node, node_map):
        """Called if no explicit visitor function exists for a node.
        Does nothing- calls visit on children nodes
        @Args
            node (AST Node)- the AST node to visited
            node_map (dict)- this node's map, contains descendents
        """
        node_type = node.__class__.__name__
        if node_type in consts.AST_NODE_TYPE2: 
           parent_map = node_map
           #Create dict, and add entries on the fly
           # as needed
           node_map = {}
           if not parent_map.has_key(node_type): 
                parent_map[node_type]=[]
           unique_id = getattr(node, "name", node.lineno)
           parent_map[node_type].append((unique_id, node_map))
        
        for field, value in ast.iter_fields(node):
            if isinstance(value, list):
                for item in value:
                    if isinstance(item, ast.AST):
                        self.visit(item, node_map)
            elif isinstance(value, ast.AST):
                self.visit(value, node_map)

#    def visit_Assign(self, node):
#        print("\nIn Assign")
#        print(node.value)
#        self.generic_visit(node)
    
#    def visit_FunctionDef(self, node, parent_map):
#        #name, args, body, decorator_list, returns
#        self_map = getMap()
#        self.generic_visit(node, self_map)
#        parent_map["func"].append((node.name, self_map))
#
#    def visit_ClassDef(self, node, parent_map):
#        print "Heeyah!"
#        nt = node_type(node)
#        self_map = {}
#        self.generic_visit(node, self_map)
#        if not parent_map.has_key(nt): 
#                parent_map[nt]=[]
#        parent_map[nt].append((node.name, self_map))

    def vist_Name(self, node, parent_map):
        nt = node_type(node)
        self_map = {}
        self.generic_visit(node, self_map)
        if not parent_map.has_key(nt): 
                parent_map[nt]=[]
        parent_class[nt].append((node.name, self_map))

def analyze(node):
    self_map = {}
    NodeVisitor().visit(node, self_map)

    # self_map contains the ast represented as a dict 
    print "Module AST is "
    prettyPrint(self_map)
  
    print "Top level entities are: "
    top_map = getTopLevelObjs2(self_map)  
    prettyPrint(top_map)


if __name__ == '__main__':

    #NOTE: consts.AST_NODE_TYPE controls granularity of tree
    node = getNode("test.py") 
    analyze(node)


