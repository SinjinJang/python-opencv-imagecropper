python-opencv-imagecropper
==========================

Description
-----------

This is image cropping tool by mouse dragging action.
I made this tool to gathering datasets for machine learning.

Run the program
---------------

<pre><code>$ pip install -r requirements.txt
$ python imagecropper.py \
  [-l|--load-directory=specify directory to load images] \
  [-s|--save-directory=specify directory to save images]
</code></pre>

How to crop
-----------
1. Copy the source images to load-directory before running the program. The default is 'load-img' directory.
1. Run the program.
1. When image is shown, drag mouse where you want to crop.
1. Press 's' to save the dragged area.
1. You can do it 3-4 step as much as you can.
1. Press 'n' to load next image.
1. You can do it 3-4 step again with new image.
1. The program will be finished when it reaches end of images.
1. Or press 'q' to finish the program.
1. You can find the images which you cropped in save-directory. The default is 'save-img' directory.
