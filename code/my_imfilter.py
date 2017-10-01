import numpy as np
import time

def pad(image, shape, mode = 'zero'):
    image_new = np.zeros((image.shape[0] + shape[0] - 1, image.shape[1] + shape[1] - 1, image.shape[2]))
    row_begin = shape[0]//2
    clm_begin = shape[1]//2
    image_new[row_begin:row_begin + image.shape[0], clm_begin:clm_begin + image.shape[1], :] = image
    if(mode == 'reflect'):
        image_new[0:row_begin, clm_begin:clm_begin + image.shape[1], :] = image[row_begin:0:-1,:,:]
        image_new[row_begin + image.shape[0]:, clm_begin:clm_begin + image.shape[1],:] \
            = image[image.shape[0]:image.shape[0] - row_begin - 1:-1,:,:]
        
        image_new[:, 0:clm_begin, :] = image_new[:,2*clm_begin:clm_begin:-1,:]
        image_new[:, clm_begin + image.shape[1]:, :] \
            = image_new[:,image.shape[1]+clm_begin - 1:image.shape[1] - 1:-1,:]
    
    return image_new
    
def pad2(image, shape, i, j,  mode = 'reflect'):
    image_new = np.zeros_like(image)
    row_begin = max([i - shape[0]//2, 0])
    clm_begin = max([j - shape[1]//2, 0])
    
    row_end = image.shape[0] - max([shape[0]//2 - i, 0])
    clm_end = image.shape[1] - max([shape[1]//2 - j, 0])
    
    row_begin2 = max([shape[0]//2 - i, 0])
    clm_begin2 = max([shape[0]//2 - j, 0])
    
    row_end2 = image.shape[0] - max([i - shape[0]//2, 0])
    clm_end2 = image.shape[1] - max([j - shape[1]//2, 0])
    
    image_new[row_begin2:row_end2, clm_begin2:clm_end2, :] = image[row_begin:row_end, clm_begin:clm_end, :]
    if(mode == 'reflect'):
        if(i < shape[0]//2):
            image_new[:row_begin2, clm_begin2:clm_end2, :] = image[row_begin2-1::-1, clm_begin:clm_end,:]

        elif(i > shape[1]//2):
            image_new[row_end2:, clm_begin2:clm_end2, :] = image[:row_end2-1:-1, clm_begin:clm_end,:]

        if(j < shape[1]//2):
            image_new[:, :clm_begin2, :] = image_new[:, clm_begin2:clm_begin2*2, :]
        elif(j > shape[1]//2):
            image_new[:, clm_end2:, :] = image_new[:, clm_end2-(j - shape[1]//2):clm_end2, :]
        
    
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

    print("###### time ######")

    import scipy.ndimage as ndimage
    tStart = time.time()
    output_org = np.zeros_like(image)
    for ch in range(image.shape[2]):
        output_org[:,:,ch] = ndimage.filters.correlate(image[:,:,ch], imfilter, mode='reflect')
    time_org = time.time() - tStart
    print("time_org: " + str(time_org))
    
    ######################## ver 1 ##########################
    # tStart2 = time.time()
    # output_v1 = np.zeros_like(image)
    # row = imfilter.shape[0];
    # clm = imfilter.shape[1];
    # image_pad = pad(image, imfilter.shape, 'reflect');
    # for i in range(image.shape[0]):
    #     for j in range(image.shape[1]):
    #         for ch in range(image.shape[2]):
    #             output_v1[i,j,ch] = np.sum(image_pad[i:i+row,j:j+clm,ch] * imfilter)
    # 
    # time_v1 = time.time() - tStart2
    # print("time_v1:" + str(time_v1))
    
    ######################## ver 2 ##########################
    # tStart3 = time.time()
    # duplic = np.zeros((image.shape[0] + imfilter.shape[0] - 1, image.shape[1] + imfilter.shape[1] - 1, image.shape[2], imfilter.shape[0] * imfilter.shape[1]))
    # row_begin = imfilter.shape[0]//2
    # clm_begin = imfilter.shape[1]//2
    # for i in range(imfilter.shape[0]):
    #     for j in range(imfilter.shape[1]):
    #         duplic[i:i + image.shape[0], j:j + image.shape[1], :, i*imfilter.shape[1] + j] = \
    #          image[:,:,:] * imfilter[imfilter.shape[0]-i-1,imfilter.shape[1]-j-1]
    # output_v2 = np.sum(duplic[row_begin:row_begin + image.shape[0], clm_begin:clm_begin + image.shape[1],:,:], axis = 3)
    # 
    # time_v2 = time.time() - tStart3
    # print("time_v2:" + str(time_v2))
    
    ######################## ver 3 ##########################
    # tStart4 = time.time()
    # duplic = np.zeros((image.shape[0], image.shape[1], image.shape[2], imfilter.shape[0] * imfilter.shape[1]))
    # for i in range(imfilter.shape[0]):
    #     for j in range(imfilter.shape[1]):
    #         duplic[:, :, :, i*imfilter.shape[1] + j] = pad2(image, imfilter.shape, i, j) * imfilter[i, j]
    # output_v3 = np.sum(duplic, axis = 3)
    # 
    # time_v3 = time.time() - tStart4
    # print("time_v3:" + str(time_v3))
    
    ######################## ver 4 ##########################
    # tStart5 = time.time()
    # duplic = np.zeros((image.shape[0], image.shape[1], image.shape[2], imfilter.shape[0] * imfilter.shape[1]))
    # for i in range(imfilter.shape[0]):
    #     for j in range(imfilter.shape[1]):
    #         row_begin = max([i - imfilter.shape[0]//2, 0])
    #         clm_begin = max([j - imfilter.shape[1]//2, 0])
    #         
    #         row_end = image.shape[0] - max([imfilter.shape[0]//2 - i, 0])
    #         clm_end = image.shape[1] - max([imfilter.shape[1]//2 - j, 0])
    #         
    #         row_begin2 = max([imfilter.shape[0]//2 - i, 0])
    #         clm_begin2 = max([imfilter.shape[1]//2 - j, 0])
    #         
    #         row_end2 = image.shape[0] - max([i - imfilter.shape[0]//2, 0])
    #         clm_end2 = image.shape[1] - max([j - imfilter.shape[1]//2, 0])
    #         
    #         duplic[row_begin2:row_end2, clm_begin2:clm_end2, :, i*imfilter.shape[1] + j] = \
    #          image[row_begin:row_end, clm_begin:clm_end, :] * imfilter[i, j]
    #         
    # output_v4 = np.sum(duplic, axis = 3)
    # time_v4 = time.time() - tStart5
    # print("time_v4:" + str(time_v4))
    
    ######################## ver 5 ##########################
    tStart6 = time.time()
    output_v5 = np.zeros_like(image)
    for i in range(imfilter.shape[0]):
        for j in range(imfilter.shape[1]):
            output_v5 += pad2(image, imfilter.shape, i, j, 'reflect') * imfilter[i, j]
    
    time_v5 = time.time() - tStart6
    print("time_v5:" + str(time_v5))
    
    print(np.max(abs(output_org - output_v5)))
    
    ###################################################################################
    #                                 END OF YOUR CODE                                #
    ###################################################################################
    return output_v5

