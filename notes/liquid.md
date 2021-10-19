---
tags: templating
description: Шаблонизатор для web-приложений Liquid,
---
# Liquid

Шаблонизатор для web-приложений, используется в т.ч. на jekyll. [Ссылка на доку](https://shopify.github.io/liquid/)

## Как исключить обертку кода, например такую как `{` из шаблона

Используй \{`%` `raw` `%`\} и \{`%` `endraw` `%`\}

```md
{% raw %}

...lots of liquid code goes here and it doesn't get interpreted...

{% endraw %}
```
