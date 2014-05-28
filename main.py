import pyglet
import engine

window = pyglet.window.Window(640, 480)
colours = engine.Colours()

imgtest = pyglet.image.load("debug.png")
player = engine.Player(imgtest, 0.098, colours.red)
tiles = [engine.Block(50,50,colours.red,imgtest), engine.Block(50,100,colours.red,imgtest)]
paint = [engine.Paint(200,200,colours.blue,imgtest,imgtest)]
keys = pyglet.window.key.KeyStateHandler()
window.push_handlers(keys)

@window.event
def on_draw():
    window.clear()
    for tile in tiles:
        tile.on_draw()
    player.on_draw()
    for pain in paint:
        pain.on_draw()

@window.event
def on_key_press(key, mods):
    player.on_key_press(key)

@window.event
def on_key_release(key, mods):
    player.on_key_release(key)

def update(dt):
    player.on_update(tiles, paint)

pyglet.clock.schedule_interval(update,1/60)

pyglet.app.run()