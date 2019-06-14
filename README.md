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
1. Copy the source image to load directory before running the program. The default is 'load-img' directory.
2. When image is shown, drag mouse where you want to crop.
3. Press 's' to save the dragged area.
4. You can do it 2-3 step as much as you can.
5. Press 'n' to load next image.
6. You can do it 2-4 step again.
7. Press 'q' to exit the program.
