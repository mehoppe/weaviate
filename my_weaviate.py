import json
import logging
import os
import pytest
import requests
import weaviate_connect
import weaviate_search

def build_class(client, class_obj, log):
    try:
        client.schema.create_class(class_obj)
        log.info("Class obj created.")
    except:
        log.warning("Class obj already exists.")

def add_objs(client, log):
    resp = requests.get('https://raw.githubusercontent.com/weaviate-tutorials/quickstart/main/data/jeopardy_tiny.json')
    data = json.loads(resp.text)  # Load data

    client.batch.configure(batch_size=100)  # Configure batch
    with client.batch as batch:  # Initialize a batch process
        for i, d in enumerate(data):  # Batch import data
            log.debug(f"importing question: {i+1}")
            properties = {
                "answer": d["Answer"],
                "question": d["Question"],
                "category": d["Category"],
            }
            try:
                batch.add_data_object(
                    data_object=properties,
                    class_name="Question"
                )
            except:
                log.error("OpenAI API Failure.")
        log.debug("All objects added.")

def main():
    log = logging.getLogger("app")
    logging.basicConfig()
    log.setLevel(logging.WARNING)

    try:
        weaviate_key = os.environ["weaviate_key"]
        openai_api_key = os.environ["openai_api_key"]
        log.info("Environment variables loaded.")
    except:
        log.error("Environment variables NOT loaded.")

    class_obj = {
        "class": "Question",
        "vectorizer": "text2vec-openai",  # If set to "none" you must always provide vectors yourself. Could be any other "text2vec-*" also.
        "moduleConfig": {
            "text2vec-openai": {},
            "generative-openai": {}  # Ensure the `generative-openai` module is used for generative queries
        }
    }
    
    client = weaviate_connect.connect(weaviate_key, openai_api_key, log)
    log.info("Connected to Weaviate.")
    build_class(client, class_obj, log)
    log.info("Class Object created.")
    add_objs(client, log)
    log.info("Objects added to class/collection.")
    result = weaviate_search.do_search(client, log)
    print(json.dumps(result, indent=4))


if __name__ == "__main__":
    main()
