---
description: Список заметок о vscode
category: list
tags: vscode
title: Vscode
---
## Can't get VSCode/Python debugger to find my project modules

[python debugging](https://code.visualstudio.com/docs/python/debugging)

```json
{
    "version": "0.2.0",
    "configurations": [
        {
           "name": "Python: Current File",
           "type": "python",
           "request": "launch",
           "program": "${file}",
           "console": "integratedTerminal",
           "env": { "PYTHONPATH": "${workspaceRoot}"}
        }
    ]
}
```

[источник](https://stackoverflow.com/questions/53290328/cant-get-vscode-python-debugger-to-find-my-project-modules). [Еще](https://stackoverflow.com/questions/38623138/vscode-how-to-set-working-directory-for-debugging-a-python-program).

Что еще почитать?

- [[2021-06-04-daily-note]]
- [[как-работать-с-foam]]
- [[vscode-from-docker]]
- [Multi-root Workspaces](https://code.visualstudio.com/docs/editor/multi-root-workspaces)

[//begin]: # "Autogenerated link references for markdown compatibility"
[2021-06-04-daily-note]: ../posts/2021-06-04-daily-note "Как получить текст ошибки в python и немного про pylance в vscode"
[как-работать-с-foam]: ../notes/как-работать-с-foam "Как работать с foam"
[vscode-from-docker]: ../notes/vscode-from-docker "VScode from docker"
[//end]: # "Autogenerated link references"