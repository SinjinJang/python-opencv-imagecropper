import datetime
import numpy as np
import cv2

x0 = 0
y0 = 0
x1 = 0
y1 = 0
img_cropped = None

# mouse callback function
def drag_and_crop(event, x, y, flags, param):
    global x0, x1, y0, y1, img, img_cropped
    if event == cv2.EVENT_LBUTTONDOWN:
        x0, y0 = x, y
    elif event == cv2.EVENT_LBUTTONUP:
        x1, y1 = x, y

        if x0 == x1 and y0 == y1:
            x0, x1, y0, y1 = 0, 0, 0, 0
            return

        len = max(x1 - x0, y1 - y0)
        img_cropped = img[y0:y0+len, x0:x0+len]
        cv2.imshow('img_cropped', img_cropped)

        print('org - x0:{0}, y0:{1}, x1:{2}, y1:{3}'.format(x0, y0, x1, y1))
        print('mod - x0:{0}, y0:{1}, x1:{2}, y1:{3}'.format(x0, y0, x0+len, y0+len))


img = cv2.imread('./test.jpg', cv2.IMREAD_COLOR)
cv2.imshow('image', img)
cv2.setMouseCallback('image', drag_and_crop)


while True:
    k = cv2.waitKey(0) & 0xFF
    if k == 27:         # wait for ESC key to exit
        cv2.destroyAllWindows()
        exit()
    elif k == ord('s'): # wait for 's' key to save
        if img_cropped is not None:
            now = datetime.datetime.now()
            filename = now.strftime('%Y-%m-%d_%H-%M-%S')
            cv2.imwrite(filename + '.png', img_cropped)
            cv2.destroyWindow('img_cropped')
