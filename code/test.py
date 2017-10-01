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
test_image = np.zeros([50,50,3])
for i in range(test_image.shape[0]):
    for j in range(test_image.shape[1]):
        if((i+j)%2):
            test_image[i,j] = (i + j)/2
        else:
            test_image[i,j] = 50 - (i + j)/2
            
test_image = test_image.astype(np.single)/50
plt.figure('Image')
plt.imshow(test_image)

shift_filter = np.array([[0,0,0],[1,0,0],[0,0,0]])
shift_image  = my_imfilter(test_image, shift_filter)

plt.figure('shift image')
plt.imshow(shift_image)


plt.show()