import pyglet
import math

def drawLine(colour1, colour2, colour3, x1, y1, x2, y2):
    pyglet.gl.glColor4f(colour1, colour2, colour3, 1.0) 
    pyglet.graphics.draw(2, pyglet.gl.GL_LINES, ('v2i', (x1, y1, x2, 
y2))) 