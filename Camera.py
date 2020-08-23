import math
from Utils import V2
from Utils import Rectangle



class Camera():

    def __init__(self, viewWidth, viewHeight):
        self.width = viewWidth
        self.height = viewHeight
        self.position = V2(0,0)
        self.borderChar = "#"
        self.rect = Rectangle( V2( self.position.x - math.floor(self.width/2), self.position.y + math.floor(self.height/2)),  V2( self.position.x + math.floor(self.width/2), self.position.y - math.floor(self.height/2)))

    def Update(self, playerPosition):
        self.position = playerPosition
        self.rect = Rectangle( V2( self.position.x - math.floor(self.width/2), self.position.y + math.floor(self.height/2)),  V2( self.position.x + math.floor(self.width/2), self.position.y - math.floor(self.height/2)))