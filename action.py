class Action:
    def __init__(self,id,name,costs):
        self.id = id
        self.name = name
        self.costs = costs
        self.p = 0.25

    def print(self):
        print("ID: "+ str(self.id) + " Name: "+ self.name + ", ")


