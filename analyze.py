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


def get_node(filename):
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

def pretty_print(self_map):
    pprint.pprint(self_map)

def unique_id(node):
    """
    Returns progressively less informative identifiers
    """
    return getattr(node, "name", 
            getattr(node, "id",
                getattr(node, "lineno", 
                    id(node) 
                )
            )
        )

def check_is_literal(node):
    """
    Checks if node represents a literal.
    If literal, return value else returns original 
    """
    tp = type(node) 
    if tp == ast.Str:
        return ("LITERAL-STR", node.s)
    elif tp == ast.Num:
        return ("LITERAL-NUM", node.n)
    else: 
        return node

def get_top_level_objs(self_map):
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

def get_top_level_objs2(self_map):
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
        ntype = node_type(node)
        if ntype in consts.AST_NODE_TYPE2: 
           parent_map = node_map
           node_map = {}
           if not parent_map.has_key(ntype): 
                parent_map[ntype]=[]
           parent_map[ntype].append((unique_id(node), node_map))
        
        for field, value in ast.iter_fields(node):
            if isinstance(value, list):
                for item in value:
                    if isinstance(item, ast.AST):
                        self.visit(item, node_map)
            elif isinstance(value, ast.AST):
                self.visit(value, node_map)

    def gvisit(self, node, parent_map): 
        """generic visit function """
        ntype = node_type(node)
        self_map = {}
        #All descendent info is in self_map
        self.generic_visit(node, self_map)
        #Create dict, and add entries on the fly as needed
        #TODO: Create a new data type that can do the following 
        #check and insert in one shot
        if not parent_map.has_key(ntype): 
                parent_map[ntype]=[]
        #Append your info in your parent's map        
        parent_map[ntype].append((unique_id(node), self_map))

    def visit_Import(self, node, parent_map):
        """
        Needed because alias is a list and unique id does
        give it the appropriate name
        """
        #TODO: handle other types of imports
        for alias in node.names:
            ntype = node_type(node)
            self_map = {}
            self.generic_visit(node, self_map)
            if not parent_map.has_key(ntype): 
                    parent_map[ntype]=[]
            parent_map[ntype].append((alias.name, self_map))

#    def visit_FunctionDef(self, node, parent_map):
#        #name, args, body, decorator_list, returns
#        self_map = getMap()
#        self.generic_visit(node, self_map)
#        parent_map["func"].append((node.name, self_map))
#
    
#    def visit_ClassDef(self, node, parent_map):
#        nt = node_type(node)
#        self_map = {}
#        self.generic_visit(node, self_map)
#        if not parent_map.has_key(nt): 
#                parent_map[nt]=[]
#        parent_map[nt].append((node.name, self_map))

    """
    Example usage: a=1
    Assign(targets=[
        Name(id='a', ctx=Store()),
                   ], value=Num(n=1)),
     ])
    """

    def visit_Assign(self, node, parent_map):
        #assignments typically have the form: targets = value
        #First, Get the value 
        value = None
        #Holds the attr of a call object
        attr = None
        if node_type(node.value) == "Name":
            value = node.value.id
            #print "Name: value is {}".format(value)   
            #self.visit_Name2(node.value)
        
        elif node_type(node.value) == "Call":
            value = node.value.func
            #print "Call: value is {} {}".format(value, type(value))  
            if type(value) == ast.Attribute:
                #print "Call value, ctx is {} {}".format(value.value, value.attr)
                attr = value.attr
                value = value.value 
            #can't use elif since might neeed to go into both conditions
            if type(value) == ast.Name:
                #print "value.id is {}".format(value.id)
                value = value.id
            #print "value is {}".format(value)
            
            #Check for Literals
            value = check_is_literal(value)
    
        #Then create a mapping 
        if value != None:
            for target in node.targets:
                if node_type(target) == "Name":
                    if "Name" not in parent_map:
                        parent_map["Name"] = []
                    if attr: 
                        tpl = (target.id, value, attr)
                    else:
                        tpl = (target.id,value)
                    parent_map["Name"].append(tpl)
                    

        #print node.targets, node.value, node_type(node.value)
        #self.gvisit(node, parent_map)
    
    def visit_Name2(self, node, parent_map):
        #ctx, id
        #print "In Name"
        print "ID is: {}. ctx is {}.".format(node.id, node.ctx)
        #self.gvisit(node, parent_map)

#    def visit_Load(self, node, parent_map):
#        self.gvisit(node, parent_map)
#
#    def visit_Store(self, node, parent_map):
#        self.gvisit(node, parent_map)

    def visit_Call(self, node, parent_map):
        #func, function name of called
        pass

def analyze(node):
    self_map = {}
    NodeVisitor().visit(node, self_map)

    # self_map contains the ast represented as a dict 
    print "Module AST is "
    pretty_print(self_map)
  
    print "Top level entities are: "
    top_map = get_top_level_objs2(self_map)  
    pretty_print(top_map)


if __name__ == '__main__':

    #NOTE: consts.AST_NODE_TYPE controls granularity of tree
    node = get_node("test.py") 
    analyze(node)


