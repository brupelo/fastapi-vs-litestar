from typing import Optional

import motor.motor_asyncio
from bson import ObjectId
from fastapi import APIRouter, Body, FastAPI, Request, status
from pydantic import BaseModel, ConfigDict, EmailStr, Field
from pydantic.functional_validators import BeforeValidator
from typing_extensions import Annotated

PyObjectId = Annotated[str, BeforeValidator(str)]


class ItemModel(BaseModel):
    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    name: str = Field(...)
    email: EmailStr = Field(...)
    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True,
        json_schema_extra={
            "example": {"name": "Jane Doe", "email": "jdoe@example.com"}
        },
    )


mcve_router = APIRouter()


@mcve_router.post(
    "",
    response_description="Add new item",
    response_model=ItemModel,
    status_code=status.HTTP_201_CREATED,
    response_model_by_alias=False,
)
async def create_item(request: Request, item: ItemModel = Body(...)):
    items_collection = request.app.items_collection
    new_item = await items_collection.insert_one(
        item.model_dump(by_alias=True, exclude=["id"])
    )
    created_item = await items_collection.find_one({"_id": new_item.inserted_id})
    return created_item


@mcve_router.get(
    "/{id}",
    response_description="Get a single item",
    response_model=ItemModel,
    response_model_by_alias=False,
)
async def show_item(request: Request, id: str):
    items_collection = request.app.items_collection
    item = await items_collection.find_one({"_id": ObjectId(id)})
    return item


def create_app():
    app = FastAPI()
    app.include_router(mcve_router, tags=["item"], prefix="/item")
    app.db_client = motor.motor_asyncio.AsyncIOMotorClient(
        "mongodb://127.0.0.1:27017/?readPreference=primary&appname=MongoDB%20Compass&ssl=false"
    )
    app.db = app.db_client.test_db_fastapi
    app.items_collection = app.db.get_collection("items")
    return app


app = create_app()
