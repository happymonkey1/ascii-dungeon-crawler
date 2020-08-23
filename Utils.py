import math

class V2():
    def __init__(self, x, y):
        self.x = x
        self.y = y

class Rectangle():

    def __init__(self, bottomLeft:V2, topRight:V2):
        self.bottomLeft = bottomLeft
        self.topRight = topRight
    
    def DoesIntersect(self, other):
        #return self.topRight.x>=other.topRight.x>=self.bottomLeft.x and self.topRight.x>=other.bottomLeft.x>=self.bottomLeft.x and self.topRight.y>=other.topRight.y>=self.bottomLeft.y and self.topRight.x>=other.bottomLeft.x>=self.bottomLeft.x

        if(self.bottomLeft.x > other.topRight.x or other.bottomLeft.x >= self.topRight.x): 
            return False
  
        # If one rectangle is above other 
        if(self.bottomLeft.y < other.topRight.y or other.bottomLeft.y <= self.topRight.y): 
            return False
  
        
        return True

    def GetIntersection(self, other):
        x1 = max(self.bottomLeft.x, other.bottomLeft.x)
        y1 = min(self.bottomLeft.y, other.bottomLeft.y)
        x2 =  min(self.topRight.x, other.topRight.x)
        y2 = max(self.topRight.y, other.topRight.y)
        return Rectangle(V2(x1, y1), V2(x2, y2))