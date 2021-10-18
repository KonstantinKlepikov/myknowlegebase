---
description: Как поставит ьспецифическую версию пакета в pip
---
# Installing specific package versions with pip

Например, используя указатель версии ниже, чем

```bash
pip install 'stevedore>=1.3.0,<1.4.0'
```

или так:

```bash
pip install 'stevedore>=1.3.0,<1.4.0' --force-reinstall
```

См. [ссылку](https://stackoverflow.com/questions/5226311/installing-specific-package-versions-with-pip), где более подробно разбирается вся ситуация.
