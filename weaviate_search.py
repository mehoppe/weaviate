import json
import logging
import os
import weaviate_connect

def do_search(client, log):
    try:
        response = (
            client.query
            .get("Question", ["question", "answer", "category"])
            .with_near_text({"concepts": ["biology"]})
            .with_limit(2)
            .do()
        )
    except:
        log.error("Query searched failed.")

    log.debug(json.dumps(response, indent=4))
    return response

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
    
    client = weaviate_connect.connect(weaviate_key, openai_api_key, log)
    response = do_search(client, log)
    print(json.dumps(response, indent=4))

if __name__ == "__main__":
    main()