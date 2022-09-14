---
description: Таскранер для poetry
tags: cl cli pip python
title: Poetrypoet
---
## Features

- Прямое объявление задач проекта в вашем `pyproject.toml` (что-то вроде сценариев npm)
- Задача запускается в виртуальной среде poetry (или в другой указанной вами среде)
- Имена задач в shell (а также глобальные параметры для zsh)
- Может использоваться отдельно или как плагин
- Задачи могут быть командами (с оболочкой или без нее) или ссылками на функции Python (например, tool.poetry.scripts)
- Короткие  команды с дополнительными аргументами, переданными в пакет задач [options] task [task_args], или вы можете явно определить аргументы
- Задачи могут указывать и ссылаться на переменные среды, как если бы они были запущены в командной облочке
- Задачи самодокументируются, с необязательными справочными сообщениями (просто запустите poe без аргументов)
- Задачи могут быть определены как последовательность других задач
- Работает с файлами .env
- Можно использовать автокомплишен по `tab` для bash, zsh, fish

## How to use

```yml
[tool.poe.tasks]
test   = "pytest --cov=poethepoet"                                # simple command based task
serve  = { script = "my_app.service:run(debug=True)" }            # python script based task
tunnel = { shell = "ssh -N -L 0.0.0.0:8080:$PROD:8080 $PROD &" }  # (posix) shell based task
```

`poe test` просто запустить или добавить дополнительные аргументы `poe test -v tests/favorite_test.py` -> `pytest --cov=poethepoet -v tests/favorite_test.py`

## Типы тасков

### Command task

Будет содержать одну команду, которая будет выполняться без оболочки. Это охватывает большинство основных вариантов использования

```yml
[tool.poe.tasks]
format = "black ."  # strings are interpreted as commands by default
clean = """
# Multiline commands including comments work too. Unescaped whitespace is ignored.
rm -rf .coverage
       .mypy_cache
       .pytest_cache
       dist
       ./**/__pycache__
"""
lint = { "cmd": "pylint poethepoet" }  # Inline tables with a cmd key work too
greet = "echo Hello $USER"  # Environment variables work, even though there's no shell!
```

### Script tasks

Содержат ссылку на python, вызываемый для импорта и выполнения

```yml
[tool.poe.tasks]
fetch-assets = { "script" = "my_package.assets:fetch" }
fetch-images = { "script" = "my_package.assets:fetch(only='images', log=environ['LOG_PATH'])" }
```

Подмножество синтаксиса, операторов и глобальных переменных Python может использоваться встроенно для определения аргументов функции с использованием обычного синтаксиса Python, включая environ (из пакета os) для доступа к переменным среды, которые доступны для задачи. Если дополнительные аргументы передаются задаче в командной строке (и аргументы CLI не объявлены), они будут доступны в вызываемой функции python через sys.argv.

### Shell task

Аналогичны простым командным задачам, за исключением того, что они выполняются внутри новой оболочки и могут состоять из нескольких отдельных команд, подстановки команд, конвейеров, фоновых процессов и т. д.

```yml
[tool.poe.tasks]
pfwd = { "shell" = "ssh -N -L 0.0.0.0:8080:$STAGING:8080 $STAGING & ssh -N -L 0.0.0.0:5432:$STAGINGDB:5432 $STAGINGDB &" }
pfwdstop = { "shell" = "kill $(pgrep -f "ssh -N -L .*:(8080|5432)")" }
```

По умолчанию poe пытается найти в системе оболочку posix (sh, bash или zsh именно в таком порядке) и использует ее. При работе в Windows это не всегда возможно. Если bash не найден по пути в Windows, то poe будет явно искать Gitbash в обычном месте.

Можно задать другие shell-интерпретаторы через `interpreter = ["posix", "pwsh"]`

Кроме того, можно можно задать python код как шелл-таск.

```python
[tool.poe.tasks.time]
shell = """
from datetime import datetime

print(datetime.now())
"""
interpreter = "python"
```

### Composite task

Определяются как последовательность других задач в виде массива. По умолчанию содержимое массива интерпретируется как ссылки на другие задачи (фактически тип задачи ref), хотя это поведение можно изменить, установив глобальную опцию default_array_item_task_type на имя другого типа задачи, например cmd, или установив default_item_type параметр локально в задаче последовательности.

```yml
[tool.poe.tasks]

test = "pytest --cov=src"
build = "poetry build"
_publish = "poetry publish"
release = ["test", "build", "_publish"]
```

Префикс `_` не включается в документацию и не исполняется непосредственно, а используется для ссылки на другие задачи.

Другой вариант записи:

```yml
release = [
  { cmd = "pytest --cov=src" },
  { script = "devtasks:build" },
  { ref = "_publish" },
]
```

Еще

```yml
[tool.poe.tasks]

  [[tool.poe.tasks.release]]
  cmd = "pytest --cov=src"

  [[tool.poe.tasks.release]]
  script = "devtasks:build"

  [[tool.poe.tasks.release]]
  ref = "_publish"
```

## Task level configuration

Можно задавать текст подсказок

```yml
[tool.poe.tasks]
style = {cmd = "black . --check --diff", help = "Check code style"}
```

Переменные окружения

```yml
[tool.poe.tasks]
serve.script = "myapp:run"
serve.env = { PORT = "9001" }
```

Можно использовать `.env` файлы

```yml
[tool.poe.tasks]
serve.script  = "myapp:run"
serve.envfile = ".env"
```

Также можно ссылаться на существующие переменные окружения при определении новой переменной окружения для задачи.

```yml
[tool.poe.tasks.serve]
serve.cmd = "flask run"
serve.env   = { FLASK_RUN_PORT = "${TF_VAR_service_port}" }
```

## Declaring CLI arguments

По умолчанию дополнительные аргументы, передаваемые в интерфейс командной строки poe после имени задачи, добавляются в конец задачи `cmd` или отображаются как `sys.argv` в задаче сценария (но вызовут ошибку для задач оболочки или последовательности задач). В качестве альтернативы можно определить именованные аргументы, которые должна принимать задача, которые будут задокументированы в справке для этой задачи и представлены в задаче таким образом, который наиболее целесообразен для этого типа задачи.

- positional arguments which are provided directly following the name of the task like `poe task-name <arg-value>`
- option arguments which are provided like `poe task-name --option-name <arg-value>`
- flags which are either provided or not, but don't accept a value like `poe task-name --flag`

Именованные аргументы настраиваются путем объявления параметра задачи args как массива или подтаблицы.

```yml
[tool.poe.tasks.serve]
cmd = "myapp:run"
args = ["host", "port"]
```

`poe serve --host 0.0.0.0 --port 8001`

Элементы в массиве также могут быть встроенными таблицами, чтобы обеспечить дефолтные значения

```yml
[tool.poe.tasks.serve]
cmd = "myapp:run"
args = [{ name = "host", default = "localhost" }, { name = "port", default = "9000" }]
```

Можно использовать `toml` синтаксис

```yml
[tool.poe.tasks.serve]
cmd = "myapp:run"
help = "Run the application server"

  [[tool.poe.tasks.serve.args]]
  name = "host"
  options = ["-h", "--host"]
  help = "The host on which to expose the service"
  default = "localhost"

  [[tool.poe.tasks.serve.args]]
  name = "port"
  options = ["-p", "--port"]
  help = "The port on which to expose the service"
  default = "8000"
```

или так

```yml
[tool.poe.tasks.serve]
cmd = "myapp:run"
help = "Run the application server"

  [tool.poe.tasks.serve.args.host]
  options = ["-h", "--host"]
  help = "The host on which to expose the service"
  default = "localhost"

  [tool.poe.tasks.serve.args.port]
  options = ["-p", "--port"]
  help = "The port on which to expose the service"
  default = "8000"
```

**Task args options:**

- default : Union[str, int, float, bool]
- help : str
- name : str
- options : List[str]
- positional : bool
- required : bool
- type : str

Для задач cmd и оболочки значения предоставляются задаче как переменные среды

```yml
[tool.poe.tasks.passby]
shell = """
echo "hello $planet";
echo "goodbye $planet";
"""
help = "Pass by a planet!"

  [[tool.poe.tasks.passby.args]]
  name = "planet"
  help = "Name of the planet to pass"
  default = "earth"
  options = ["-p", "--planet"]
```

`poe passby --planet mars`

Аргументы могут быть определены для задач сценария таким же образом, но то, как они отображаются для базовой функции Python, зависит от того, как определен сценарий.

```yml
[tool.poe.tasks]
build = { script = "project.util:build", args = ["dest", "version"] }
```

```yml
[tool.poe.tasks]
build = { script = "project.util:build(dest, build_version=version, verbose=True)", args = ["dest", "version"]
```

Аргументы могут быть переданы задачам, на которые ссылается задача последовательности

```yml
[tool.poe.tasks]
build = { script = "util:build_app", args = [{ name = "target", positional = true }] }

[tool.poe.tasks.check]
sequence = ["build ${target}", { script = "util:run_tests(environ['target'])" }]
args = ["target"]
```

## Project-wide configuration options

### Global environment variables

В `tool.poe.env`

```yml
[tool.poe.env]
VAR1 = "FOO"
VAR2 = "BAR BAR BLACK ${FARM_ANIMAL}"
```

Можно задать дефолт, если переменная не указана

```yml
# .env
STAGE=dev
PASSWORD='!@#$%^&*('

[tool.poe.env]
VAR1.default = "FOO"
```

Можно использовать `.env`

```yml
[tool.poe]
envfile = ".env"
```

### [Default command verbosity](https://github.com/nat-n/poethepoet#default-command-verbosity)

### [Run poe from anywhere](https://github.com/nat-n/poethepoet#run-poe-from-anywhere)

### [Change the default task type](https://github.com/nat-n/poethepoet#change-the-default-task-type)

### [Change the executor type](https://github.com/nat-n/poethepoet#change-the-executor-type)

- auto: to automatically use the most appropriate of the following executors in order
- poetry: to run tasks in the poetry managed environment
- virtualenv: to run tasks in the indicated virtualenv (or else "./.venv" if present)
- simple: to run tasks without doing any specific environment setup

```yml
[tool.poe.executor]
type = "virtualenv"
location = "myvenv"
```

### [Change the default shell interpreter](https://github.com/nat-n/poethepoet#change-the-default-shell-interpreter)

## [Load tasks from another file](https://github.com/nat-n/poethepoet#load-tasks-from-another-file)

В некоторых сценариях может потребоваться определить задачи вне pyproject.toml. Например, если вы хотите распределять задачи между проектами через модули git, динамически генерировать определения задач или просто иметь много задач и не хотите, чтобы pyproject.toml стал слишком большим. Этого можно достичь, создав файл toml или json в структуре каталогов вашего проекта, включая ту же структуру для задач, которая используется в pyproject.toml.

Еще:

- Usage as a poetry plugin
- Usage without poetry

Еще ссылки:

- [документация](https://github.com/nat-n/poethepoet)
- [[poetry]]
- [[argparsing]]
- [[click]]
- [[cli]]

[//begin]: # "Autogenerated link references for markdown compatibility"
[poetry]: poetry "Poetry"
[argparsing]: argparsing "Arguments parsing in python"
[click]: click "Click интерфейс командной строки"
[cli]: ../tag/cli "Tag: cli"
[//end]: # "Autogenerated link references"