import argparse
import datetime
import os
import sys

import cv2


img_org = None
img = None
p0 = None
p1 = None
resize_ratio = 1

opt_squared = False
auto_box_size = 50


def make_squared(_p0, _p1):
    """ Make a rectangle as squared """

    # Nothing to do if two points are same.
    if _p0 == _p1:
        return _p0, _p1

    long_side = max(abs(_p1[0] - _p0[0]), abs(_p1[1] - _p0[1]))

    if _p1[0] > _p0[0]:
        p1_x = _p0[0] + long_side
    else:
        p1_x = _p0[0] - long_side

    if _p1[1] > _p0[1]:
        p1_y = _p0[1] + long_side
    else:
        p1_y = _p0[1] - long_side

    return _p0, (p1_x, p1_y)


def draw_box(_img, _p0, _p1):
    """ Draw box which selected by mouse dragging """
    global opt_squared

    boxed = _img.copy()

    if opt_squared:
        _p0, _p1 = make_squared(_p0, _p1)

    boxed = cv2.rectangle(boxed, _p0, _p1, (0, 255, 0), 2)
    cv2.imshow('image', boxed)


def save_box(_img, _p0, _p1, _dir_out):
    """ Save the boxed area as an image """
    global opt_squared, img_org

    now = datetime.datetime.now()
    filename = now.strftime('%Y-%m-%d_%H-%M-%S')

    if opt_squared:
        _p0, _p1 = make_squared(_p0, _p1)

    x0 = int(min(_p0[0], _p1[0]) // resize_ratio)
    y0 = int(min(_p0[1], _p1[1]) // resize_ratio)
    x1 = int(max(_p0[0], _p1[0]) // resize_ratio)
    y1 = int(max(_p0[1], _p1[1]) // resize_ratio)

    img_boxed = img_org[y0:y1, x0:x1]
    cv2.imwrite(os.path.join(_dir_out, filename + '.png'), img_boxed)

    print('saved image x0:{0}, y0:{1}, x1:{2}, y1:{3}'.format(x0, y0, x1, y1))


def drag_box(event, x, y, flags, param):
    """ Mouse callback function - by mouse dragging """
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


def auto_box(event, x, y, flags, param):
    """ Mouse callback function - always draw box which resizable """
    global p0, p1, img, auto_box_size

    p0 = (x, y)
    p1 = (x + auto_box_size, y + auto_box_size)

    draw_box(img, p0, p1)


def do_main(dir_in, dir_out, is_auto_box_on):
    global img_org, img, p0, p1, resize_ratio, opt_squared, auto_box_size

    files = [os.path.join(dir_in, each) for each in os.listdir(dir_in)
             if os.path.isfile(os.path.join(dir_in, each))]
    files.sort()

    nums = len(files)
    idx = 0

    while nums > idx:
        img_org = cv2.imread(files[idx], cv2.IMREAD_COLOR)

        # If the file is not image, then continue to next
        if img_org is None:
            idx += 1
            continue

        # Shrink image if the image is too big to display on the screen
        height = img_org.shape[0]
        if height > 1000:
            resize_ratio = (1000 / height) - 0.1
            img = cv2.resize(img_org, dsize=(0, 0), fx=resize_ratio, fy=resize_ratio,
                             interpolation=cv2.INTER_AREA)

        # Show image
        cv2.imshow('image', img)
        cv2.setMouseCallback('image', auto_box if is_auto_box_on else drag_box)
        print('[{}/{}] {}'.format(idx+1, nums, files[idx]))

        while True:
            k = cv2.waitKey(100) & 0xFF
            if k == ord('q') or cv2.getWindowProperty('image', 0) == -1:
                # wait for 'q' key to exit the program
                cv2.destroyAllWindows()
                exit()
            elif k == ord('s'):
                # wait for 's' key to save boxed image
                if p0 is not None and p1 is not None:
                    save_box(img, p0, p1, dir_out)
                    cv2.imshow('image', img)
                    p0 = p1 = None
            elif k == ord('d'):
                # wait for 'd' key to decrease auto box size
                if auto_box_size > 10:
                    auto_box_size -= 10
            elif k == ord('t'):
                # wait for 't' key to toggle squared box on/off
                opt_squared = not opt_squared
            elif k == ord(' '):
                # wait for ' ' key to load next image
                idx += 1
                break
            elif k == ord('b'):
                # wait for 'b' key to load previous image
                idx -= 1
                break
            elif k == ord('f'):
                # wait for 'f' key to increase auto box size
                auto_box_size += 10

    cv2.destroyAllWindows()


if __name__ == '__main__':
    # parsing arguments
    parser = argparse.ArgumentParser(description='Command line argument')
    parser.add_argument('-i', '--input-directory', type=str, default='img-raw',
                        help='specify directory to load raw images')
    parser.add_argument('-o', '--output-directory', type=str, default='img-cropped',
                        help='specify directory to save cropped images')
    parser.add_argument('-a', '--auto_box', action='store_true',
                        help='draw box for cropping image automatically')
    args = parser.parse_args()

    # check and initialize
    if not os.path.isdir(args.input_directory):
        sys.exit('The input directory is not exist!!!')
    if not os.path.isdir(args.output_directory):
        os.mkdir(args.output_directory)

    # run main job for image cropping
    do_main(args.input_directory, args.output_directory, args.auto_box)
