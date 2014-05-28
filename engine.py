#TODO: Add a rectangle (block) class. Has properties x y colour.
#TODO: Add player
import pyglet


class _Colour(object):
    def __init__(self, name, r, g, b):
        self.name = name
        self.tuple_colour = (r, g, b)


class Colours(object):
    def __init__(self):
        self.red = _Colour("red", 255, 0, 0)
        self.blue = _Colour("blue", 0, 0, 255)
        self.green = _Colour("green", 0, 255, 0)


class Block(object):
    def __init__(self, x, y, colour, image):
        self.sprite = pyglet.sprite.Sprite(image, x, y)
        self.colour = colour
        self.sprite.color = self.colour.tuple_colour

    def on_draw(self):
        self.sprite.draw()

    def on_collision(self, other_x, other_y, other_height, other_width):

        if other_x >= self.sprite.width+self.sprite.x:
            return False
        elif other_width+other_x <= self.sprite.x:
            return False
        elif other_y >= self.sprite.height+self.sprite.y:
            return False
        elif other_height+other_y <= self.sprite.y:
            return False
        else:
            return True


class _PaintBlock(object):
    def __init__(self, x, y, colour, image):
        self.sprite = pyglet.sprite.Sprite(image, x, y)
        self.colour = colour
        self.sprite.color = self.colour.tuple_colour

    def on_draw(self):
        self.sprite.draw()

    def on_collision(self, other_x, other_y, other_height, other_width):

        if other_x >= self.sprite.width+self.sprite.x:
            return False
        elif other_width+other_x <= self.sprite.x:
            return False
        elif other_y >= self.sprite.height+self.sprite.y:
            return False
        elif other_height+other_y <= self.sprite.y:
            return False
        else:
            return True


class Paint(object):
    def __init__(self, x, y, colour, image_surrounding_blocks, image_paint):
        #TODO: Add mini blocks here surrounding paint.
        self.paint = _PaintBlock(x, y, colour, image_paint)

    def on_draw(self):
        self.paint.on_draw()

    def on_collision(self, other_x, other_y, other_height, other_width):
        return self.paint.on_collision(other_x, other_y, other_height, other_width)


class Player(object):
    def __init__(self, image, gravity, colour):
        self.sprite = pyglet.sprite.Sprite(image, 50, 200)
        self.gravity = gravity
        self.downwards_speed = 0
        self.left_speed = 0
        self.right_speed = 0
        self.colour = colour
        self.sprite.color = colour.tuple_colour

    def on_draw(self):
        self.sprite.draw()

    def on_key_press(self, key):
        if key == pyglet.window.key.SPACE:
            self.downwards_speed = -4
        if key == pyglet.window.key.A:
            self.left_speed = 1
        if key == pyglet.window.key.D:
            self.right_speed = 1

    def on_key_release(self, key):
        if key == pyglet.window.key.A:
            self.left_speed = 0
        if key == pyglet.window.key.D:
            self.right_speed = 0

    def on_update(self, blocks, paints):
        self.downwards_speed += self.gravity

        for block in blocks:
            #collision for the top of block
            if block.colour.name == self.colour.name:
                if block.on_collision(self.sprite.x, self.sprite.y-self.downwards_speed, self.sprite.width, self.sprite.height):
                    if self.downwards_speed > 0:
                        self.downwards_speed = 0


            if block.colour.name == self.colour.name:
                if block.on_collision(self.sprite.x, self.sprite.y +
                                      1, self.sprite.width, self.sprite.height):
                    self.right_speed = 0
                    self.left_speed = 0

        for paint in paints:
            if paint.on_collision(self.sprite.x, self.sprite.y +
                                  1, self.sprite.width, self.sprite.height):
                self.colour = paint.paint.colour
                self.sprite.color = paint.paint.colour.tuple_colour

        self.sprite.y -= self.downwards_speed
        self.sprite.x -= self.left_speed
        self.sprite.x += self.right_speed
        #TODO: Max speed.