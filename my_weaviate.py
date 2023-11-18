import json
import logging
import os
import requests
import weaviate_connect
import weaviate_search


def build_class(client, class_obj, log):
    try:
        client.schema.create_class(class_obj)
        log.info("Class obj created.")
    except:
        print("Class obj:\n, %s", class_obj)
        log.warning("Class obj already exists.")


def add_objs(client, data, log):
    client.batch.configure(batch_size=100)  # Configure batch
    with client.batch as batch:  # Initialize a batch process
        for i, d in enumerate(data):  # Batch import data
            log.debug(f"importing question: {i+1}")
            properties = {
                "answer": d["Answer"],
                "question": d["Question"],
                "category": d["Category"],
            }
            batch.add_data_object(
                data_object=properties,
                class_name="Question"
                )
        log.debug("All objects added.")

              
def main():
    log = logging.getLogger("app")
    logging.basicConfig()
    log.setLevel(logging.WARNING)

    weaviate_key = os.environ["weaviate_key"]
    openai_api_key = os.environ["openai_api_key"]
    log.info("Environment variables loaded.")

    # Class object/collection to create
    class_obj = {
        "class": "Question",
        "vectorizer": "text2vec-openai",
        "moduleConfig": {
            "text2vec-openai": {},
            "generative-openai": {}
        }
    }
    
    client = weaviate_connect.connect(weaviate_key, openai_api_key, log)
    log.info("Connected to Weaviate.")
    # Build the class obj/collection if it does not exist
    build_class(client, class_obj, log)
    log.info("Class Object created.")
    
    # Add objects to the collection
    resp = requests.get('https://raw.githubusercontent.com/weaviate-tutorials/quickstart/main/data/jeopardy_tiny.json')
    data = json.loads(resp.text)  # Load data
    add_objs(client, data, log)
    log.info("Objects added to class/collection.")
    # Perform a query against the created collection
    result = weaviate_search.do_search(client, log)
    print(json.dumps(result, indent=4))


if __name__ == "__main__":
    main()
