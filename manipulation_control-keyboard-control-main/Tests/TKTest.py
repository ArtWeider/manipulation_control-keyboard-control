class Point():
    x = 0
    y = 0
    z = 0

    var1 = 1
    var2 = 2

    def __init__(self, x, y, z):

        self.x = x
        self.y = y
        self.z = z

        self.var1 = self.x + self.z

def CreatePoints():
    for i in range(10):



dict = {"1 2 3": Point(1, 2, 3), "1 2 4": Point(1, 2, 4)}

print(dict["1 2 4"].var1)