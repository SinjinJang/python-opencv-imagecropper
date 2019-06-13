import datetime
import numpy as np
import cv2

img = None
p0 = None
p1 = None


# draw box which selected by mouse dragging
def draw_box(img, p0, p1):
    boxed = img.copy()
    boxed = cv2.rectangle(boxed, p0, p1, (0, 255, 0), 2)
    cv2.imshow('image', boxed)


# Save the boxed area as an image
def save_box(img, p0, p1):
    now = datetime.datetime.now()
    filename = now.strftime('%Y-%m-%d_%H-%M-%S')

    x0 = min(p0[0], p1[0])
    y0 = min(p0[1], p1[1])
    x1 = max(p0[0], p1[0])
    y1 = max(p0[1], p1[1])

    img_boxed = img[y0:y1, x0:x1]
    cv2.imwrite(filename + '.png', img_boxed)

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


def main():
    global img, p0, p1

    img = cv2.imread('./test.jpg', cv2.IMREAD_COLOR)
    cv2.imshow('image', img)
    cv2.setMouseCallback('image', select_box)

    while True:
        k = cv2.waitKey(100) & 0xFF
        if k == 27 or cv2.getWindowProperty('image', cv2.WND_PROP_VISIBLE) < 1:
            # wait for ESC key to exit
            break
        elif k == ord('s'):
            # wait for 's' key to save
            if p0 is not None and p1 is not None:
                save_box(img, p0, p1)
                cv2.imshow('image', img)
                p0 = p1 = None

    cv2.destroyAllWindows()


if __name__ == '__main__':
    main()
