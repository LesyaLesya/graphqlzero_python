"""Модуль со схемами user."""

from helpers.schemas.common_schemas import STRING_NULL_TYPE


USER_SCHEMA = {
    'type': 'object',
    'properties': {
        'id': STRING_NULL_TYPE,
        'name': STRING_NULL_TYPE,
        'phone': STRING_NULL_TYPE,
        'email': STRING_NULL_TYPE,
        'username': STRING_NULL_TYPE,
        'website': STRING_NULL_TYPE},
        'address': {
            'type': 'object',
            'properties': {
                'geo': {
                    'type': 'object',
                    'properties': {
                        'lat': {'type': 'number'},
                        'lng': {'type': 'number'}}}}}}


USERS_SCHEMA = {
    '$schema': 'http://json-schema.org/draft-04/schema#',
    'type': 'object',
    'properties': {
        'data': {
            'type': 'array',
            'items': [USER_SCHEMA]}}}


GET_USER_SCHEMA = {
    '$schema': 'http://json-schema.org/draft-04/schema#',
    'type': 'object',
    'properties': {
        'data':
            {'type': 'object',
             'properties': {
                'user': USER_SCHEMA},
             'required': ['user']}},
    'required': ['data']}


GET_USERS_SCHEMA = {
    '$schema': 'http://json-schema.org/draft-04/schema#',
    'type': 'object',
    'properties': {
        'data': {
            'type': 'object',
            'properties': {
                'users': USERS_SCHEMA},
            'required': ['users']}},
    'required': ['data']}
