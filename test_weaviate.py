import json
import logging
import my_weaviate
import os
import pytest
import weaviate_connect
import weaviate_search


def test_add_objs():
    weaviate_key = os.environ["weaviate_key"]
    openai_api_key = os.environ["openai_api_key"]
    log = logging.getLogger("app")
    logging.basicConfig()
    log.setLevel(logging.CRITICAL)

    client = weaviate_connect.connect(weaviate_key, openai_api_key, log)

    data = json.loads('[{"Category":"SCIENCE","Question":"This organ removes excess glucose from the blood & stores it as glycogen","Answer":"Liver"}]')
    # Add objects to the collection
    try:
        my_weaviate.add_objs(client, data, log)
    except:
        pytest.fail("Add Object FAIL.") 


def test_weaviate_search():
    weaviate_key = os.environ["weaviate_key"]
    openai_api_key = os.environ["openai_api_key"]
    log = logging.getLogger("app")
    logging.basicConfig()
    log.setLevel(logging.CRITICAL)

    client = weaviate_connect.connect(weaviate_key, openai_api_key, log)
    result = weaviate_search.do_search(client, log)
    assert type(result) is dict