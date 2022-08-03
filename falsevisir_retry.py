#!/usr/bin/env python3
'''
Run falsevisir with different downsize parameter to get best result for a pair.
'''
from pathlib import Path
import logging
import time


from falsevisir import process_pair
from config import CFG   


def parse_args():

    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--downsize", type=int, default=500,
                    help="downsize image to speedup processing")
    parser.add_argument("-i", "--ir-image", type=str,
                    help="path of ir image")
    parser.add_argument("-v", "--vis-image", type=str,
                    help="path of vis image")

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
    
    downsizes = list(range(750,1000,50))
    print(downsizes)
    
    args = parse_args()
    print(args)
    
    
    im_paths = (args.vis_image, args.ir_image) if (args.ir_image and args.vis_image) else SAMPLES
    im_paths = [Path(fp).resolve() for fp in im_paths]
    vi_path, ir_path = im_paths
    print(vi_path, ir_path)
    
    for downsize in downsizes:    
        CFG["downsize"] = downsize
        try:
            process_pair(vi_path, ir_path, show=False, save=True)
        except ValueError as e:
            print(e)    

    logging.debug(f'Script finished in {time.time() - start:.1f} s')
