import math

import numpy as np
from PIL import Image


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __str__(self):
        return f'({self.x},{self.y})'

    def transform(self, t, T):
        x = self.x
        y = self.y

        r = math.sqrt(pow(x, 2) + pow(y, 2))
        theta = math.atan2(y, x)

        r = r
        theta += ((2 * math.pi) * t) / T

        x_transformed = r * math.cos(theta)
        y_transformed = r * math.sin(theta)

        return Point(x_transformed, y_transformed)

    def shift(self, half_width, half_height):
        x_out = int(self.x + half_width)
        y_out = int(-self.y + half_height)

        return Point(x_out, y_out)


def build_frame(frame_points, frame_width, frame_height, background_color=0):
    frame_array = np.empty([frame_height, frame_width], dtype=np.uint8)
    for y in range(0, frame_height):
        for x in range(0, frame_width):
            frame_array[y,x] = background_color

    for point in frame_points:
        x = point.x
        y = point.y

        if x >= 0 and y >= 0 and x < frame_width and y < frame_height:
            frame_array[y,x] = 255 - frame_array[y,x]

    img = Image.fromarray(frame_array)

    return img


def merge_frame(frame_array, frame_points, frame_width, frame_height, background_color=0):
    if frame_array is None:
        frame_array = np.empty([frame_height, frame_width], dtype=np.uint8)
        for y in range(0, frame_height):
            for x in range(0, frame_width):
                frame_array[y,x] = background_color

    for point in frame_points:
        x = point.x
        y = point.y

        if x >= 0 and y >= 0 and x < frame_width and y < frame_height:
            frame_array[y,x] = 255 - frame_array[y,x]

    img = Image.fromarray(frame_array)

    return {
        'img': img,
        'array': frame_array
        }

