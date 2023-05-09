#!/usr/bin/env python3
"""insers a new document in a collection"""


def insert_school(mongo_collection, **kwargs):
    """"returns new _id"""
    new_doc = mongo_collection.insert_one(kwargs).inserted_id
    return new_doc
