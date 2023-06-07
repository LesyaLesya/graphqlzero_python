"""Модуль со схемами post."""

from helpers.schemas.common_schemas import STRING_NULL_TYPE
from helpers.schemas.user_schemas import USER_SCHEMA


POST_SCHEMA = {
    'type': 'object',
    'properties': {
        'id': STRING_NULL_TYPE,
        'title': STRING_NULL_TYPE,
        'body': STRING_NULL_TYPE,
        'user': USER_SCHEMA,
        'comments':
            {'type': 'object',
             'properties': {
                 'data': {
                     'type': 'array',
                     'items': [{
                         'type': 'object',
                         'properties': {
                             'id': STRING_NULL_TYPE,
                             'name': STRING_NULL_TYPE,
                             'body': STRING_NULL_TYPE}}]}}}}}

POSTS_SCHEMA = {
    '$schema': 'http://json-schema.org/draft-04/schema#',
    'type': 'object',
    'properties': {
        'data': {
            'type': 'array',
            'items': [POST_SCHEMA]}}}


GET_POST_SCHEMA = {
    '$schema': 'http://json-schema.org/draft-04/schema#',
    'type': 'object',
    'properties': {
        'data':
            {'type': 'object',
             'properties': {
                'post': POST_SCHEMA},
             'required': ['post']}},
    'required': ['data']}

GET_POSTS_SCHEMA = {
    '$schema': 'http://json-schema.org/draft-04/schema#',
    'type': 'object',
    'properties': {
        'data': {
            'type': 'object',
            'properties': {
                'posts': POSTS_SCHEMA},
            'required': ['posts']}},
    'required': ['data']}


UPDATE_POST_SCHEMA = {
    '$schema': 'http://json-schema.org/draft-04/schema#',
    'type': 'object',
    'properties': {
        'data':
            {'type': 'object',
             'properties': {
                'updatePost': POST_SCHEMA},
             'required': ['updatePost']}},
    'required': ['data']}


CREATE_POST_SCHEMA = {
    '$schema': 'http://json-schema.org/draft-04/schema#',
    'type': 'object',
    'properties': {
        'data':
            {'type': 'object',
             'properties': {
                'createPost': POST_SCHEMA},
             'required': ['createPost']}},
    'required': ['data']}
