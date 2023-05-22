from fastapi import Cookie, FastAPI, Path
from typing import Annotated, Dict, List, Optional, Union
from pydantic import BaseModel

app = FastAPI()



@app.get("/")
async def index(name: Union[str, None] = None) -> Dict:
    if not name:
        name = "world"
    return {
        "Hello": name
    }

@app.get("/hello_from_{name}")
async def hello_from_name(name: str) -> Dict:
    return {"Hello from": name}

@app.get("/hello_with_cookie")
async def hello_with_cookie(ads_id: Annotated[Union[str,None], Cookie()] = None):
    return {"ads_id": ads_id}

class PropertyModel(BaseModel):
    address: str
    price: int


class UserModel(BaseModel):
    username: str
    age: int
    properties: Optional[List[PropertyModel]]


@app.post("/users/")
async def create_user(user: UserModel):
    return user


@app.get("/items/{id}")
async def get_item_by_id(id: Annotated[int, Path(title="Id expected")]):
    return {"item_id": id}

