class Variable:
    def __init__(self, name: str, value = None):
        self.name = name
        self.value = value

class Group:
    def __init__(self, variables = []):
        self.variables = variables
    
    def add_variable(self, variable):
        self.variables.append(variable)
    
    def to_dict(self):
        toDict = {}
        for i in self.variables:
            toDict[i.name] = i.value
        return toDict
    
    def __getattr__(self, name):
        if name == 'variables':
            return self.variables
        elif name in [i.name for i in self.variables]:
            return [i for i in self.variables if i.name == name][0]
        else:
            raise AttributeError(f"Not Known property of Group: {name}")
    
    def __repr__(self):
        return 'GROUP DATA:' + '\n' + '\n'.join([f"\t{i.name} = {i.value}" for i in self.variables])