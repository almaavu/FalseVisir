
# falsevisir
https://github.com/almaavu/falsevisir

**Program pro automatické vytvoření obrazu ve falešných barvách spojením snímků ve viditelném a infračerveném světle.**



Zobrazení ve falešných barvách je technika zpracování obrazu používaná při průzkumu uměleckých děl (např. závěsných obrazů, nástěnných maleb, polychromovaných plastik). Pro vyhodnocení je vhodné porovnat snímky získané infračervenou reflektografií (IRR) se snímky ve viditelném světle (VIS). Spojení obou obrazů do snímku ve falešných barvách může pomoci při studiu podmalby nebo pro identifikaci některých pigmentů. [[1]](#1), [[2]](#2).

Ve výsledném obrazu jsou RGB kanály využity takto:
```
    IRR   -> R
    Vis R -> G
    Vis G -> B
    Vis B ->  
```
Pro složení snímků jsou obvykle využívány grafické editory (Adobe Photoshop, GIMP, ...). Snímky jsou zobrazeny přes sebe, pro přesný překryv je obvykle je nutné je transformovat a napravit tak zkreslení způsobené rozdíly v geometrii zobrazení a použitých objektivech. 

Pokud mají oba snímky podobné rysy, je možné je provést transformaci a následné složení do falešných barev automaticky. To je výhodné zejména při zpracování většího počtu snímků.   

---

## Instalace:

Instalace programovacího jazyka Python3

    https://www.python.org/downloads/
    
Instalace programu falsevisir

    python -m pip install git+https://github.com/almaavu/falsevisir.git
    
    
Instalace knihoven:

    python -m pip install --upgrade requirements.txt
    
* numpy
* matplotlib
* scikit-image
* imageio

---

## Použití:

Program lze spustit z příkazového řádku se zadáním cesty ke vstupním souborům - obrázku ve viditelném a infračerveném světle.

    python -m falsevisir vis_soubor.jpg ir_soubor.jpg  
    
Skript je možné spustit i bez instalace:

    python falsevisir.py vis_soubor.jpg ir_soubor.jpg 

Program je také možné spustit interaktivně v prostředí Jupyter notebook:

    jupyter notebook falsevisir-jupyter.ipynb

### Vstupní data:
Cesta a název souboru snímku ve viditelném světla (formát RGB) a infračerveného snímku (formát RGB nebo stupně šedé)

### Funkce programu:
- Změna velikosti obrázků na stejnou výšku
- Transformace snímků pro přesné překrytí - oprava rozdílů v natočení, perspektivním zkreslení, zkreslení různých objektivů apod. (obrázky musí mít podobné rysy, jinak  může selhat) [[3]](#3)
- Spojení obrazů do falešných barev (IRR-R-G)
- Prolnutí obrazů (50% IRR, 50% VIS)
- Uložení výsledků

### Výstup:
- Snímek ve falešných barvách
- Snímek s překrytými snímky v IR a VIS světle (50 % IR + 50 % VIS)
- Transformované snímky v IR a VIS světle (se snímky lze dále pracovat, např. pro vytvoření prolnutí s jinými parametry)

---

## Ukázka:

### Zdrojové obrázky:
<p align="center">
  <img src="samples/vis_image.jpg" width="150" title="">
  <img src="samples/ir_image.jpg" width="150" alt="">
</p>

### Výsledek:
Obraz ve falešných barvách
<p align="center">
  <img src="samples/false_color_results/a001_ir_image_a001_vis_image_falsecolor.png" width="150">
</p>
Prolnutí
<p align="center">
  <img src="samples/false_color_results/a001_ir_image_a001_vis_image_blend.png" width="150">
</p>
Transformované snímky
<p align="center">
  <img src="samples/false_color_results/a001_ir_image_a001_vis_image_ir_warp.png" width="150">
    <img src="samples/false_color_results/a001_ir_image_a001_vis_image_vi_warp.png" width="150">
</p>

---

### Odkazy:
<a id="1">[1]</a> 
https://en.wikipedia.org/wiki/False_color

<a id="2">[2]</a> 
[Cosentino, A. Identification of pigments by multispectral imaging; a flowchart method. herit sci 2, 8 (2014). https://doi.org/10.1186/2050-7445-2-8](https://heritagesciencejournal.springeropen.com/articles/10.1186/2050-7445-2-8)

<a id="3">[3]</a> 
https://en.wikipedia.org/wiki/Affine_transformation
