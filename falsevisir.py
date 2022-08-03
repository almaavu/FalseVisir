#!/usr/bin/env python3
'''
Combine infrared and visible light images of the same object to false colors automatically.

Input: file paths of visible light image (RGB) and infrared image (RGB or grey)

Process:
- resize images to same height
- warp images to fit when overlayed (images must have similar features, otherwise it may fail)
- combine images to false colors - R channel from IR image, 
    G channel from VIS-R and B channel from VIS-G (VIS-B is discarded)
- blend images (50 % IR, 50 % VIS)

Output:
- False color image
- Blend image
- VIS image resized and warped
- IR image resized and warped


TODO:
- remove first resize step? 



resources:
https://en.wikipedia.org/wiki/False_color
https://chsopensource.org/infrared-false-color-photography-irfc/    
https://en.wikipedia.org/wiki/Affine_transformation
'''
import sys
from pathlib import Path
import logging
import time
from functools import update_wrapper
import json

from imageio import imwrite, imread
import numpy as np
import matplotlib.pyplot as plt
import skimage as sk
from skimage import img_as_float, img_as_ubyte
from skimage.color import rgb2gray
from skimage import transform, exposure, feature
from scipy.ndimage.filters import gaussian_filter
import cv2
from config import CFG    
    


# TIMEIT DECORATOR ----------------------------------------

def decorator(d):
    'Make function d a decorator: d wraps a function fn.'
    def _d(fn):
        return update_wrapper(d(fn), fn)
    update_wrapper(_d, d)
    return _d

@decorator
def timeit(f):
    '''Usage: decorate function with @timeit to log its execution time'''
    def new_f(*args, **kwargs):
        bt = time.time()
        r = f(*args, **kwargs)
        et = time.time()
        logging.debug(f'timeit: {f.__qualname__}: {et - bt:.2f}s')
        return r
    return new_f


# HELPER FUNCTIONS ----------------------------------------

def load_image(fpath):
    '''Load image from file to float numpy array.'''
    logging.info(f'Load image {fpath}')
    return img_as_float(imread(str(fpath)))

def save_image(fpath, im):
    '''Save numpy array as 8bit image.'''
    logging.info(f'Save image {fpath}')
    imwrite(fpath, img_as_ubyte(im))

def show_images(images, labels=None, **kw):
    '''Display images side by side.
    image0, image1, image2, ... : list of ndarrrays
    labels : list
    '''
    logging.info(f'show images... {labels}')
    if type(images) not in (list, tuple):
        images = [images]
        labels = [labels]
    f, axes = plt.subplots(1, len(images), **kw)
    axes = np.array(axes, ndmin=1)

    if labels is None:
        labels = [''] * len(images)

    for n, (image, label) in enumerate(zip(images, labels)):
        axes[n].imshow(image, interpolation='nearest', cmap='gray', vmin=0, vmax=1)
        axes[n].set_title(label)
        axes[n].axis('off')
    plt.show()

def info(im, name=''):
    '''Print basic numpy array info.'''
    i = f'shape: {im.shape} dtype: {im.dtype} min--max: {im.min():.3f}--{im.max():.3f}'
    logging.debug(f'info: *** {name} *** ... {info}')
    return i
    

        
# OVERLAY IMAGES ----------------------------------------

def blend_image(vis, irr, weight=.5):
    '''Make weighted average of two images.'''
    logging.info('Blend images...')
    if irr.ndim == 2 :
        irr = np.dstack((irr,irr,irr))          # to grey rgb
    im = (1 - weight) * vis + weight * irr     # weight average
    return im

def false_image(vis, irr):
    '''Make false color image
    vis: RGB image array
    irr: grey or RGB image array
    result: image array with channels: IRR, R, G (blue channel is dropped)
    '''
    logging.info('Make false images...')
    if irr.ndim > 2:
        irr = rgb2gray(irr)
    im = np.dstack((irr, vis[:,:,0], vis[:,:,1]))
    return im


# WARP FUNCTIONS ----------------------------------------

def warp_image(images, model_robust):

    r, c = images[0].shape[:2]

    corners = np.array([[0, 0],
                        [0, r],
                        [c, 0],
                        [c, r]])

    logging.debug('warp_corners...')
    warped_corners = model_robust(corners)

    logging.debug('stack_corners...')
    all_corners = np.vstack((warped_corners, corners))

    corner_min = np.min(all_corners, axis=0)
    corner_max = np.max(all_corners, axis=0)

    output_shape = (corner_max - corner_min)
    output_shape = np.ceil(output_shape[::-1])

    logging.debug('SimilarityTransform....')

    offset = transform.SimilarityTransform(translation=-corner_min)
    logging.debug(f'{images[1].min(), images[1].max()}')
    logging.debug('warp... im0')

    warp_0 = transform.warp(images[0], offset.inverse,
                       output_shape=output_shape, cval=0)

        
    logging.debug('warp... im1')
    warp_1 = transform.warp(images[1], (model_robust + offset).inverse,
                   output_shape=output_shape, cval=0)

    return warp_0, warp_1

def resize_images(images, new_height=None, method="scipy", **kw):
    '''Resize images to same height.'''
    
    logging.info(f'Resize images...')
    heights = [im.shape[0] for im in images]
    new_height = new_height or min(heights)
    logging.debug(f'image heights {heights} \t  new height {new_height}')
    # images1 = [transform.resize(im, (new_height, im.shape[1]*new_height//im.shape[0])) for im in images]
    images1 = []
    
    for im in images:
        newshape = np.array((new_height, im.shape[1] * new_height // im.shape[0]))
        im = fast_downscale(im, newshape*2)  # fast resize to cca double of target size 
        
        logging.info(f"resize image {im.shape} -> {newshape}")
        # 
        if method == "scipy":
            
            images1.append(transform.resize(im, newshape))
        else:    
            images1.append(cv2.resize(im, dsize=newshape),interpolation=cv2.INTER_AREA)
    return images1

def resize_images_to_same_size(images):
    
    shapes = np.array([im.shape[:2] for im in images])
    new_shape = np.min(shapes, axis=0)
    # print(shapes, new_shape)
    images = [fast_downscale(im, new_shape * 2) for im in images] 
    resized = [transform.resize(im, new_shape) for im in images]
    return resized
    
# def test_resize_images_to_same_size():
    # fps =  ("/home/m/Y/APOLLO/2022/J1828/a393_J1828__TF_90.png","/home/m/Y/APOLLO/2022/J1828/J1828 3200.png")
    # images = [imread(fp) for fp in fps]   
    # images = resize_images_to_same_size(images)
    # for im, fp in zip(images, fps):
        # imwrite(fp + "_2.png", im)
        
def fast_downscale(im, newsize):
    '''Fast resize numpy array by slicing as much as possible to target size. 
    Returned array size >= newsize'''
    from math import floor
    old = np.array(im.shape[:2])
    new = newsize
    r = floor(min(old / new))
    if r < 2:
        return im
    else:    
        logging.info(f"fast downscale {im.shape} by slicing: {r}")
        im2 = im[::r,::r,...]
        return im2
        
# def test_fast_downscale():
    # im = np.arange(1,101).reshape((10,10))
    # newsize = (6,5)
    # print(fast_downscale(im, newsize))
    
    
    
def transformation_valid(model_robust, valid_params):
    '''Check if transformation was found and is withing allowed bounds (prevent excessive deformation).'''
    
    if np.isnan(model_robust.params).any():
        return False
    
    # check if all parameters are in bounds     
    mmin, mmax = valid_params
    valid = (model_robust.params > mmin).all() and (model_robust.params < mmax).all()
    
    return valid
  
def preprocess_images(images, blur_sigma=None, normalize=None, equalize=None, edge=None, edge_sigma=None, edge_low_threshold=None,  edge_high_threshold=None, show=False):
    
    # TO GRAY 
    # images_gray = [rgb2gray(im) if im.ndim > 2 else im for im in images]
    images_gray = [im[:,:,0] if im.ndim > 2 else im for im in images] # from VIS image use red channel to match features  - most similar to IRR
    
    # SMOOTH
    if blur_sigma:
        images_gray = [gaussian_filter(im, sigma=blur_sigma) for im in images_gray]
    
    # NORMALIZE 
    if normalize:
        logging.debug('apply normalize filter....')
        images_gray = [exposure.rescale_intensity(im, in_range='image', out_range='dtype') for im in images_gray]
    
    # EQUALIZE 
    if equalize:
        logging.debug('apply equalize filter....')
        images_gray = [exposure.equalize_hist(im) for im in images_gray]
        
    # EDGE DETECTION     
    if edge:
        logging.debug('apply edge filter....')
        images_gray = [feature.canny(im, sigma=edge_sigma, low_threshold=edge_low_threshold, high_threshold=edge_high_threshold) for im in images_gray]

        
    if show:
        show_images(images_gray, labels=['downsized VIS','downsized IR'])
    
    return images_gray
        
    
    
def warp_images(vis, irr, show=False, **kw):
    '''Warp images.'''
    logging.info('Warp images...')
    assert vis.ndim == 3 # RGB
    if irr.ndim > 2:     # RGB or L
        irr = irr[:,:,0]

    images = vis, irr

    orig_height = images[0].shape[0]
    print("...warping... downsize to:", CFG['downsize'])
    images_small = resize_images(images, new_height=CFG['downsize'])
    downsize_scale = CFG['downsize'] / orig_height
    logging.debug('preprocess images...')
    images_gray = preprocess_images(images_small, show=show, **CFG['preprocess_images'])

    logging.debug('find_keypoints...')
    keypoints, descriptors = extract(images_gray, **CFG['extract_features'])
    logging.debug(f'{len(keypoints[0]), len(keypoints[1])}')

    logging.info('Find_matches...')
    matches = feature.match_descriptors(*descriptors, cross_check=True, **CFG['match'])  # slow
    logging.debug(f'found: {len(matches)} matches')

    if show:
        show_matches(images_gray, keypoints, matches, 'all matches')
        print(f"All matches: {len(matches)}")
        logging.debug(keypoints)
        logging.debug(matches)

    # CALC TRANSFORMATION
    src_keys = keypoints[1][matches[:, 1]][:, ::-1]
    dst_keys = keypoints[0][matches[:, 0]][:, ::-1]

    model_robust, inliers = sk.measure.ransac(
            (src_keys, dst_keys),
            transform.ProjectiveTransform, **CFG['ransac'])

       
    if show:
        show_matches(images_gray, keypoints, matches[inliers], 'good matches')
        print(f"Good matches: {len(matches[inliers])}")
        
    logging.debug(f'model robust parameters: {model_robust.params}')
    
    if not transformation_valid(model_robust, CFG['model_robust_param_limits']):
        raise ValueError('Transformation failed, not enough similar features?')    
#    logging.debug(model_robust)

    # RESCALE TRANSFORMATION
    S_down = transform.SimilarityTransform(scale=downsize_scale)
    S_up = transform.SimilarityTransform(scale=1/downsize_scale)
    full_tf = S_down + model_robust + S_up


    vis, irr =  warp_image(images, full_tf)

    if show:
        show_images([vis, irr], labels=['VIS','IR'])

    return vis, irr


def show_matches(images, keypoints, matches, label=''):
    '''For debugging only: show matched points of transformation.'''
    from skimage.feature import plot_matches
    fig, ax = plt.subplots(1, 1, figsize=(5, 5))
    plot_matches(ax, *images, *keypoints, matches)
    plt.title(label)
    plt.axis('off')
    plt.show()


def select_matches(keypoints, matches, min_samples=4, residual_threshold=3, max_trials=1000, **kw):
    '''Select best keypoint pairs matches to be used for transformation.'''
    src = keypoints[1][matches[:, 1]][:, ::-1]
    dst = keypoints[0][matches[:, 0]][:, ::-1]

    model_robust, inliers = sk.measure.ransac(
            (src, dst),
            transform.ProjectiveTransform,
            min_samples=min_samples,
            residual_threshold=residual_threshold,
            max_trials=max_trials)
    return model_robust, inliers


def extract(images, method='HARRIS', min_distance = 1, threshold_rel = 1e-7, patch_size=59, **kw):
    '''Find keypoints in both images.'''
    logging.debug(f'extract images, method: {method}, kw: {kw}')

    keypoints = []
    descriptors = []

    if method == 'ORB':
        orb = feature.ORB(n_keypoints=1000, fast_threshold=0.02)
        for im in images:
            orb.detect_and_extract(im)
            keypoints.append(orb.keypoints)
            descriptors.append(orb.descriptors)

    elif method == 'HARRIS':
        # https://www.kite.com/python/docs/skimage.feature.BRIEF
        brief = feature.BRIEF(patch_size=patch_size, mode='uniform')
        for im in images:
            logging.debug(f'{im.shape}')
            keypoints1 = feature.corner_peaks(feature.corner_harris(im), min_distance=min_distance,
                              threshold_rel=threshold_rel)
            brief.extract(im, keypoints1)
            keypoints.append(keypoints1[brief.mask])
            descriptors.append(brief.descriptors)

    return keypoints, descriptors



def process_pair(vi_path, ir_path, show=True, save=True, dst_dir=None, overwrite=False, warp=True):
    logging.info(f"process pair {vi_path} {ir_path}")
    vi_path = Path(vi_path)
    ir_path = Path(ir_path)
    ds = CFG["downsize"]
    dst_dir = dst_dir or ir_path.parent / f'false_color_results_{ds}'
    
    irfc_out = dst_dir / f'{ir_path.stem}_{vi_path.stem}_falsecolor.png'
    blend_out = dst_dir / f'{ir_path.stem}_{vi_path.stem}_blend.png'
    vi_out = dst_dir / f'{ir_path.stem}_{vi_path.stem}_vi_warp.png'
    ir_out = dst_dir / f'{ir_path.stem}_{vi_path.stem}_ir_warp.png'
    
    if irfc_out.is_file() and not overwrite:  # skip if already done
        print(f"destination file exists, exit: {irfc_out}")
        return
    
    # Load images
    vi_image, ir_image = [load_image(fp) for fp in (vi_path, ir_path)]


    if warp:
        # Resize to same height
        vi_image, ir_image = resize_images((vi_image, ir_image))
        # Warp images
        vi_image, ir_image = warp_images(vi_image, ir_image, show=False)
    else:
        vi_image, ir_image = resize_images_to_same_size((vi_image, ir_image))
        
        
    info(ir_image, 'ir_image')

    # Blend images
    blend_im = blend_image(vi_image, ir_image, weight=.5)
    info(blend_im, 'blend_im')

    # False color image
    false_im = false_image(vi_image, ir_image)
    info(false_im, 'false_im')

    # Show results
    if show:
        show_images((vi_image, ir_image, blend_im, false_im), labels=('VIS', 'IR', 'BLEND', 'FALSE_COLOR'))

    # Save results
    if save:
           
        dst_dir.mkdir(exist_ok=True)

        save_image(irfc_out, false_im)
        save_image(ir_out, ir_image)
        save_image(vi_out, vi_image)
        save_image(blend_out, blend_im)

    return vi_image, ir_image, blend_im, false_im


def parse_args():

    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--downsize", type=int, default=500,
                    help="downsize image to speedup processing")
    parser.add_argument("-i", "--ir-image", type=str,
                    help="path of ir image")
    parser.add_argument("-v", "--vis-image", type=str,
                    help="path of vis image")
    parser.add_argument("-n", "--no-warp", action='store_true',
                    help="only resize images, no warping (use when warping fails)")

    args = parser.parse_args()
    # args_dict = vars(args)

    return args



#%% Main program =============================================================================================

if __name__ == '__main__':
    

    # LOGLEVEL = logging.DEBUG
    LOGLEVEL = logging.INFO
    SAMPLES = ('samples/vis_samples/a001_vis_image.jpg', 'samples/ir_samples/a001_ir_image.jpg')

    logging.basicConfig(
        level=LOGLEVEL, format='!%(levelno)s [%(module)10s %(lineno)4d]\t%(message)s')
    logging.getLogger('matplotlib.font_manager').disabled = True
    logging.debug(f'Script started...')
    start = time.time()

    args = parse_args()
    print(args)
    CFG["downsize"] = args.downsize
    
    im_paths = (args.vis_image, args.ir_image) if (args.ir_image and args.vis_image) else SAMPLES
    im_paths = [Path(fp).resolve() for fp in im_paths]
    vi_path, ir_path = im_paths
    print(vi_path, ir_path)
    warp = not args.no_warp
    process_pair(vi_path, ir_path, show=True, save=True, warp=warp)

    logging.debug(f'Script finished in {time.time() - start:.1f} s')
