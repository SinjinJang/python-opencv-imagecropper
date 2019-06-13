import datetime
import numpy as np
import cv2

img = None
p0 = None
p1 = None

# draw box which selected by mouse dragging
def draw_box(img, p0, p1):
    boxed = img.copy()
    boxed = cv2.rectangle(boxed, p0, p1, (0, 255, 00), 2)
    cv2.imshow('image', boxed)

# mouse callback function
def drag_and_crop(event, x, y, flags, param):
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
    global img

    img = cv2.imread('./test.jpg', cv2.IMREAD_COLOR)
    cv2.imshow('image', img)
    cv2.setMouseCallback('image', drag_and_crop)

    while True:
        k = cv2.waitKey(0) & 0xFF
        if k == 27:         # wait for ESC key to exit
            cv2.destroyAllWindows()
            exit()
        elif k == ord('s'): # wait for 's' key to save
            if p0 is not None and p1 is not None:
                now = datetime.datetime.now()
                filename = now.strftime('%Y-%m-%d_%H-%M-%S')
                
                x0 = min(p0[0], p1[0])
                y0 = min(p0[1], p1[1])
                x1 = max(p0[0], p1[0])
                y1 = max(p0[1], p1[1])
                
                img_boxed = img[y0:y1, x0:x1]
                cv2.imwrite(filename + '.png', img_boxed)

                print('saved image x0:{0}, y0:{1}, x1:{2}, y1:{3}'.format(x0, y0, x1, y1))

if __name__ == '__main__':
    main()
