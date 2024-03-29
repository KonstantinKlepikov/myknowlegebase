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

Статья про [[debugging]] в VSCode, Смотри еще [[pdb-python-debugger]]. Еще [[devtools]]

Что еще почитать?

- [[2021-06-04-daily-note]]
- [[как-работать-с-foam]]
- [[vscode-from-docker]]
- [Multi-root Workspaces](https://code.visualstudio.com/docs/editor/multi-root-workspaces)
- [Python settings reference](https://code.visualstudio.com/docs/python/settings-reference)
- [VSCode doesn't show poetry virtualenvs in select interpreter option](https://stackoverflow.com/questions/59882884/vscode-doesnt-show-poetry-virtualenvs-in-select-interpreter-option)
- [[trinity]] A VSCode extension for [[cypher]] and [[neo4j]]

[//begin]: # "Autogenerated link references for markdown compatibility"
[debugging]: ../notes/debugging "Debugging in VSCode"
[pdb-python-debugger]: ../notes/pdb-python-debugger "Pdb python debugger"
[devtools]: ../notes/devtools "Python devtools"
[2021-06-04-daily-note]: ../posts/2021-06-04-daily-note "Как получить текст ошибки в python и немного про pylance в vscode"
[как-работать-с-foam]: ../notes/%D0%BA%D0%B0%D0%BA-%D1%80%D0%B0%D0%B1%D0%BE%D1%82%D0%B0%D1%82%D1%8C-%D1%81-foam "Как работать с foam"
[vscode-from-docker]: ../notes/vscode-from-docker "VScode from docker"
[trinity]: ../notes/trinity "Trinity"
[cypher]: ../notes/cypher "Cypher query language"
[neo4j]: ../notes/neo4j "Neo4j graph data base"
[//end]: # "Autogenerated link references"
[//begin]: # "Autogenerated link references for markdown compatibility"
[2021-06-04-daily-note]: ../posts/2021-06-04-daily-note "Как получить текст ошибки в python и немного про pylance в vscode"
[как-работать-с-foam]: ../notes/как-работать-с-foam "Как работать с foam"
[vscode-from-docker]: ../notes/vscode-from-docker "VScode from docker"
[trinity]: ../notes/trinity "Trinity"
[cypher]: ../notes/cypher "Cypher query language"
[neo4j]: ../notes/neo4j "Neo4j graph data base"
[//end]: # "Autogenerated link references"