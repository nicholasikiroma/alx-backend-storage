#!/usr/bin/env python3
""" lists all documents in a collection"""


def list_all(mongo_collection):
    """Return documents in collection"""
    return mongo_collection.find()
