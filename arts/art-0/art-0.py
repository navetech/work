import sys
import math

import numpy as np
from PIL import Image

from util import Point, build_frame, merge_frame


def main():
    if len(sys.argv) != 2 and len(sys.argv) != 3 :
        sys.exit("Usage: python art-0.py number-of-points [period]")

    N = sys.argv[1] if len(sys.argv) >= 2 else 64
    N = int(N)
    T = sys.argv[2] if len(sys.argv) == 3 else 36
    T = int(T)

    # Build generatrix
    generatrix_points = []
    for i in range(0, N):
        point = Point(x=i, y=i)
        generatrix_points.append(point)

    half_width = len(generatrix_points)
    half_height = len(generatrix_points)

    width = half_width * 2
    height = half_height * 2

    frames = []

    merged_frames = []

    merged_frame_array = None

    for  t in range(0, T):
        frame_points = []

        for point in generatrix_points:
            transformed_point = point.transform(t, T)

            shifted_point = transformed_point.shift(half_width, half_height)
            frame_points.append(shifted_point)

        frame = build_frame(frame_points, width, height, background_color=0)
        frames.append(frame)

        merged_frame = merge_frame(merged_frame_array, frame_points, width, height, background_color=0)
        merged_frames.append(merged_frame['img'])
        merged_frame_array = merged_frame['array']

    img = Image.fromarray(merged_frame_array)
    img.save('testgrey.png')

    merged_frame_array = None

    for  t in range(0, T):
        frame_points = []

        for point in generatrix_points:
            transformed_point = point.transform(t, T)

            shifted_point = transformed_point.shift(half_width, half_height)
            frame_points.append(shifted_point)

        frame = build_frame(frame_points, width, height, background_color=255)
        frames.append(frame)

        merged_frame = merge_frame(merged_frame_array, frame_points, width, height, background_color=255)
        merged_frames.append(merged_frame['img'])
        merged_frame_array = merged_frame['array']

    frame_one = frames[0]
    """
    frame_one.save("circle.gif", format="GIF", append_images=frames,
                   save_all=True, duration=100, loop=0)
    """
    frame_one.save("circle.gif", format="GIF", append_images=frames,
                   save_all=True, duration=100, loop=1)


    frame_one = merged_frames[0]
    frame_one.save("circle2.gif", format="GIF", append_images=merged_frames,
                   save_all=True, duration=100, loop=1)


if __name__ == "__main__":
    main()
