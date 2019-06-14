import argparse
import os
import sys

import cv2
import numpy as np


def do_main(dir_in, dir_out, size):
    files = [{'src': os.path.join(dir_in, file), 'dst': os.path.join(dir_out, file)}
             for file in os.listdir(dir_in) if os.path.isfile(os.path.join(dir_in, file))]

    for file in files:
        img = cv2.imread(file['src'])
        if img is None:
            continue

        # make image as squared
        h, w, c = img.shape
        max_len = max(h, w)
        img_squared = np.zeros((max_len, max_len, c), np.uint8)
        img_squared[0:h, 0:w] = img

        # image resize
        img_resized = cv2.resize(img_squared, dsize=(size, size), interpolation=cv2.INTER_AREA)

        # save image
        cv2.imwrite(file['dst'], img_resized)


if __name__ == '__main__':
    # parsing arguments
    parser = argparse.ArgumentParser(description='Command line argument')
    parser.add_argument('-i', '--input-directory', type=str,
                        default='img-cropped', help='specify directory to load cropped images')
    parser.add_argument('-o', '--output-directory', type=str,
                        default='img-squared', help='specify directory to save squared images')
    parser.add_argument('-s', '--size', type=int,
                        default=128, help='specify the size of one side of squared images for resizing')
    args = parser.parse_args()

    # check and initialize
    if not os.path.isdir(args.input_directory):
        sys.exit('The input directory is not exist!!!')
    if not os.path.isdir(args.output_directory):
        os.mkdir(args.output_directory)

    # run main job for image cropping
    do_main(args.input_directory, args.output_directory, args.size)
