
# Alma FalseVisir
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

Příklad složení snímku v infračerveném světle s červeným a zeleným kanálem snímku ve viditelném světle:
<TABLE>
   <TR>
      <TD>IRR</TD>
      <TD><img src="samples/false_color_results/a002_s002__TL_a002_palette_ir_warp.png" width="150"></TD>
      <TD colspan="3" align="center" style="text-align: center; vertical-align: middle;"></TD>
   </TR>
   <TR>
      <TD>VIS</TD>
      <TD></TD>
      <TD colspan="3" align="center" style="text-align: center; vertical-align: middle;"><img src="samples/false_color_results/a002_s002__TL_a002_palette_vi_warp.png" width="150"></TD>
   </TR>
   <TR>
      <TD>VIS R G B</TD>  
      <TD></TD>
      <TD><img src="samples/false_color_results/a002_s002__TL_a002_palette_vi_warp_0.png" width="150"></TD>
      <TD><img src="samples/false_color_results/a002_s002__TL_a002_palette_vi_warp_1.png" width="150"></TD>
      <TD><img src="samples/false_color_results/a002_s002__TL_a002_palette_vi_warp_2.png" width="150"></TD>
   </TR>
      <TR>
      <TD>False color R G B</TD>
      <TD><img src="samples/false_color_results/a002_s002__TL_a002_palette_ir_warp.png" width="150"></TD>
      <TD><img src="samples/false_color_results/a002_s002__TL_a002_palette_vi_warp_0.png" width="150"></TD>
      <TD><img src="samples/false_color_results/a002_s002__TL_a002_palette_vi_warp_1.png" width="150"></TD>
      <TD></TD>
   </TR>
   <TR>
      <TD>False color</TD>
      <TD colspan="3" align="center" style="text-align: center; vertical-align: middle;"><img src="samples/false_color_results/a002_s002__TL_a002_palette_falsecolor.png" width="150"></TD>
      <TD></TD>
   </TR>
</TABLE>




Pro složení snímků jsou obvykle využívány grafické editory (Adobe Photoshop, GIMP, ...). Snímky jsou zobrazeny přes sebe, pro přesný překryv je obvykle je nutné je transformovat a napravit tak zkreslení způsobené rozdíly v geometrii zobrazení (natočení, perspektivní zkreslení) a použitých objektivech (soudkovité zkreslení). 

Pokud mají oba snímky podobné rysy, je možné transformaci a následné složení do falešných barev provést automaticky programem FalseVisir. To je výhodné zejména při zpracování většího počtu snímků.   


---

## Instalace:

Instalace programovacího jazyka **Python3**

    https://www.python.org/downloads/
    
Instalace programu **FalseVisir**

    python -m pip install --upgrade git+https://github.com/almaavu/falsevisir.git#egg=falsevisir

    
    
Instalace knihoven:

    python -m pip install --upgrade requirements.txt
    
* numpy
* matplotlib
* scikit-image
* scipy
* imageio

---

### Licence:

Program je uvolněn pod licencí GNU General Public License 3.0 (GNU GPL), lze jej používat zdarma pro soukromé i pro komerční účely. 
https://cs.wikipedia.org/wiki/GNU_General_Public_License

---

## Použití:

### Příkazový řádek

Program lze spustit z příkazového řádku se zadáním cesty ke vstupním souborům - obrázku ve viditelném a infračerveném světle.

    python -m falsevisir -v "vis_soubor.jpg" -i "ir_soubor.jpg"    
    
Skript je možné spustit i bez instalace:

    python falsevisir.py -v "vis_soubor.jpg" -i "ir_soubor.jpg" pg" 
    
  

#### Vstupní data:
Cesta a název souboru snímku ve viditelném světla (formát RGB) a infračerveného snímku (formát RGB nebo stupně šedé). Snímky by měly být oříznuté na přibližně stejný výřez (bez přehnaně širokých okrajů). Mohou být různě pootočené (viz ukázky).


#### Hromadné zpracování:

Program **falsevisir_batch.py** je určený pro hromadné zpracování většího počtu obrázků. Program načte snímky ze zvolených složek a zpracuje páry souborů podle ID souborů, které musí být uvedeno na začátku názvu následované podtržítkem. Zpracuje např. soubory "a001_vis_image.jpg" a "a001_ir_image.jpg". 

    python falsevisir_batch.py "samples/vis_samples/" "samples/ir_samples/"  



### Jupyter notebook

Program je také možné spustit interaktivně v prostředí Jupyter notebook, to je výhodné v případě, kdy je potřeba sledovat jednotlivé kroky zpracování obrazů, např. při úpravě  nastavení konfigurace programu. 

    jupyter notebook falsevisir_jupyter.ipynb


Změna konfigurace v prostředí Jupyter notebook:

<img src="samples/jupyter/jupyter_sample1.png" width="800" title="">


Kontrola průběhu transformace:

<img src="samples/jupyter/jupyter_sample2.png" width="800" title="">

Nezdařená transformace při nastavení parametru preprocess_images - edge:

<img src="samples/jupyter/jupyter_sample3.png" width="800" title="">


### Použití ve formě knihovny

Program je možné začlenit jako knihovnu do jiného programu v jazyce Python3:
    
    from falsevisir import process_pair
    process_pair("vis_soubor.jpg", ir_soubor.jpg, show=False, save=True, cfg=CFG) 
    
Ukázka importu: [falsevisir_batch.py](falsevisir_batch.py)    

### Funkce programu:
- Změna velikosti obrázků na stejnou výšku
- Transformace snímků pro přesné překrytí - oprava rozdílů v natočení, perspektivním zkreslení, zkreslení různých objektivů apod. (obrázky musí mít podobné rysy, jinak  může selhat) [[3]](#3)
- Spojení obrazů do falešných barev (IRR-R-G)
- Prolnutí obrazů (50% IRR, 50% VIS)
- Uložení výsledků


### Konfigurace:
Parametry jsou uloženy v globální proměnné CFG. Jejich úprava může být užitečná, pokud program nenajde správnou transformaci.
- _downsize_: výška zmenšeného obrázku v pixelech. Zmenšené snímky program používá pro urychlení výpočtu transformace. Změna velikosti může pomoci, když transformace selže. Vyšší hodnota vede k pomalejšímu výpočtu, výchozí hodnota: 500 pix.  
- _preprocess_images_: Před výpočtem transformace je lze provést úpravu jasu a kontrastu ("normalize"), equalizaci histogramu ("equalize") nebo detekci hran ("edge")
- _extract_features_: parametry funkce pro výběr bodů
- _ransac_: parametry Ransac algoritmu použitého pro výběr odpovídajících dvojic bodů
- _match_: parametry match algoritmu

Výchozí konfigurace:
```
    CFG = {
     'downsize': 500,
     'extract_features': {'method': 'HARRIS',
                          'min_distance': 1,
                          'patch_size': 59,
                          'threshold_rel': 1e-07},
     'irr_weight': 0.5,
     'match': {'max_distance': 200},
     'model_robust_param_limits': [[[-10, -1, -100], [-1, -2, -100], [-0.1, -0.02, 0]],
                                   [[10, 1, 100], [1, 2, 100], [0.1, 0.02, 2]]],
     'preprocess_images': {'blur_sigma': 2,
                           'edge': False,
                           'edge_high_threshold': 0.1,
                           'edge_low_threshold': 0.05,
                           'edge_sigma': 2,
                           'equalize': False,
                           'normalize': False},
     'ransac': {'max_trials': 10000, 'min_samples': 5, 'residual_threshold': 10}
    }
```

### Výstup:
- Snímek ve falešných barvách
- Snímek s překrytými snímky v IR a VIS světle (50 % IR + 50 % VIS)
- Transformované snímky v IR a VIS světle (se snímky lze dále pracovat, např. pro vytvoření prolnutí s jinými parametry)

---

## Ukázka:

### Zdrojové obrázky:
<p align="center">
  <img src="samples/vis_samples/a001_vis_image.jpg" width="150" title="">
  <img src="samples/ir_samples/a001_ir_image.jpg" width="150" alt="">
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





---

_Software je výsledkem projektu NAKI II:  Neinvazivní výzkum portrétních miniatur pro účely jejich datace, autentikace, prezentace a ochrany, číslo projektu: DG18P02OVV034_



