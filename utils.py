
class FileLeaf():
    """Represents a child file.     
    """
    def __init__(self, path):
        self.path = path

    def __str__(self):
        return self.path

    def get_path(self):
        return self.path

#TODO: project/package object inherits from FileTree?
class FileTree():
    """Represents a directory hierarchy with children files.     
    """
    def __init__(self, path):
        """
        """
        self.path = path
        self.child_files = []
        self.child_dirs = []
        self.is_package = False

    def __str__(self):
        #dirs = map(str, self.child_dirs)
        #files = map(str, self.child_files)
        #return "{} --> Dirs: {}, Files: {}".format(self.path, dirs, files)
        return "{}".format(self.path)
   
    def __repr__(self):
        return "{}".format(self.path)


    def add_child_file(self, child):
        """Adds a child file"""
        child = FileLeaf(child)
        self.child_files.append(child)
        #print "self.path is {}, child is {}".format(self.path, child.path)
        return child
    
    def add_child_dir(self, child):
        """Adds a child directory"""
        child = FileTree(child)
        self.child_dirs.append(child)
        #print "self.path is {}, child is {}".format(self.path, child.path)
        return child

    def get_path(self):
        return self.path
    
    def set_package(self, is_package):
        """
        Sets whether directory is package
        
        Arguments:-
            is_package: (True|False)
        """
        self.is_package = is_package
    
    def package_list(self):
        """Iterate over list of python packages"""
        #TODO: turn into iterator?
        packages = []
        if self.is_package:
            #Append package
            packages.append(self)
        for d in self.child_dirs:
            #Append child sub-packages
            child_package_list = d.package_list()
            if child_package_list: 
                packages += child_package_list
        return packages
    
    def module_list(self):
        """Iterate over list of python modules in this package"""
        #TODO: turn into iterator?
        if not self.is_package:
            return None
        else:
            modules = []
            for f in self.child_files: 
                if is_module(f):
                    modules.append(f)
            return modules

    
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
