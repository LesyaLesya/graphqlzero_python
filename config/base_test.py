from services.post.schemas import (
    CreatePostSchema, GetPostSchema, GetPostsSchema, UpdatePostSchema, PostsSchema)
from services.user.schemas import GetUserSchema, GetUsersSchema
from utils.common_data import Errors, Messages
from utils.query_variables import QueryVariables
from services.post.data import PostData, CommentsData
from services.post.response_generator import PostResponseBodyGenerator
from services.user.data import UserData
from services.user.response_generator import UserResponseBodyGenerator


class BaseTest:

    def setup_method(self):
        # schemas
        self.create_post_schema = CreatePostSchema
        self.get_post_schema = GetPostSchema
        self.get_posts_schema = GetPostsSchema
        self.update_post_schema = UpdatePostSchema
        self.posts_schema = PostsSchema
        self.get_user_schema = GetUserSchema
        self.get_users_schema = GetUsersSchema

        # data
        self.post_data = PostData
        self.user_data = UserData
        self.comments_data = CommentsData
        self.errors = Errors
        self.messages = Messages
        self.user_generator = UserResponseBodyGenerator
        self.post_generator = PostResponseBodyGenerator

        # for queries
        self.query_vars = QueryVariables
