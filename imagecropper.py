import argparse
import datetime
import os
import sys

import cv2

img = None
p0 = None
p1 = None


# draw box which selected by mouse dragging
def draw_box(_img, _p0, _p1):
    boxed = _img.copy()
    boxed = cv2.rectangle(boxed, _p0, _p1, (0, 255, 0), 2)
    cv2.imshow('image', boxed)


# Save the boxed area as an image
def save_box(_img, _p0, _p1, _dir_out):
    now = datetime.datetime.now()
    filename = now.strftime('%Y-%m-%d_%H-%M-%S')

    x0 = min(_p0[0], _p1[0])
    y0 = min(_p0[1], _p1[1])
    x1 = max(_p0[0], _p1[0])
    y1 = max(_p0[1], _p1[1])

    img_boxed = img[y0:y1, x0:x1]
    cv2.imwrite(os.path.join(_dir_out, filename + '.png'), img_boxed)

    print('saved image x0:{0}, y0:{1}, x1:{2}, y1:{3}'.format(x0, y0, x1, y1))


# mouse callback function
def select_box(event, x, y, flags, param):
    global p0, p1, img

    if event == cv2.EVENT_LBUTTONDOWN:
        p0 = (x, y)
        p1 = None
    elif event == cv2.EVENT_LBUTTONUP:
        if p0 == p1:
            p0 = p1 = None
        else:
            p1 = (x, y)

    if p0 is not None and p1 is None:
        draw_box(img, p0, (x, y))


def do_main(dir_in, dir_out):
    global img, p0, p1

    files = [os.path.join(dir_in, file) for file in os.listdir(dir_in)
             if os.path.isfile(os.path.join(dir_in, file))]

    for file in files:
        img = cv2.imread(file, cv2.IMREAD_COLOR)
        cv2.imshow('image', img)
        cv2.setMouseCallback('image', select_box)

        while True:
            k = cv2.waitKey(100) & 0xFF
            if k == ord('q') or cv2.getWindowProperty('image', cv2.WND_PROP_VISIBLE) < 1:
                # wait for 'q' key to exit the program
                cv2.destroyAllWindows()
                exit()
            elif k == ord('s'):
                # wait for 's' key to save boxed image
                if p0 is not None and p1 is not None:
                    save_box(img, p0, p1, dir_out)
                    cv2.imshow('image', img)
                    p0 = p1 = None
            elif k == ord('n'):
                # wait for 'n' key to load next image
                break

    cv2.destroyAllWindows()


if __name__ == '__main__':
    # parsing arguments
    parser = argparse.ArgumentParser(description='Command line argument')
    parser.add_argument('-i', '--input-directory', type=str,
                        default='img-raw', help='specify directory to load raw images')
    parser.add_argument('-o', '--output-directory', type=str,
                        default='img-cropped', help='specify directory to save cropped images')
    args = parser.parse_args()

    # check and initialize
    if not os.path.isdir(args.input_directory):
        sys.exit('The input directory is not exist!!!')
    if not os.path.isdir(args.output_directory):
        os.mkdir(args.output_directory)

    # run main job for image cropping
    do_main(args.input_directory, args.output_directory)
