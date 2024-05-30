"""Модуль со схемами post."""

from services.user.schemas import UserSchema


from typing import Optional, List
from pydantic import BaseModel


class Comment(BaseModel):
    id: Optional[str] = None
    name: Optional[str] = None
    body: Optional[str] = None


class ListComments(BaseModel):
    data: List[Comment]


class PostSchema(BaseModel):
    id: Optional[str] = None
    title: Optional[str] = None
    body: Optional[str] = None
    user: Optional[UserSchema] = None
    comments: Optional[ListComments] = None


class PostsSchema(BaseModel):
    data: List[PostSchema]


class GetPost(BaseModel):
    post: PostSchema


class GetPostSchema(BaseModel):
    data: GetPost


class GetPosts(BaseModel):
    posts: PostsSchema


class GetPostsSchema(BaseModel):
    data: GetPosts


class UpdatePost(BaseModel):
    updatePost: PostSchema


class UpdatePostSchema(BaseModel):
    data: UpdatePost


class CreatePost(BaseModel):
    createPost: PostSchema


class CreatePostSchema(BaseModel):
    data: CreatePost
