# Before trying to construct hybrid images, it is suggested that you
# implement my_imfilter.m and then debug it using proj1_test_filtering.py

from my_imfilter import my_imfilter
from vis_hybrid_image import vis_hybrid_image
from normalize import normalize
from gauss2D import gauss2D
import numpy as np
import matplotlib.image as mpimg
from PIL import Image
import matplotlib.pyplot as plt
import scipy
import os

''' Setup '''
# read images and convert to floating point format
name1 = 'submarine'
name2 = 'fish'
main_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
image1 = mpimg.imread(main_path + '/data/'+ name1 + '.bmp')
image2 = mpimg.imread(main_path + '/data/'+ name2 + '.bmp')
image1 = image1.astype(np.single)/255
image2 = image2.astype(np.single)/255

# Several additional test cases are provided for you, but feel free to make
# your own (you'll need to align the images in a photo editor such as
# Photoshop). The hybrid images will differ depending on which image you
# assign as image1 (which will provide the low frequencies) and which image
# you asign as image2 (which will provide the high frequencies)

''' Filtering and Hybrid Image construction '''
cutoff_frequency = 4 # This is the standard deviation, in pixels, of the 
# Gaussian blur that will remove the high frequencies from one image and 
# remove the low frequencies from another image (by subtracting a blurred
# version from the original version). You will want to tune this for every
# image pair to get the best results.
gaussian_filter = gauss2D(shape=(cutoff_frequency*4+1,cutoff_frequency*4+1), sigma = cutoff_frequency)


#########################################################################
# TODO: Use my_imfilter create 'low_frequencies' and                    #
# 'high_frequencies' and then combine them to create 'hybrid_image'     #
#########################################################################
#########################################################################
# Remove the high frequencies from image1 by blurring it. The amount of #
# blur that works best will vary with different image pairs             #
#########################################################################
low_frequencies = my_imfilter(image1, gaussian_filter)


############################################################################
# Remove the low frequencies from image2. The easiest way to do this is to #
# subtract a blurred version of image2 from the original version of image2.#
# This will give you an image centered at zero with negative values.       #
############################################################################
pulse = np.zeros_like(gaussian_filter)
pulse[cutoff_frequency*2 + 1,cutoff_frequency*2 + 1] = 1
# high_frequencies = np.clip(my_imfilter(image2, pulse - gaussian_filter), -0.5 ,0.5)
high_frequencies = my_imfilter(image2, pulse - gaussian_filter)

############################################################################
# Combine the high frequencies and low frequencies                         #
############################################################################
hybrid_image = normalize(high_frequencies + low_frequencies)
# hybrid_image2 = normalize(np.sqrt((high_frequencies + 0.5) * low_frequencies))

''' Visualize and save outputs '''
plt.figure(1)
plt.imshow(low_frequencies)
plt.figure(2)
plt.imshow(high_frequencies+0.5)
vis = vis_hybrid_image(hybrid_image)
plt.figure(3)
plt.imshow(vis)
# plt.figure(4)
# vis2 = vis_hybrid_image(hybrid_image2)
# plt.imshow(vis2)
plt.imsave(main_path+'/results/low_frequencies_'+ name1 + '.png', low_frequencies, 'quality', 95)
plt.imsave(main_path+'/results/high_frequencies_'+ name2 + '.png', high_frequencies + 0.5, 'quality', 95)
plt.imsave(main_path+'/results/hybrid_image_'+ name1 + '_' +  name2 + '.png', hybrid_image, 'quality', 95)
plt.imsave(main_path+'/results/hybrid_image_scales_'+ name1 + '_' +  name2 + '.png', vis, 'quality', 95)
# plt.imsave(main_path+'/results/hybrid_image2_'+ name1 + '_' +  name2 + '.png', hybrid_image2, 'quality', 95)
# plt.imsave(main_path+'/results/hybrid_image_scales2_'+ name1 + '_' +  name2 + '.png', vis2, 'quality', 95)
plt.show()
