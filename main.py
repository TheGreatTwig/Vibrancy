import pyglet
import engine

#TODO: Use dt in update.

window = pyglet.window.Window(640, 480)

imgtest = pyglet.image.load("debug.png")
player = pyglet.sprite.Sprite(imgtest, 80, 80)
mvm = engine.Vector(0,3)

@window.event
def on_draw():
    window.clear()
    player.draw()

def update(dt):
    player.x, player.y =  mvm.add_to_point(player.x, player.y)

pyglet.clock.schedule_interval(update,1/60)

pyglet.app.run()