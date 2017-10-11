#this script has test cases to help you test my_imfilter() which you will
#write. You should verify that you get reasonable output here before using
#your filtering to construct a hybrid image in proj1.m. The outputs are
#all saved and you can include them in your writeup. You can add calls to
#imfilter() if you want to check that my_imfilter() is doing something
#similar.



from gauss2D import gauss2D
from my_imfilter import my_imfilter
from my_imfilter import pad2
from normalize import normalize
from scipy.misc import imresize
import numpy as np
import matplotlib.image as mpimg
import matplotlib.pyplot as plt
import os

''' set up '''
main_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
img_path = main_path + '/data/cat.bmp'
test_image = mpimg.imread(img_path)
test_image = imresize(test_image,0.7,'bilinear')
test_image = test_image.astype(np.single)/255
plt.figure('Image')
plt.imshow(test_image)

''' Large blur '''
#This blur would be slow to do directly, so we instead use the fact that
#Gaussian blurs are separable and blur sequentially in each direction.
# large_2d_blur_filter = gauss2D(shape=(25,25), sigma = 10)
test = pad2(test_image, (25,25), 0, 0)
plt.figure('Gauss filter')
plt.imshow(normalize(test))

plt.show()