"""Модуль со схемами user."""


from typing import Optional, List
from pydantic import BaseModel


class GeoSchema(BaseModel):
    lat: Optional[float]
    lng: Optional[float]


class AddressSchema(BaseModel):
    geo: GeoSchema


class UserSchema(BaseModel):
    id: Optional[str] = None
    name: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[str] = None
    username: Optional[str] = None
    website: Optional[str] = None
    address: Optional[AddressSchema] = None


class UsersSchema(BaseModel):
    data: List[UserSchema]


class GetUser(BaseModel):
    user: UserSchema


class GetUserSchema(BaseModel):
    data: GetUser


class GetUsers(BaseModel):
    users: UsersSchema


class GetUsersSchema(BaseModel):
    data: GetUsers
