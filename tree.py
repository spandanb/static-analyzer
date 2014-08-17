class Tree():
    def __init__(self, children, data):
        self.children = children
        self.data = data 

    def __str__(self):
        """
        Pre-order traversal print
        """
        str_rep = str(self.data)
        for child in self.children:
            str_rep += child.__str__()
        return str_rep    

    def get_children(self):
        return self.children

    def set_children(self, children):
        self.children = children
    
    def get_data(self):
        return self.data

    def set_data(self, data):
        self.data = data


    


class Leaf():
    def __init__(self, data):
        self.data = data
    
    def __str__(self):
        return self.data

    def get_data(self):
        return self.data

    def set_data(self, data):
        self.data = data
        


