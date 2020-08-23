import builtins
import math
from math import floor
import random


from Camera import Camera
from Utils import V2
from Utils import Rectangle


r1 = ["----------",
      "|........|",
      "|........|",
      "|........|",
      "----------",]

r2 = ["-------------------------------",
      "|.............................|",
      "|.............................|",
      "|.............................|",
      "-------------------------------",]

r3 =   ["--------------",
        "|............|",
        "|............|",
        "|............|",
        "--------------",]

r4 = ["--------------------------",
      "|.........................|",
      "|.........................|",
      "|.........................|",
      "|.........................|",
      "|.........................|",
      "|.........................|",
      "|.........................|",
      "---------------------------",]





class Room():

    def __init__(self, data, pos:V2, id):
        self.width = len(data[0])
        self.height = len(data)
        self.overlay = []
        self.data = self._generateMapData(data)
        self.uniqueRoomID = id
        self.position = pos
        self.rect = Rectangle( V2( self.position.x, self.position.y + self.height ),  V2( self.position.x + self.width, self.position.y ) )
        self._isColliding = False

    def _generateMapData(self, data):
        d = []
        for y in range(self.height):
            self.overlay.append([])
            d.append([])
            for x in range(self.width):
                self.overlay[y].append(0)
                d[y].append(data[y][x])
        
        return d

    def _updatePos(self, x:int, y:int):
        self._updatePosX(x)
        self._updatePosY(y)

    def _updatePosX(self, x:int):
        self.position.x = x
        self.rect = Rectangle( V2( self.position.x, self.position.y + self.height ),  V2( self.position.x + self.width, self.position.y ) )
    
    def _updatePosY(self, y:int):
        self.position.y = y
        self.rect = Rectangle( V2( self.position.x, self.position.y + self.height ),  V2( self.position.x + self.width, self.position.y ) )



class LevelGenerator():

    def __init__(self):
        self.rooms = []

    def GetCurrentMapData(self) -> list(list()):
        return self.culledMapData
    def GetRandomPointInCircle(self, radius) -> V2:
        t = 2*math.pi*random.random()
        u = random.random()+random.random()
        r = 0
        if u > 1:
            r = 2-u 
        else: 
            r = u
        return V2(round(radius*r*math.cos(t)), round(radius*r*math.sin(t)))

    
    def GenerateStartingRooms(self, numRooms, rad, roomSpacing:int):
        for i in range(numRooms):
            self.rooms.append(Room(random.choice([r1, r2, r3, r4]), self.GetRandomPointInCircle(rad), i))

        g._bounceRooms(roomSpacing)

    def _bounceRooms(self, bounceAmount:int):
        colRooms = 1
        iter = 1
        while colRooms > 0:
            print(iter)
            iter += 1
            for room in self.rooms:
                col = False
                for otherRoom in self.rooms:
                    if room.uniqueRoomID != otherRoom.uniqueRoomID:
                        if room.rect.DoesIntersect(otherRoom.rect):
                            absDX = abs(room.position.x - otherRoom.position.x)
                            absDY = abs(room.position.y - otherRoom.position.y)
                            if absDX >= absDY:
                                room._updatePosX( room.position.x + bounceAmount if room.position.x > otherRoom.position.x else room.position.x - bounceAmount )
                                otherRoom._updatePosX( otherRoom.position.x - bounceAmount if room.position.x > otherRoom.position.x else otherRoom.position.x + bounceAmount )
                                col = True
                            else:
                                room._updatePosY( room.position.y + bounceAmount if room.position.y > otherRoom.position.y else room.position.y - bounceAmount )
                                otherRoom._updatePosY( otherRoom.position.y - bounceAmount if room.position.y > otherRoom.position.y else otherRoom.position.y + bounceAmount )
                                col = True

                        '''
                        absDX = abs(room.position.x - otherRoom.position.x)
                        absDY = abs(room.position.y - otherRoom.position.y)
                        if absDX < min(room.width, otherRoom.width):
                            room.position.x = room.position.x + bounceAmount if room.position.x > otherRoom.position.x else room.position.x - bounceAmount
                            otherRoom.position.x = otherRoom.position.x - bounceAmount if room.position.x > otherRoom.position.x else otherRoom.position.x + bounceAmount
                            col = True
                        elif absDY < min(room.height, otherRoom.height):
                            room.position.y = room.position.y + bounceAmount if room.position.y > otherRoom.position.y else room.position.y - bounceAmount
                            otherRoom.position.y = otherRoom.position.y - bounceAmount if room.position.y > otherRoom.position.y else otherRoom.position.y + bounceAmount
                            col = True
                        '''

                room._isColliding = col
                        
            colRooms = 0
            for room in self.rooms:
                if room._isColliding == True:
                    colRooms += 1

        for room in self.rooms:
            print(room.position.x, room.position.y)

    def _getDrawRoomData(self, camera):

        roomsToRender = []
        intersectionData = []
        for i in range(len(self.rooms)):
            room = self.rooms[i]
            if room.rect.DoesIntersect(camera.rect):
                intersection = room.rect.GetIntersection(camera.rect)
                roomsToRender.append(room)
                intersectionData.append(intersection)

        mapToRender = []
        rowData = []

        #create border data
        for i in range(camera.width+2):
            rowData.append(camera.borderChar)

        #add border after last row
        mapToRender.append(rowData) 
        col = 1
        row = 0
        for y in range(camera.rect.topRight.y, camera.rect.bottomLeft.y + 1):
            mapToRender.append([])
            for x in range(camera.rect.bottomLeft.x-1, camera.rect.topRight.x + 2):
                if x == camera.rect.bottomLeft.x-1:
                    mapToRender[col].append(camera.borderChar)
                    continue
                elif x == camera.rect.topRight.x + 1:
                    mapToRender[col].append(camera.borderChar)
                    continue

                foundRoom = False
                for i in range(len(intersectionData)):
                    intersectedRoom = intersectionData[i]
                    if y <= intersectedRoom.bottomLeft.y and intersectedRoom.topRight.y <= y and x >= intersectedRoom.bottomLeft.x and x <= intersectedRoom.topRight.x:
                        topLeftX = intersectedRoom.bottomLeft.x
                        topLeftY = intersectedRoom.topRight.y
                        
                        
                        roomY = y - topLeftY
                        if roomY >= len(roomsToRender[i].data):
                            break

                        roomX = x - topLeftX
                        if roomX >= len(roomsToRender[i].data[roomY]):
                            break
                            
                        mapToRender[col].append(roomsToRender[i].data[roomY][roomX])
                        foundRoom = True
                        row += 1
                        break
                
                if not foundRoom:
                    mapToRender[col].append(" ")

                

            row = 0
            col += 1
        
        #add border after last row
        mapToRender.append(rowData)
        return mapToRender
                    

    def DrawRooms(self, cam:Camera):
        mapToRender = g._getDrawRoomData(cam)
        for y in range(len(mapToRender)):
            builtRow = ""
            for x in range(len(mapToRender[y])):
                builtRow += mapToRender[y][x]
            print(builtRow)

        self.culledMapData = mapToRender



if __name__ == "__main__":
    g = LevelGenerator()
    g.GenerateStartingRooms(5, 5, 1)
    

    cam = Camera(49, 11)
    
    playerPos = V2(0,0)

    cam.Update(playerPos)
    #g.DrawRooms(cam)
    
    
    while True:
        g.DrawRooms(cam)

        move = input()
        s = 5
        if move == "w":
            playerPos.y -= 1 * s
        elif move == "s":
            playerPos.y += 1 * s
        elif move == "a":
            playerPos.x -= 1 * s
        elif move == "d":
            playerPos.x += 1 * s
        
        cam.Update(playerPos)

        


    