import traceback
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager, closing
from typing import Annotated

from bson import ObjectId
from litestar import Litestar, Router, get, post
from litestar.contrib.pydantic import PydanticDTO
from litestar.controller import Controller
from litestar.datastructures import State
from litestar.dto import DTOData
from litestar.exceptions import NotFoundException
from motor import motor_asyncio
from motor.motor_asyncio import AsyncIOMotorClient
from pydantic import BaseModel, ConfigDict, Field
from pydantic.functional_validators import BeforeValidator

PyObjectId = Annotated[str, BeforeValidator(str)]


class ItemModel(BaseModel):
    id: PyObjectId | None = Field(alias="_id", default=None)
    name: str = Field(...)
    email: str = Field(...)
    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True,
        json_schema_extra={
            "example": {"name": "Jane Doe", "email": "jdoe@example.com"}
        },
    )


class ItemController(Controller):
    @post(dto=PydanticDTO[ItemModel])
    async def create_item(self, data: DTOData[ItemModel], state: State) -> ItemModel:
        items_collection = state.mongo.mcve_db.get_collection("items")
        new_item = await items_collection.insert_one(data.as_builtins())
        created_item = await items_collection.find_one({"_id": new_item.inserted_id})
        return ItemModel.model_validate(created_item)

    @get("{id: str}", return_dto=PydanticDTO[ItemModel])
    async def show_item(self, id: str, state: State) -> ItemModel:
        try:
            items_collection = state.mongo.mcve_db.get_collection("items")
            item = await items_collection.find_one({"_id": ObjectId(id)})
            if item is not None:
                return item

            raise NotFoundException(f"item {id} not found")
        except Exception:
            traceback.print_exc()
            raise


@asynccontextmanager
async def db_connection(app: Litestar) -> AsyncIterator[None]:
    conn_string = "mongodb://127.0.0.1:27017/?readPreference=primary&appname=MongoDB%20Compass&ssl=false"
    with closing(AsyncIOMotorClient(conn_string)) as db_client:
        app.state.items_collection = db_client.mcve_db.get_collection("items")
        yield


def create_app():
    return Litestar(
        route_handlers=[
            Router(
                path="/item",
                route_handlers=[
                    ItemController,
                ],
            ),
        ],
        state=State(
            {
                "mongo": motor_asyncio.AsyncIOMotorClient(
                    "mongodb://127.0.0.1:27017/?readPreference=primary&appname=MongoDB%20Compass&ssl=false"
                ),
            }
        ),
        # lifespan=[db_connection],
    )


app = create_app()
