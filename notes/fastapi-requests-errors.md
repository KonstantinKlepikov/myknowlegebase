# fastapi-requests-errors

## Поднимать руками

[Handling Errors](https://fastapi.tiangolo.com/tutorial/handling-errors/)

```python
from fastapi import FastAPI, HTTPException

app = FastAPI()

items = {"foo": "The Foo Wrestlers"}


@app.get("/items/{item_id}")
async def read_item(item_id: str):
    if item_id not in items:
        raise HTTPException(status_code=404, detail="Item not found")
    return {"item": items[item_id]}
```

Недостаток - не документируется в [[swagger]]

## Определить респонс и прописать в модели

[Additional Responses in OpenAPI](https://fastapi.tiangolo.com/advanced/additional-responses/)

```python
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from pydantic import BaseModel


class Item(BaseModel):
    id: str
    value: str


class Message(BaseModel):
    message: str


app = FastAPI()


@app.get("/items/{item_id}", response_model=Item, responses={404: {"model": Message}})
async def read_item(item_id: str):
    if item_id == "foo":
        return {"id": "foo", "value": "there goes my hero"}
    else:
        return JSONResponse(status_code=404, content={"message": "Item not found"})

```

Респонс прописывается в [[swagger]], но есть проблема - если мы возвращаем респонс в от унаследованного ресурса, возвращается тело ошибки и его надо обрабатывать на уровне ниже. Ошибку эту так-же не будет видно в документации в наследующем ресурсе.

В статье так-же описано как можно переопределить статус ы [[fastapi]]

[Additional Status Codes](https://fastapi.tiangolo.com/advanced/additional-status-codes/)
[[http-requests-errors]]
[[requests]]