# Remove background

Este proyecto usa la librería `rembg` de python para hacer la tarea principal de remover el background de la foto que tu desees.

# Requirements

``` python
python: >3.7, <3.13
```

Librerías usadas:
 - os
 - numpy
 - cv2
 - skimage
 - tkinter
 - rembg

# Ejemplo de aplicación

### Original
<img src="/examples/foto_to_test.jpg" height="350" >
<br>
<br>

### Procesada
<img src="/examples/foto_to_test_whitebg.png" height="350" >

# Background color
Cambia el color de fondo en la [línea 105](https://github.com/Sergio55Veliz/Remove_Background_Photos/blob/main/by_rembg.py#L105)
``` python
    BGR_Color = (255, 255, 255) # Background Color 
```
Está en código RGB.
