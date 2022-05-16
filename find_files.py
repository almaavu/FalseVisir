#!/usr/bin/env python3
'''

'''
import sys
from pprint import pprint
from pathlib import Path
import re

from tqdm import tqdm

from falsevisir import process_pair


def get_files_dict(src_dir, extensions=[".png"], id_pattern=r"(\w+?)_.*", exclude=None, id_to_lowercase=True):
    '''
    Find files recursivelly by extension, 
    get file id from filename by regex pattern, convert to lowercase (A001 => a001)
    store it in dictionary {file_id1 : filepath1, ...}
    example: 
        A212_vis_image.png ->  {"a212" : "A112_vis_image.png", ...}
    '''
    
    src_dir = Path(src_dir)
    fs = [f for f in src_dir.rglob("*.*") if f.suffix in extensions]
    #print(fs)
    regex = re.compile(id_pattern)
    file_dict = {}
    for f in fs:
        # print(f.stem)
        if regex.match(f.stem):
            if exclude:
                if re.match(exclude, str(f)):
                    continue
            file_id = regex.match(f.stem).group(1)
            if id_to_lowercase:
                file_id = file_id.lower()
            # print(file_id)
            file_dict.setdefault(file_id, []).append(f.resolve())
    file_dict = dict(sorted(file_dict.items()))
    return file_dict



def main():



    INDIRS  =  "/home/m/Y/SKENY/VIS/", "/home/m/Y/APOLLO/2021/"

    # indirs from command line
    src_dir_vis, src_dir_irr = sys.argv[1:3] if len(sys.argv) == 3 else INDIRS

    src_dir_vis, src_dir_irr  = Path(src_dir_vis), Path(src_dir_irr)  
        
    # get files dictionaries {id1 : filepath1, ...}
    irr_files = get_files_dict(src_dir_irr, extensions=[".png"], id_pattern=r".*?_(\w{5})_.*")
    vis_files = get_files_dict(src_dir_vis, extensions=[".tif"], id_pattern=r"(\w{5}).*", exclude=r".*(spod|zad|reverz|rub).*")  # exclude zadni strana
    
    pprint(irr_files)
    pprint(vis_files)



if __name__ == "__main__":
    main()

