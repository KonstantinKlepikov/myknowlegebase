---
description: Pythen библиотека алгоритмов обработки изображений
title: Scikit-image
tags: ml python
---
Scikit-image работает с [[numpy]] array

```python
>>> from skimage import data
>>> camera = data.camera()
>>> type(camera)
<type 'numpy.ndarray'>
>>> # An image with 512 rows and 512 columns
>>> camera.shape
(512, 512)
```

Модуль data содержить [несколько тестовых наборов данных](https://scikit-image.org/docs/stable/api/skimage.data.html#module-skimage.data)

Импорт своих изображений

```python
>>> import os
>>> filename = os.path.join(skimage.data_dir, 'moon.png')
>>> from skimage import io
>>> moon = io.imread(filename)
```

Отдельный пакет [natsort](https://github.com/SethMMorton/natsort) позволяет предварительно отсортировать список натуральным образом (не лексикографически) перед импортом

```python
>>> import os
>>> from natsort import natsorted, ns
>>> from skimage import io
>>> list_files = os.listdir('.')
>>> list_files
['01.png', '010.png', '0101.png', '0190.png', '02.png']
>>> list_files = natsorted(list_files)
>>> list_files
['01.png', '02.png', '010.png', '0101.png', '0190.png']
>>> image_list = []
>>> for filename in list_files:
...   image_list.append(io.imread(filename))
```

## [[numpy]] for images

```python
>>> from skimage import data
>>> camera = data.camera()
>>> type(camera)
<type 'numpy.ndarray'>

>>> camera.shape
(512, 512)
>>> camera.size
262144

>>> camera.min(), camera.max()
(0, 255)
>>> camera.mean()
118.31400299072266
```

Каналы для цветных изображений

```python
>>> cat = data.chelsea()
>>> type(cat)
<type 'numpy.ndarray'>
>>> cat.shape
(300, 451, 3)

>>> cat[10, 20]
array([151, 129, 115], dtype=uint8)
>>> # Set the pixel at (50th row, 60th column) to "black"
>>> cat[50, 60] = 0
>>> # set the pixel at (50th row, 61st column) to "green"
>>> cat[50, 61] = [0, 255, 0]  # [red, green, blue]
```

[Больше деталей](https://scikit-image.org/docs/stable/user_guide/numpy_images.html)

## [Image data types](https://scikit-image.org/docs/stable/user_guide/data_types.html)

Изображение - это всего лишь массив numpy с одним из следующих типов:

| Data | typeRange |
|-|-|
| uint8 | 0 to 255 |
| uint16 | 0 to 65535 |
| uint32 | 0 to 232 - 1 |
| float | -1 to 1 or 0 to 1 |
| int8 | -128 to 127 |
| int16 | -32768 to 32767 |
| int32 | -231 to 231 - 1 |

Функции могут поддерживать только подмножество определенных типов данных. В таком случае ввод будет преобразован в требуемый тип (если это возможно), и в лог будет напечатано предупреждающее сообщение, если потребуется копия в памяти. Доступны следующие служебные функции в основном пакете:

| Function name | Description |
|-|-|
| img_as_float | Convert to floating point (integer types become 64-bit floats) |
| img_as_ubyte | Convert to 8-bit uint. |
| img_as_uint | Convert to 16-bit uint. |
| img_as_int | Convert to 16-bit int. |

```python
>>> from skimage.util import img_as_ubyte
>>> image = np.array([0, 0.5, 1], dtype=float)
>>> img_as_ubyte(image)
array([  0, 128, 255], dtype=uint8)
```

Конвертация может приводить к потере точности! Кроме того, некоторые функции имеют собственные ограничению по ренжу.

Кроме того, можно использовать данные из [[open-cv]] с минимальными затратами на конвертацию. [Подробнее](https://scikit-image.org/docs/stable/user_guide/data_types.html#working-with-opencv)

## [I/O Plugin Infrastructure](https://scikit-image.org/docs/stable/user_guide/plugins.html)

## [Handling Video Files](https://scikit-image.org/docs/stable/user_guide/video.html)

В исследовательских целях удобнее преобразовать файлы видео в последовательности изображений или многомерный TIF. Для одноразового решения самый простой и надежный способ — преобразовать видео в набор последовательно пронумерованных файлов изображений, часто называемый последовательностью изображений. Затем это [можно читать так](https://scikit-image.org/docs/stable/api/skimage.io.html#skimage.io.imread_collection). Пример преобразования (из каждого кадра видео делается изображение, которое нумеруется пятью цифрами с добавлением нуля слева):

```bash
ffmpeg -i "video.mov" -f image2 "video-frame%05d.png"
```

Создание последовательности изображений имеет недостатки: они могут быть большими и громоздкими, а их создание может занять некоторое время. Как правило, предпочтительнее работать непосредственно с исходным видеофайлом. Для этого подойдет пакет [PyAV](https://pyav.org/docs/develop/)

```python
import av
v = av.open('path/to/video.mov')

for packet in container.demux():
    for frame in packet.decode():
        if frame.type == 'video':
            img = frame.to_image()  # PIL/Pillow image
            arr = np.asarray(img)  # numpy array
            # Do something!
```

С помощью пакета [pilms](https://github.com/soft-matter/pims), написанного поверх PyAV, можно получяить доп.функциональность и работать с разными форматами, используя общий АПИ.

```python
import pims
v = pims.Video('path/to/video.mov')
v[-1]  # a 2D numpy array representing the last frame
```

[Moviepy](https://zulko.github.io/moviepy/) позволяет изменять небольшие видео. [Imageio](https://imageio.readthedocs.io/en/stable/) поддерживает большее число форматов.

Наконец, можно использовать [[open-cv]]

## [Image adjustment: transforming image content](https://scikit-image.org/docs/stable/user_guide/transforming_image_data.html)

- [манипуляции с цветом](https://scikit-image.org/docs/stable/user_guide/transforming_image_data.html#color-manipulation)
- [контраст и выдержка](https://scikit-image.org/docs/stable/user_guide/transforming_image_data.html#contrast-and-exposure)

## [Geometrical transformations of images](https://scikit-image.org/docs/stable/user_guide/geometrical_transform.html)

- [Cropping, resizing and rescaling images](https://scikit-image.org/docs/stable/user_guide/geometrical_transform.html#cropping-resizing-and-rescaling-images)
- [Projective transforms (homographies)](https://scikit-image.org/docs/stable/user_guide/geometrical_transform.html#projective-transforms-homographies)

## Полезные ресурсы

- [Image Segmentation](https://scikit-image.org/docs/stable/user_guide/tutorial_segmentation.html)
- [How to parallelize loops](https://scikit-image.org/docs/stable/user_guide/tutorial_parallelization.html)
- [Examples galery](https://scikit-image.org/docs/stable/auto_examples/index.html#examples-gallery)
- [full api](https://scikit-image.org/docs/stable/api/api.html)
- [api glossary](https://scikit-image.org/docs/stable/genindex.html)

Смотри еще:

- [scikit-image.org](https://scikit-image.org/)
- [[computer-visions]]
- [[PIL]]
- [[open-cv]]
- [[scipy]]
- [[numpy]]

[//begin]: # "Autogenerated link references for markdown compatibility"
[numpy]: numpy "Numpy"
[numpy]: numpy "Numpy"
[open-cv]: open-cv "Open-cv"
[open-cv]: open-cv "Open-cv"
[computer-visions]: ../lists/computer-visions "Computer visions"
[PIL]: PIL "Pillow - обработка изображений"
[open-cv]: open-cv "Open-cv"
[scipy]: scipy "Scipy"
[numpy]: numpy "Numpy"
[//end]: # "Autogenerated link references"
[//begin]: # "Autogenerated link references for markdown compatibility"
[numpy]: numpy "Numpy"
[numpy]: numpy "Numpy"
[open-cv]: open-cv "Open-cv"
[open-cv]: open-cv "Open-cv"
[computer-visions]: ../lists/computer-visions "Computer visions"
[PIL]: PIL "Pillow - обработка изображений"
[open-cv]: open-cv "Open-cv"
[scipy]: scipy "Scipy"
[numpy]: numpy "Numpy"
[//end]: # "Autogenerated link references"