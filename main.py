from fastapi import FastAPI
from typing import Optional

app = FastAPI()


@app.get("/items/{item_id}/{name}")
async def read_item(item_id:int, name:Optional[str] = None):
    if name == None:
        return {"item_id": item_id}
    else:
        return {"item_id": item_id, 'name': name}
