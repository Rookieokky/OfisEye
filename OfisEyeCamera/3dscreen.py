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
import stereo
import sys
import video

ply_header = '''ply
format ascii 1.0
element vertex %(vert_num)d
property float x
property float y
property float z
property uchar red
property uchar green
property uchar blue
end_header
'''


# temporary hardcoded video sources
camLeft = 3
camRight = 4

def write_ply(fn, verts, colors):
    verts = verts.reshape(-1, 3)
    colors = colors.reshape(-1, 3)
    verts = np.hstack([verts, colors])
    with open(fn, 'w') as f:
        f.write(ply_header % dict(vert_num=len(verts)))
        np.savetxt(f, verts, '%f %f %f %d %d %d')

if __name__ == '__main__':
    print __doc__
    
    def nothing(*arg):
        pass

    # create windows
    cv2.namedWindow('camLeft')
    cv2.namedWindow('camRight')
    cv2.namedWindow('disparity')
    cv2.namedWindow('tools')
    
    # create trackbar tools
    cv2.createTrackbar('uniqRat', 'tools', 10, 20, nothing)
    cv2.createTrackbar('spcklWinSize', 'tools', 100, 250, nothing)
    cv2.createTrackbar('disp12MazDiff', 'tools', 1, 5, nothing)
    

    #set up video captures
    capL = video.create_capture(camLeft)
    capR = video.create_capture(camRight)
    
    #cv2.waitKey()
    #time.sleep(6)
    
    while True:
    	print 'top of capture/compute loop'
    	#get video frames
        flagL, imgL = capL.read()
        flagR, imgR = capR.read()
        
        #display images
        cv2.imshow('camLeft', imgL)
        cv2.imshow('camRight', imgR)
        
        # downscale images for faster processing
        imgLds = cv2.pyrDown( imgL )
        imgRds = cv2.pyrDown( imgR )

        # disparity range is tuned for 'aloe' image pair
        window_size = 3 #size of blocks for matching
        min_disp = 16
        num_disp = 112-min_disp
        stereo = cv2.StereoSGBM(
    	    minDisparity = min_disp, 
            numDisparities = num_disp, 
            SADWindowSize = window_size,
            uniquenessRatio = cv2.getTrackbarPos('uniqRat', 'tools'),
            speckleWindowSize = cv2.getTrackbarPos('spcklWinSize', 'tools'),
            speckleRange = 32,
            disp12MaxDiff = cv2.getTrackbarPos('disp12MaxDiff', 'tools'),
            P1 = 8*3*window_size**2,
            P2 = 32*3*window_size**2,
            fullDP = False
        )

        print 'computing disparity...'
        disp = stereo.compute(imgLds, imgRds).astype(np.float32) / 16.0
    
        print 'generating 3d point cloud...'
        h, w = imgL.shape[:2]
        f = 0.8*w                          # guess for focal length
        Q = np.float32([[1, 0, 0, -0.5*w],
                        [0,-1, 0,  0.5*h], # turn points 180 deg around x-axis, 
                        [0, 0, 0,     -f], # so that y-axis looks up
                        [0, 0, 1,      0]])
        points = cv2.reprojectImageTo3D(disp, Q)
        #get colors from left image
        colors = cv2.cvtColor(imgL, cv2.COLOR_BGR2RGB)
        mask = disp > disp.min()
        out_points = points[mask]
        out_colors = colors[mask]
        out_fn = 'out.ply'
        # write file
        write_ply('out.ply', out_points, out_colors)
        print '%s saved' % 'out.ply'

        # display disparity map
        dispUs = cv2.pyrUp( ((disp-min_disp)/num_disp) )
        cv2.imshow('disparity', dispUs)
        #cv2.imshow('disparity', (disp-min_disp)/num_disp)
        
        # detect keypresses
        ch = cv2.waitKey(5)
        if ch == 27:
            # exit on 'escape' key
            break
    cv2.destroyAllWindows() 