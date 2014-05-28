import pyglet
import shelve
import simplifiedDrawing

#constants
mousePlacementRange = 64

maxScaleFactor = 1
minScaleFactor = 0.25

fps = 60

saveFile = "test"

scaleChangeFactor = 2


class GameVariables(object):
    #This class allows for easy manipulation of game variables without the use of the global function.
    def __init__(self, tileSize, windowWidth, windowHeight, mouseCompensation, spriteScaleFactor):
        self.tileSize = tileSize

        self.windowWidth = windowWidth
        self.windowHeight = windowHeight

        self.mouseCompensation = mouseCompensation
        self.spriteScaleFactor = spriteScaleFactor

        self.screenLocalX = 0  #x distance from origin of level editor screen
        self.screenLocalY = 0  #y distance from origin of level editor screen


class ButtonMaps(object):
    def __init__(self, key_ZoomIn, key_ZoomOut, key_SidebarScrollUp, key_SidebarScrollDown):
        self.key_ZoomIn = key_ZoomIn
        self.key_ZoomOut = key_ZoomOut
        self.key_SidebarScrollUp = key_SidebarScrollUp
        self.key_SidebarScrollDown = key_SidebarScrollDown

gameVariables = GameVariables(32, 1025, 600, 16, 1)


#These are images to be loaded
imgDebug = pyglet.image.load("resources/debug.png")
imgButtonWall = pyglet.image.load("resources/gui/buttonWall.png")
imgButtonWallPressed = pyglet.image.load("resources/gui/buttonWallPressed.png")
imgButtonSave = pyglet.image.load("resources/gui/buttonSave.png")
imgButtonSavePressed = pyglet.image.load("resources/gui/buttonSavePressed.png")


#pyglet variables
window = pyglet.window.Window(gameVariables.windowWidth, gameVariables.windowHeight)


#library-based pointer variables
button = gui.Button


#miscellaneous
shelf = shelve.open(saveFile, writeback=True)

buttons = []
objects = []


class SavingTile(object):
    def __init__(self, x, y, imagePath):
        self.x = x
        self.y = y

        self.imagePath = imagePath


def buttonWall():
    #This function is a temporary function designed to represent the future ability to create blocks with buttons.
    #the sprites must be scaled before they are appended (and drawn).
    newObj = DWall()
    newObj.sprite.scale = gameVariables.spriteScaleFactor
    objects.append(newObj)


def buttonFunctionSave():
    savingObjects = []

    for gameObject in objects:
        savingObjects.append(SavingTile(gameObject.sprite.x, gameObject.sprite.y, gameObject.imagePath))

    shelf["objects"] = savingObjects

    shelf.sync()


#add buttons
buttons.append(button(imgButtonWall, imgButtonWallPressed, 64, 64, (32, 32), function=buttonWall))
buttons.append(button(imgButtonSave, imgButtonSavePressed, 64, 64, (32, 256), function=buttonFunctionSave))


#debug/testing variables
class DWall(object):
    def __init__(self):
        self.sprite = pyglet.sprite.Sprite(imgDebug, -10, -10)
        self.imagePath = "resources/debug.png"

        self.globalX = -10
        self.globalY = -10

        self.selected = True
        
    def updateClick(self, mouseX, mouseY):
        if self.selected:
            #If the wall is not yet placed, move it to a point on the grid closest to the mouse
            self.sprite.x = int(gameVariables.tileSize * round(float(mouseX - gameVariables.mouseCompensation)
                                                               / gameVariables.tileSize))
            self.sprite.y = int(gameVariables.tileSize * round(float(mouseY - gameVariables.mouseCompensation)
                                                               / gameVariables.tileSize))

            self.globalX = self.sprite.x/gameVariables.tileSize
            self.globalY = (self.sprite.y+mousePlacementRange) / gameVariables.tileSize - (mousePlacementRange * 2 /
                                                                                           gameVariables.tileSize)


    def update(self):
            self.sprite.x = self.globalX*gameVariables.tileSize
            self.sprite.y = self.globalY*gameVariables.tileSize+mousePlacementRange

    def draw(self):
        self.sprite.draw()


@window.event
def on_draw():
    window.clear()

    for guiButton in buttons:
        guiButton.draw()

    for gameObject in objects:
        gameObject.draw()

    for lineX in range(0, int(gameVariables.windowWidth / gameVariables.tileSize)):
        #Draw a line up-down
        simplifiedDrawing.drawLine(20, 20, 20, lineX * gameVariables.tileSize, mousePlacementRange,
                                   lineX * gameVariables.tileSize, gameVariables.windowHeight)

    for lineY in range(0, int(gameVariables.windowHeight / gameVariables.tileSize)):
        #Draw a line left-right
        if lineY * gameVariables.tileSize > mousePlacementRange - 1:
            simplifiedDrawing.drawLine(20, 20, 20, 0, lineY * gameVariables.tileSize, gameVariables.windowWidth,
                                       lineY * gameVariables.tileSize)


@window.event 
def on_mouse_press(x, y, buttonPressed, modifiers):
    if buttonPressed == pyglet.window.mouse.LEFT:
        for guiButton in buttons:
            guiButton.update(x, y)

        if y > mousePlacementRange:
            for gameObject in objects:
                if gameObject.selected:
                    buttonWall()
                    gameObject.selected = False
                    break

    elif buttonPressed == pyglet.window.mouse.RIGHT:
        for idx, val in enumerate(objects):
            if val.selected == False:
                if val.sprite.x == int(gameVariables.tileSize * round(float(x - gameVariables.mouseCompensation)
                                                                   / gameVariables.tileSize)):
                    if val.sprite.y == int(gameVariables.tileSize * round(float(y - gameVariables.mouseCompensation)
                                                                   / gameVariables.tileSize)):
                        objects.remove(val)
            

@window.event        
def on_mouse_release(x, y, buttonPressed, modifiers):
    if buttonPressed == pyglet.window.mouse.LEFT:
        for guiButton in buttons:
            guiButton.mouseRelease()


@window.event
def on_mouse_motion(x, y, dx, dy):
    for gameObject in objects:
        gameObject.updateClick(x, y)


@window.event
def on_key_press(symbol, mods):
    if symbol == pyglet.window.key.MINUS or symbol == pyglet.window.key.NUM_SUBTRACT:
        if gameVariables.spriteScaleFactor > minScaleFactor:

            for gameObject in objects:
                gameObject.sprite.scale /= scaleChangeFactor
            gameVariables.spriteScaleFactor /= scaleChangeFactor

            gameVariables.tileSize /= scaleChangeFactor
            gameVariables.tileSize = int(gameVariables.tileSize)

            print(str(gameVariables.tileSize))

            gameVariables.mouseCompensation /= scaleChangeFactor

    elif symbol == pyglet.window.key.EQUAL or symbol == pyglet.window.key.NUM_ADD:
            if gameVariables.spriteScaleFactor < maxScaleFactor:
                for gameObject in objects:
                    gameObject.sprite.scale *= scaleChangeFactor
                gameVariables.spriteScaleFactor *= scaleChangeFactor

                gameVariables.tileSize *= scaleChangeFactor
                gameVariables.tileSize = int(gameVariables.tileSize)

                print(str(gameVariables.tileSize))

                gameVariables.mouseCompensation *= scaleChangeFactor
            print(str(gameVariables.tileSize))

def timeUpdate(dt):
    for gameObject in objects:
        gameObject.update()

pyglet.clock.schedule_interval(timeUpdate, 1/fps)

pyglet.app.run()

'''
Changes still needed to be made:

- Error checking
- Deleting
- Height and Width proper so lines look good
- customisable line colour (definitely in future)
- button only creates a block if there is none selected (if a block is already being placed, do not create a second
block with the button
- Types of tile/block types instead of buttons ('obstacles'-'water') for example
- Move save button
- proper images
- ability to change width and height of map
- ability to change background colour of map
- ability to fill all empty grid squares with a particular type of block (probably will be a little bit lagging)
- putting one type of block over another deletes the previous block
- attempting to place the same type of block on top of each other does nothing.
- customisable level variables; wind direction/speed, etc
- mouse placement (int(gameVariables.tileSize * round(float(mouseX - gameVariables.mouseCompensation)
                                                               / gameVariables.tileSize))) code MUST be put in a
                                                               function and replaced at all necessary locations.
- selected (not yet placed) blocks must be transparent so you can see if you've deleted the underlying block
'''