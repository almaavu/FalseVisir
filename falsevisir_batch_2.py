#!/usr/bin/env python3
'''

'''
import sys
from pprint import pprint
from pathlib import Path
import re
import logging

from tqdm import tqdm

from falsevisir import process_pair
from find_files import get_files_dict

from config import CFG    


def main():

    CFG["downsize"] = 600
    

    INDIRS  =  "/home/m/Y/SKENY/VIS/", "/home/m/Y/APOLLO/2022/"


    LOGLEVEL = logging.INFO
    logging.basicConfig(
        level=LOGLEVEL, format='!%(levelno)s [%(module)10s %(lineno)4d]\t%(message)s')
    logging.getLogger('matplotlib.font_manager').disabled = True
    

    # indirs from command line
    src_dir_vis, src_dir_irr = sys.argv[1:3] if len(sys.argv) == 3 else INDIRS

    src_dir_vis, src_dir_irr  = Path(src_dir_vis), Path(src_dir_irr)  
        
    # get files dictionaries {id1 : filepath1, ...}
    irr_files = get_files_dict(src_dir_irr, extensions=[".png"], id_pattern=r".*?_(\w{5})_.*", exclude=r".*false_color.*")
    vis_files = get_files_dict(src_dir_vis, extensions=[".tif"], id_pattern=r"(\w{5}).*", exclude=r".*(spod|zad|reverz|rub|back).*")  # exclude zadni strana
    
    pprint(irr_files)
    pprint(vis_files)

    for file_id in tqdm(irr_files):

        if not file_id in vis_files:
            print(f"... VIS file missing: {file_id} ") 
            continue
        
        for ir_path in irr_files[file_id]:
        
            vi_path = vis_files[file_id][-1]
            print(f"'{ir_path}', '{vi_path}'")   
            try:
                process_pair(vi_path, ir_path, show=False, save=True, dst_dir=ir_path.parent / "false_color_results")
            except Exception as e:
                raise(e)
                print(f"... FAILED: {file_id} \n{e}")

    print(f"{Path(__file__).resolve()} finished")


if __name__ == "__main__":
    main()

