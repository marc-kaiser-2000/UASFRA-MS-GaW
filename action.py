class Action:
    def __init__(self,id,name,costs,color):
        self.id = id
        self.name = name
        self.costs = costs
        self.p = 0.25
        self.color = color

    def print(self):
        print("ID: "+ str(self.id) + " Name: "+ self.name + ", ")
