
from math import sin, cos, pi
from PIL import Image, ImageDraw
import numpy as np

from .canvas import Canvas
from .model import Color


class PillowCanvas(Canvas):
    """
    Draw the given results on a pillow canvas.
    """
    def __init__(self, width, height):
        super().__init__(width, height)
        self.image = Image.new('RGBA', (width, height))
        self.background_color = Color(255, 255, 255)
        self.draw = ImageDraw.Draw(self.image)

    def tr_pos(self, pos):
        x, y = pos.x, pos.y
        return x + self.width / 2, -y + self.height / 2

    @staticmethod
    def tr_color(color):
        return color.red, color.blue, color.green, 255

    def draw_rectangular_line(self, start, end, color, width):
        self.draw.line([self.tr_pos(start), self.tr_pos(end)], self.tr_color(color), width)

    def draw_circle(self, center, radius, color, width, is_filled):
        x, y = self.tr_pos(center)
        left_up = (x-radius, y-radius)
        right_down = (x+radius, y+radius)
        box = [left_up, right_down]
        if is_filled:
            self.draw.ellipse(box, fill=self.tr_color(color))
        else:
            circle(self.draw, x, y, radius, color, width=width)

    def fill_polygon(self, points, color):
        self.draw.polygon(
            [self.tr_pos(point) for point in points],
            fill=self.tr_color(color)
        )

    def set_bgcolor(self, color):
        self.background_color = color

    def clear(self):
        self.draw.rectangle((0, 0, self.width, self.height), fill=(0, 0, 0, 0))

    def export(self):
        data = np.array(self.image)
        assert len(data.shape) == 3 and data.shape[-1] == 4
        transparents = data[:,:,-1] == 0
        data[transparents] = self.tr_color(self.background_color)
        return data

def circle(draw, cx, cy, r, fill, width=1, segments=100):
    # based on https://gist.github.com/skion/9259926
    da = 2 * pi / segments
    dl = r * da

    for i in range(segments):
        a = (i+0.5) * da

        x = cx + r * cos(a)
        y = cy + r * sin(a)

        dx = -sin(a) * dl
        dy = cos(a) * dl

        draw.line([(x-dx, y-dy), (x+dx, y+dy)], fill=fill, width=width)
