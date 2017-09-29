import numpy as np
import time

def pad(image, shape):
    image_new = np.zeros((image.shape[0] + shape[0] - 1, image.shape[1] + shape[1] - 1, image.shape[2]))
    row_begin = shape[0]//2
    clm_begin = shape[1]//2
    image_new[row_begin:row_begin + image.shape[0], clm_begin:clm_begin + image.shape[1], :] = image
    
    return image_new


def my_imfilter(image, imfilter):

    '''
    Input:
        image: A 3d array represent the input image.
        imfilter: The gaussian filter.
    Output:
        output: The filtered image.
    '''
    ###################################################################################
    # TODO:                                                                           #
    # This function is intended to behave like the scipy.ndimage.filters.correlate    #
    # (2-D correlation is related to 2-D convolution by a 180 degree rotation         #
    # of the filter matrix.)                                                          #
    # Your function should work for color images. Simply filter each color            #
    # channel independently.                                                          #
    # Your function should work for filters of any width and height                   #
    # combination, as long as the width and height are odd (e.g. 1, 7, 9). This       #
    # restriction makes it unambigious which pixel in the filter is the center        #
    # pixel.                                                                          #
    # Boundary handling can be tricky. The filter can't be centered on pixels         #
    # at the image boundary without parts of the filter being out of bounds. You      #
    # should simply recreate the default behavior of scipy.signal.convolve2d --       #
    # pad the input image with zeros, and return a filtered image which matches the   #
    # input resolution. A better approach is to mirror the image content over the     #
    # boundaries for padding.                                                         #
    # Uncomment if you want to simply call scipy.ndimage.filters.correlate so you can # 
    # see the desired behavior.                                                       #
    # When you write your actual solution, you can't use the convolution functions    #
    # from numpy scipy ... etc. (e.g. numpy.convolve, scipy.signal)                   #
    # Simply loop over all the pixels and do the actual computation.                  #
    # It might be slow.                                                               #
    ###################################################################################
    ###################################################################################
    # NOTE:                                                                           #
    # Some useful functions                                                           #
    #     numpy.pad or numpy.lib.pad                                                  #
    # #################################################################################
    
    # Uncomment if you want to simply call scipy.ndimage.filters.correlate so you can 
    # see the desired behavior.

    print("################### time #####################")

    import scipy.ndimage as ndimage
    tStart = time.time()
    output_org = np.zeros_like(image)
    for ch in range(image.shape[2]):
        output_org[:,:,ch] = ndimage.filters.correlate(image[:,:,ch], imfilter, mode='constant')
    time_org = time.time() - tStart
    print("time_org: " + str(time_org))
    
    tStart2 = time.time()
    output_v1 = np.zeros_like(image)
    row = imfilter.shape[0];
    clm = imfilter.shape[1];
    image_pad = pad(image, imfilter.shape);
    for i in range(image.shape[0]):
        for j in range(image.shape[1]):
            for ch in range(image.shape[2]):
                output_v1[i,j,ch] = np.sum(image_pad[i:i+row,j:j+clm,ch] * imfilter)
    
    time_v1 = time.time() - tStart2
    print("time_v1:" + str(time_v1))
    
    tStart3 = time.time()
    output_v2 = np.zeros_like(image)
    duplic = np.zeros((image.shape[0] + imfilter.shape[0] - 1, image.shape[1] + imfilter.shape[1] - 1, imfilter.shape[0] * imfilter.shape[1]))
    row_begin = imfilter.shape[0]//2
    clm_begin = imfilter.shape[1]//2
    for ch in range(image.shape[2]):
        for i in range(imfilter.shape[0]):
            for j in range(imfilter.shape[1]):
                duplic[i:i + image.shape[0], j:j + image.shape[1], i*imfilter.shape[1] + j] = image[:,:,ch] * imfilter[imfilter.shape[0]-i-1,imfilter.shape[1]-j-1]
        output_v2[:,:,ch] = np.sum(duplic[row_begin:row_begin + image.shape[0], clm_begin:clm_begin + image.shape[1],:], axis = 2)
    
    time_v2 = time.time() - tStart3
    print("time_v2:" + str(time_v2))
    
    # print("time_pad:" + str(tStart4 - tStart3))
    # print("time_cor:" + str(time_new - (tStart4 - tStart2)))
    
    ###################################################################################
    #                                 END OF YOUR CODE                                #
    ###################################################################################
    return output_v2
















