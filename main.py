from urllib import response
from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel
app = FastAPI()


class Item(BaseModel):
    text:str
    is_done:bool=False

items=[]

@app.get("/")
def root():
    return {"Hello": "World"}


@app.post("/items")
def create_item(item: Item):
    for existing_item in items:
        if existing_item.text == item.text:
            existing_item.is_done = item.is_done
            return items
    else:
        items.append(item)
    return items


@app.get("/items", response_model=list[Item])
def list_items(limit: int=10):
    return items[:limit]


@app.get("/items/{item_id}",response_model=Item)
def get_item(item_id:int)->Item:
    if item_id < 0 or item_id >= len(items):
        raise HTTPException(status_code=404, detail="Item not found")
    else:
        item= items[item_id]
        return item