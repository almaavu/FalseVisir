# falsevisir
https://github.com/almaavu/falsevisir

**Combine infrared and visible light images of the same object to false colors automatically.**


---

## Install:

Python3

    https://www.python.org/downloads/
    
falsevisir

    python -m pip install --upgrade git+https://github.com/almaavu/falsevisir.git#egg=falsevisir

Dependencies:

    python -m pip install --upgrade requirements.txt
    
* numpy
* matplotlib
* scikit-image
* imageio

---




### Input: 
file paths of visible light image (RGB) and infrared image (RGB or grey)


### Process:
- resize images to same height
- warp images to fit when overlayed (images must have similar features, otherwise it may fail)
- combine images to false colors - R channel from IR image, 
    G channel from VIS-R and B channel from VIS-G (VIS-B is discarded)
- blend images (50 % IR, 50 % VIS)


### Output:
- False color image
- Blend image
- VIS image resized and warped
- IR image resized and warped


## Usage:

    python -m falsevisir "vis_soubor.jpg" "ir_soubor.jpg"  
    
Without installation:

    python falsevisir.py "vis_soubor.jpg" "ir_soubor.jpg" 

In Jupyter notebook:

    jupyter notebook falsevisir_jupyter.ipynb

Batch processing: 

    python falsevisir_batch.py "samples/vis_samples/" "samples/ir_samples/" 
    
    


### resources:

https://en.wikipedia.org/wiki/False_color

https://chsopensource.org/infrared-false-color-photography-irfc/

https://en.wikipedia.org/wiki/Affine_transformation


---

## Example:

### Source:
<p align="center">
  <img src="samples/vis_samples/a001_vis_image.jpg" width="150" title="">
  <img src="samples/ir_samples/a001_ir_image.jpg" width="150" alt="">
</p>

### Result:
False color image
<p align="center">
  <img src="samples/false_color_results/a001_ir_image_a001_vis_image_falsecolor.png" width="150">
</p>
Blend
<p align="center">
  <img src="samples/false_color_results/a001_ir_image_a001_vis_image_blend.png" width="150">
</p>
Warped images
<p align="center">
  <img src="samples/false_color_results/a001_ir_image_a001_vis_image_ir_warp.png" width="150">
    <img src="samples/false_color_results/a001_ir_image_a001_vis_image_vi_warp.png" width="150">
</p>

---
