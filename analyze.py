"""
This module contains the functions and classes that analyze
the code or directly help in the analysis.
"""
import ast
import tree


def prnt(obj, spaces):
    if type(obj) != str:
        obj = str(obj)
    norm_spaces = spaces + len(obj) * 2
    print(obj.rjust(norm_spaces))

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

nodeTypes = ["Num", "Str", "Bytes", "List", "Tuple", "Set", "Dict", "Ellipsis", "NameConstant", "Name", "Load", "Store", "Del", "Starred", "Expr", "UnaryOp", "UAdd", "USub", "Not", "Invert", "BinOp", "Add", "Sub", "Mult", "Div", "FloorDiv", "Mod", "Pow", "LShift", "RShift", "BitOr", "BitXor", "BitAnd", "BoolOp", "And", "Or", "Compare", "Eq", "NotEq", "Lt", "LtE", "Gt", "GtE", "Is", "IsNot", "In", "NotIn", "Call", "keyword", "IfExp", "Attribute", "Subscript", "Index", "Slice", "ExtSlice", "ListComp", "SetComp", "GeneratorExp", "DictComp", "comprehension", "Assign", "AugAssign", "Print", "Raise", "Assert", "Delete", "Pass", "Import", "ImportFrom", "alias", "If", "For", "While", "Break", "Continue", "Try", "TryFinally", "TryExcept", "ExceptHandler", "With", "FunctionDef", "Lambda", "arguments", "arg", "Return", "Yield", "YieldFrom", "Global", "Nonlocal", "ClassDef"]  

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


def getMap():
    """
    return a dictionary that holds lists of various entity types
    """
    return {"func":[], "class":[], "module":[]}


class Func(ast.NodeVisitor):
    """Copied from ast.py""" 
    def visit(self, node, node_map):
        """Visit a node."""
        method = 'visit_' + node.__class__.__name__
        visitor = getattr(self, method, self.generic_visit)
        """
        If visitor method does not exist, calls generic visit
        """
        return visitor(node, node_map)

    def generic_visit(self, node, node_map):
        """Called if no explicit visitor function exists for a node."""
        for field, value in ast.iter_fields(node):
            if isinstance(value, list):
                for item in value:
                    if isinstance(item, ast.AST):
                        self.visit(item, node_map)
            elif isinstance(value, ast.AST):
                self.visit(value, node_map)

    def scoped_visit(self, node, node_map):
        """Called if no explicit visitor function exists for a node."""
        ret_vector = []
        for field, value in ast.iter_fields(node):
            if isinstance(value, list):
                for item in value:
                    if isinstance(item, ast.AST):
                        ret_vector.append(self.visit(item, node_map))
            elif isinstance(value, ast.AST):
                ret_vector.append(self.visit(value, node_map))
        #return ret_vector

    """
    The attributes i.e. name, arg, decorators etc are 
    properties of the node obj
    """
#    def visit_Assign(self, node):
#        print("\nIn Assign")
#        print(node.value)
#        self.generic_visit(node)
    
    def visit_FunctionDef(self, node, parent_map):
        #name, args, body, decorator_list, returns
        #self.func_list.append(node.name) 
        parent_map["func"].append(node.name)
        #self.generic_visit(node)
        #return node.name

    def visit_ClassDef(self, node, parent_map):
        #self.class_list.append(node.name)
        self_map = getMap()
        self.scoped_visit(node, self_map)
        parent_map["class"].append((node.name, self_map))

    def visit_Module(self, node, parent_map):
        #All the classes
        #self.class_list = [] 
        #All the functions
        #self.func_list = []
        self_map = getMap()
        self.scoped_visit(node, self_map)
        #print self.class_list
        #print self.func_list
        parent_map["module"].append(("MODULE", self_map))


#    def visit_Module(self, node):
#        for fieldname, value in ast.iter_fields(node):
#            print fieldname, value.id


class MyNodeVisitor(ast.NodeVisitor):
    pass


def getNode(filename):
    f = open(filename, "r")
    lines = "".join(f.readlines())
    f.close()
    
    node = ast.parse(lines)
    return node

def analyze1(node):
    #v = NodeVisitor()
    v = AllNames()
    v.visit(node)

def analyze2(node):
  self_map = getMap()
  Func().visit(node, self_map)
  print self_map

def analyze3(node):
    for i in ast.walk(node): 
        print dir(i)

def analyze4(node):
    for node in ast.walk(node):
        if isinstance(node, ast.FunctionDef):
                print(node.name)

class X():
    pass

def hello(self):
    print "hello"
setattr(X, "hellow", hello)

if __name__ == '__main__':

    node = getNode("test.py") 
    analyze2(node)


    #x= X()
    #x.hellow()
