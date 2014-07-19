from PIL import Image
from numpy import *
from pylab import *
import numpy as np
from matplotlib import pyplot as plt
import scipy
import cv2
import homography
import sfm
import sift
import camera



def plane_sweep_ncc(im_l,im_r,start,steps,wid):

	m,n = im_l.shape

	# arrays holding the different sum
	mean_l = zeros((m,n))
	mean_r = zeros((m,n))
	s = zeros((m,n))
	s_l = zeros((m,n))
	s_r = zeros((m,n))

	# array to hold depth planes
	dmaps = zeros((m,n,steps))

	#compute mean of patch
	filters.uniform_filter(im_l,wid,mean_l)
	filters.uniform_filter(im_r,wid,mean_r)

	#normalized images
	norm_l = im_l - mean_l
	norm_r = im_r - mean_r

	#try different disparities
	for displ in range(steps):
			#move left screen to right and compute sums
			filters.uniform_filter(roll(norm_l,-displ-start)*norm_r,wid,s) #nominator
			filters.uniform_filter(roll(norm_l,-displ-start)*roll(norm_l,-displ-start),wid,s_l)
			filters.uniform_filter(norm_r*norm_r,wid,s_r) # sum denaminator

			#store ncc scores
			dmaps[:,:,displ] = s/sqrt(s_l*s_r)

		# pick best depth for each pixels
	return argmax(dmaps,axis=2)

