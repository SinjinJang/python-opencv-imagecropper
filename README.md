python-opencv-imagecropper
==========================

Description
-----------

This is image cropping tool by mouse dragging action.
And also there are simple tool which is to make image squared and same size.
I made this tool for gathering datasets for machine learning.

Run the image cropper
---------------------

<pre><code>$ pip install -r requirements.txt
$ python imagecropper.py \
  [-i|--input-directory=specify directory to load raw images] \
  [-o|--output-directory=specify directory to save cropped images]
</code></pre>

How to crop
-----------
1. Copy the source images to load-directory before running the program. The default is 'load-img' directory.
1. Run the program.
1. When image is shown, drag mouse where you want to crop.
1. Press 's' to save the dragged area.
1. You can do it 3-4 step as much as you can.
1. Press space bar to load next image.
1. You can do it 3-4 step again with new image.
1. The program will be finished when it reaches end of images.
1. Or press 'q' to finish the program.
1. You can find the images which you cropped in save-directory. The default is 'save-img' directory.

Run the post job
----------------

This tool is for making squared/resized images from cropped images.
<pre><code>$ python postjob.py \
  [-i|--input-directory=specify directory to load cropped images] \
  [-o|--output-directory=specify directory to save squared images] \
  [-s|--size=specify the size of one side of squared images for resizing]
</code></pre>
