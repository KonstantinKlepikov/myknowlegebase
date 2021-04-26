# heroku-variables-config

[Статья](https://devcenter.heroku.com/articles/config-vars)

![vars](../attachments/2021-04-27-00-46-24.png)

Доступ к БД устанавливать через энвирон. Требуется `psycopq2` для постгреса.

```python
DATABASE_URL = os.environ.get('DATABASE_URL')
```

Для переменных локально использовать [[dot-env]]

[[heroku]]
[[requirements]]
[[heroku-piplines]]
[[heroku-release-phase]]
