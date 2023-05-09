#!/usr/bin/env python3
"""Task 11"""


def schools_by_topic(mongo_collection, topic):
    """returns school based on topic lookup"""
    return mongo_collection.find({"topics": topic})
