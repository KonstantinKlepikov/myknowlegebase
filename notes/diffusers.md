---
description: Библиотека машинного обучения diffusers
tags: machine-learning
title: Diffusers library
---
Диффузионные модели обучаются пошагово удалять случайный гауссовский шум, чтобы сгенерировать интересующий образец, например изображение или аудио. Diffusers — это библиотека, нацеленная на то, чтобы сделать такие модели широкодоступными для всех.

## Краткое введение

Есть три основных компонента библиотеки, о которых нужно знать:

- DiffusionPipeline — это сквозной класс высокого уровня, предназначенный для быстрой генерации выборок из предварительно обученных моделей.
- [Популярные предварительно обученные архитектуры моделей и модули](https://huggingface.co/docs/diffusers/main/en/api/models), которые можно использовать в качестве строительных блоков для создания диффузионных систем.
- [Множество различных планировщиков](https://huggingface.co/docs/diffusers/api/schedulers/overview) — алгоритмов, которые управляют тем, как добавляется шум для обучения, и как генерируются изображения с шумоподавлением во время вывода.

### Основные задачи

| Task | Description | Pipeline |
|-|-|-|
| Unconditional Image Generation | generate an image from Gaussian noise | [unconditional_image_generation](https://huggingface.co/docs/diffusers/using-diffusers/unconditional_image_generation) |
| Text-Guided Image Generation | generate an image given a text prompt | [conditional_image_generation](https://huggingface.co/docs/diffusers/using-diffusers/conditional_image_generation) |
| Text-Guided Image-to-Image Translation | adapt an image guided by a text prompt | [img2img](https://huggingface.co/docs/diffusers/using-diffusers/img2img) |
| Text-Guided Image-Inpainting | fill the masked part of an image given the image, the mask and a text prompt | [inpaint](https://huggingface.co/docs/diffusers/using-diffusers/inpaint) |
| Text-Guided Depth-to-Image Translation | adapt parts of an image guided by a text prompt while preserving structure via depth estimation | [depth2img](https://huggingface.co/docs/diffusers/using-diffusers/depth2img) |

Еще [txt-to-img-to-video](https://huggingface.co/docs/diffusers/using-diffusers/text-img2vid)

Подробнее как организовать простейший пайплайн [смотри тут](https://huggingface.co/docs/diffusers/quicktour). Как работает дифузионная модель с понижением размерности смотри в [этом колабе](https://colab.research.google.com/github/huggingface/notebooks/blob/main/diffusers/diffusers_intro.ipynb).

### [AutoPipeline](https://huggingface.co/docs/diffusers/tutorials/autopipeline)

Класс AutoPipeline разработан для упрощения разнообразия конвейеров в Diffusers. Это общий конвейер task-first, который позволяет сосредоточиться на задаче (AutoPipelineForText2Image, AutoPipelineForImage2Image и AutoPipelineForInpainting) без необходимости знать конкретный класс конвейера. AutoPipeline автоматически определяет правильный класс конвейера для использования.

Под капотом AutoPipeline :

- Обнаруживает класс для выбранной модели
- В зависимости от задачи, загружает StableDiffusionPipeline, StableDiffusionImg2ImgPipeline или StableDiffusionInpaintPipelin . Любой параметр ( strength, num_inference_steps, и т. д.), который вы передадите этим конкретным конвейерам, также может быть передан AutoPipeline.

## [Обучение](https://huggingface.co/docs/diffusers/tutorials/basic_training)

## [LoRA для инференса](https://huggingface.co/docs/diffusers/tutorials/using_peft_for_inference) (пример с пикселартом)

Существует множество типов адаптеров (самыми популярными являются [LoRA](https://huggingface.co/docs/peft/conceptual_guides/adapter#low-rank-adaptation-lora)), обученных в разных стилях для достижения разных эффектов. Можно комбинировать несколько адаптеров для создания новых и уникальных изображений.

## Load

- [load pipeline](https://huggingface.co/docs/diffusers/using-diffusers/loading)
- [load community pipelines](https://huggingface.co/docs/diffusers/using-diffusers/custom_pipeline_overview)
- [load shedulers and models](https://huggingface.co/docs/diffusers/using-diffusers/schedulers)
- [load adapters](https://huggingface.co/docs/diffusers/using-diffusers/loading_adapters)

### [Файлы моделей и макеты](https://huggingface.co/docs/diffusers/using-diffusers/other-formats)

#### Файлы

Веса моделей [[pytorch]] обычно сохраняются с помощью утилиты `pickle` Python в виде файлов ckpt или bin. Однако `pickle` не является безопасным, и файлы `pickle` могут содержать вредоносный код, который может быть выполнен. Эта уязвимость вызывает серьезную озабоченность, учитывая популярность совместного использования моделей. Для решения этой проблемы безопасности была разработана библиотека `Safetensors` как безопасная альтернатива `pickle`, которая сохраняет модели в виде файлов safetensors.

#### [Safetensors](https://blog.eleuther.ai/safetensors-security-audit/)

Safetensors — это безопасный и быстрый формат файла для безопасного хранения и загрузки тензоров. Safetensors ограничивает размер заголовка, чтобы ограничить определенные типы атак, поддерживает ленивую загрузку (полезно для распределенных установок) и в целом имеет более высокую скорость загрузки.

Safetensors хранит веса в файле safetensors. Diffusers загружает файлы safetensors по умолчанию, если они доступны и установлена ​​библиотека Safetensors. Существует два способа организации файлов safetensors:

- Макет Diffusers-multifolder: может быть несколько отдельных файлов safetensors, по одному для каждого компонента конвейера (текстовый кодировщик, UNet, VAE), организованных в подпапки (в качестве примера см. репозиторий stable-diffusion-v1-5/stable-diffusion-v1-5)
- Однофайловая компоновка: все веса моделей можно сохранить в одном файле (в качестве примера см. репозиторий WarriorMama777/OrangeMixs)

Метод `from_pretrained()` используется для загрузки модели с файлами safetensors, хранящимися в нескольких папках.

#### Файлы LoRA

LoRA — это легкий адаптер, который быстро и легко обучается, что делает его особенно популярным для генерации изображений определенным образом или в определенном стиле. Эти адаптеры обычно хранятся в файле safetensors и широко распространены на платформах обмена моделями, таких как civitai.

LoRA загружаются в базовую модель с помощью метода `load_lora_weights()`.

#### ckpt

`pickle` файлы могут быть небезопасными, поскольку их можно использовать для выполнения вредоносного кода. Рекомендуется использовать файлы safetensors, где это возможно, или преобразовать веса в файлы safetensors.

## CogVideoX

## [Инференс](https://huggingface.co/docs/diffusers/using-diffusers/overview_techniques) (подробнее)

### Оптимизация

- [Speed up inference](https://huggingface.co/docs/diffusers/optimization/fp16)
- [Reduce memory usage](https://huggingface.co/docs/diffusers/optimization/memory)
- [PyTorch 2.0](https://huggingface.co/docs/diffusers/optimization/torch2.0)
- [xFormers](https://huggingface.co/docs/diffusers/optimization/xformers)
- [Token merging](https://huggingface.co/docs/diffusers/optimization/tome)
- [DeepCache](https://huggingface.co/docs/diffusers/optimization/deepcache)
- [TGATE](https://huggingface.co/docs/diffusers/optimization/tgate)
- [xDiT](https://huggingface.co/docs/diffusers/optimization/xdit)

Смотри еще:

- [[machine-learning]]
- [[pytorch]]
- [документация](https://huggingface.co/docs/diffusers/index)
- [theory-1 colab](https://colab.research.google.com/github/huggingface/notebooks/blob/main/examples/annotated_diffusion.ipynb#scrollTo=290edb0b)
- [theory02 colab](https://colab.research.google.com/github/huggingface/notebooks/blob/main/diffusers/diffusers_intro.ipynb#scrollTo=PzW5ublpBuUt)


[//begin]: # "Autogenerated link references for markdown compatibility"
[pytorch]: pytorch "Machine learning framework pytorch"
[machine-learning]: ../lists/machine-learning "Алгоритмы машинного обучения"
[//end]: # "Autogenerated link references"