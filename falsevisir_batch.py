#!/usr/bin/env python3
'''

'''
import sys
from pprint import pprint
from pathlib import Path

from tqdm import tqdm

from falsevisir import process_pair


def get_files_dict(src_dir, extensions=[".png"], id_pattern=r"(\w+?)_.*"):
    '''
    Find files recursivelly by extension, 
    get file id from filename, 
    store it in dictionary {file_id1 : filepath1, ...}
    example: 
        a212_vis_image.png ->  {"a212" : "a112_vis_image.png", ...}
    '''
    
    src_dir = Path(src_dir)
    fs = [f for f in src_dir.rglob("*.*") if f.suffix in extensions]
    #print(fs)
    regex = re.compile(id_pattern)
    file_dict = {}
    for f in fs:
        # print(f.stem)
        if regex.match(f.stem):
            file_id = regex.match(f.stem).group(1).lower()
            # print(file_id)
            file_dict[file_id] = f.resolve()
    file_dict = dict(sorted(file_dict.items()))
    return file_dict


def main():



    SAMPLES  = "samples/vis_samples", "samples/ir_samples"

    src_dir_vis, src_dir_irr = sys.argv[1:3] if len(sys.argv) == 3 else SAMPLES

    src_dir_vis, src_dir_irr  = Path(src_dir_vis), Path(src_dir_irr)  
        
    irr_files = get_files_dict(src_dir_irr, extensions=(".png", ".jpg"))
    vis_files = get_files_dict(src_dir_vis, extensions=(".png", ".jpg"))
    print(irr_files)
    print(vis_files)

    for file_id in tqdm(irr_files):
        vi_path, ir_path = vis_files[file_id], irr_files[file_id]
        print(f"--------- PROCESS PAIR... ID: {file_id} VIS: {vi_path}  IRR: {ir_path}-------------")
        if not file_id in vis_files:
            print(f"============== VIS file missing: {file_id}  ================") 
        else:    
            try:
                process_pair(vi_path, ir_path, show=False, save=True, dst_dir=src_dir_vis.parent / "false_color_results")
            except Exception as e:
                print(f"=================== FAILED: {file_id}  ===================\n{e}")

    print(f"{Path(__file__).resolve()} finished")


if __name__ == "__main__":
    main()

