---
description: JSON Web Tokens
tags: jwt http python
title: JWT
---

Токен JWT состоит из трех частей: заголовка (header), полезной нагрузки (payload) и подписи. Первые два элемента — это JSON-объекты Третий элемент вычисляется на основании первых и зависит от выбранного алгоритма (в случае использования неподписанного JWT можно пропустить). Токены могут быть перекодированы в компактное представление (JWS/JWE Compact Serialization): к заголовку и полезной нагрузке применяется алгоритм кодирования Base64-URL, после чего добавляется подпись и все три элемента разделяются точками («.»).

## Заголовок

В заголовке описывается сам токен.

Обязательный ключ:

- `alg`: алгоритм, используемый для подписи/шифрования (в случае неподписанного JWT используется значение «none»).

Необязательные ключи:

- `typ`: тип токена (type). Используется в случае, когда токены смешиваются с другими объектами, имеющими JOSE заголовки. Должно иметь значение «JWT».
- `cty`: тип содержимого (content type). Если в токене помимо зарегистрированных служебных ключей есть пользовательские, то данный ключ не должен присутствовать. В противном случае должно иметь значение «JWT»

## Полезная нагрузка

Тут пользовательская информация, а также могут быть использованы некоторые служебные ключи. Все это необязательно:

- `iss`: чувствительная к регистру строка или URI, которая является уникальным идентификатором стороны, генерирующей токен (issuer).
- `sub`: чувствительная к регистру строка или URI, которая является уникальным идентификатором стороны, о которой содержится информация в данном токене (subject). Значения с этим ключом должны быть уникальны в контексте стороны, генерирующей JWT.
- `aud`: массив чувствительных к регистру строк или URI, являющийся списком получателей данного токена. Когда принимающая сторона получает JWT с данным ключом, она должна проверить наличие себя в получателях — иначе проигнорировать токен (audience).
- `exp`: время в формате Unix Time, определяющее момент, когда токен станет невалидным (expiration).
- `nbf`: в противоположность ключу exp, это время в формате Unix Time, определяющее момент, когда токен станет валидным (not before).
- `jti`: строка, определяющая уникальный идентификатор данного токена (JWT ID).
- `iat`: время в формате Unix Time, определяющее момент, когда токен был создан. iat и nbf могут не совпадать, например, если токен был создан раньше, чем время, когда он должен стать валидным (issued at).

Подробнее в [статье wiki](https://ru.wikipedia.org/wiki/JSON_Web_Token)

Пример с [pyjwt](https://pyjwt.readthedocs.io/en/stable/index.html)

```python
>>> import jwt
>>> encoded_jwt = jwt.encode({"some": "payload"}, "secret", algorithm="HS256")
>>> print(encoded_jwt)
eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzb21lIjoicGF5bG9hZCJ9.4twFt5NiznN84AWoo1d7KO1T_yoc0Z6XOpOVswacPZg
>>> jwt.decode(encoded_jwt, "secret", algorithms=["HS256"])
{'some': 'payload'}
```

Еще ресурсы:

- [wiki](https://ru.wikipedia.org/wiki/JSON_Web_Token)
- [пример с jwt](https://fastapi.tiangolo.com/tutorial/security/oauth2-jwt/#__tabbed_2_1) для [[fastapi]]
- [все jwt либы](https://jwt.io/libraries)
- [PyJWT](https://pyjwt.readthedocs.io/en/stable/index.html)
- [python-jose](https://github.com/mpdavis/python-jose/)
- [authlib](https://github.com/lepture/authlib)
- [JWCrypto](https://github.com/latchset/jwcrypto/)
- [fastapi-jwt-auth](https://github.com/IndominusByte/fastapi-jwt-auth/) брошено

[//begin]: # "Autogenerated link references for markdown compatibility"
[fastapi]: fastapi "Fastapi"
[//end]: # "Autogenerated link references"