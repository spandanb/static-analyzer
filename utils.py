

class FileLeaf():
    """Represents a child file.     
    """
    def __init__(self, path):
        self.path = path

    def __str__(self):
        return self.path

    def get_path(self):
        return self.path

class FileTree():
    """Represents a directory hierarchy with children files.     
    """
    def __init__(self, path):
        """
        """
        self.path = path
        self.child_files = []
        self.child_dirs = []

    def __str__(self):
        dirs = map(str, self.child_dirs)
        files = map(str, self.child_files)
        return "{} --> Dirs: {}, Files: {}".format(self.path, dirs, files)
    
    def add_child_file(self, child):
        """Adds a child file"""
        child = FileLeaf(child)
        self.child_files.append(child)
        return child
    
    def add_child_dir(self, child):
        """Adds a child directory"""
        child = FileTree(child)
        self.child_dirs.append(child)
        return child

    def get_path(self):
        return self.path
    
    def traverse(self):
        """
        """
        for d in dirs: 
        pass
    
