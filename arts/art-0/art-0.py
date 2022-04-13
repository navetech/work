import sys
import math

import numpy as np
from PIL import Image


def generatrix(t):
    return np.array([t, t])


def build_rotation(theta):
    return np.array(
        [
            [math.cos(theta), - math.sin(theta)],
            [math.sin(theta), math.cos(theta)]
        ]
        )


def build_translation(tx, ty):
    return np.array([tx, ty])


def build_scale(Sx, Sy):
    return np.array([[Sx, 0], [0, Sy]])


def build_reflexion_on_Xaxis():
    return np.array([[1, 0], [0, -1]])


def build_reflexion_on_Yaxis():
    return np.array([[-1, 0], [0, 1]])


def build_reflexion_on_X_and_Yaxis():
    return np.array([[-1, 0], [0, -1]])


# Shearing (distorção, deslizamento)
def build_shearing__on_Xdirection(Shx):
    return np.array([[1, Shx], [0, 1]])


def build_shearing__on_Ydirection(Shy):
    return np.array([[1, 0], [Shy, 1]])


def main():
    if len(sys.argv) != 1 and len(sys.argv) != 5:
        sys.exit(
            "Usage: python art-0.py [num-points] [period] [width] [height]"
            )

    num_points = sys.argv[1] if len(sys.argv) >= 2 else 64
    num_points = int(num_points)
    period = sys.argv[2] if len(sys.argv) >= 3 else 36
    period = int(period)
    width = sys.argv[3] if len(sys.argv) >= 4 else 256
    width = int(width)
    height = sys.argv[4] if len(sys.argv) >= 5 else 256
    height = int(height)

    min_dimension = min(width, height)
    scale = min_dimension / 2
    scale_matrix = np.array(
        [
            [scale, 0],
            [0, scale]]
        )

    points = np.empty([2, num_points])
    for n in range(num_points):
        point = generatrix(n / num_points)
        point = np.dot(scale_matrix, point)
        points[0][n] = point[0]
        points[1][n] = point[1]

    frames_images = []
    frame_array = None

    opposite_y = np.array([[1, 0], [0, -1]])
    translation = np.array([width / 2, height / 2])

    for t in range(period):
        frame_points = []

        for n in range(num_points):
            point = np.array([points[0][n], points[1][n]])

            theta = ((2 * math.pi) * t) / period
            transformation = build_rotation(theta)
            point = np.dot(transformation, point)

            point = np.dot(opposite_y, point)
            point = np.add(translation, point)

            frame_points.append(
                {'x': point[0], 'y': point[1]}
                )

        frame = build_frame(
            frame_array, frame_points,
            width, height, bg_color=0
            )
        frame_array = frame['array']
        frames_images.append(frame['image'])

    img = Image.fromarray(frame_array)
    img.save('art-0.png')

    frame_one = frames_images[0]
    frame_one.save(
        "art-0.gif", format="GIF", append_images=frames_images,
        save_all=True, duration=100, loop=0
        )


def build_frame(merged_frame_array, frame_points, width, height, bg_color=0):
    if merged_frame_array is None:
        merged_frame_array = np.empty([height, width], dtype=np.uint8)
        for y in range(0, height):
            for x in range(0, width):
                merged_frame_array[y, x] = bg_color

    frame_array = np.empty([height, width], dtype=np.uint8)
    for y in range(0, height):
        for x in range(0, width):
            frame_array[y, x] = bg_color

    for point in frame_points:
        x = int(point['x'])
        y = int(point['y'])

        if x >= 0 and y >= 0 and x < width and y < height:
            frame_array[y, x] = 255 - frame_array[y, x]
            merged_frame_array[y, x] = 255 - merged_frame_array[y, x]

    img = Image.fromarray(frame_array)

    return {
        'image': img,
        'array': merged_frame_array
        }


if __name__ == "__main__":
    main()
