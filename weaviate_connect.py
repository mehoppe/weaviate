import logging
import os


def connect(weaviate_key, openai_api_key, log):
    import weaviate

    client = weaviate.Client(
        url="https://weaviate-64pq3jgx.weaviate.network",
        auth_client_secret=weaviate.AuthApiKey(api_key=weaviate_key),
        additional_headers={
            "X-OpenAI-Api-Key": openai_api_key
        }
    )

    test = client.schema.get()
    log.debug("Client schema: %s", test)

    return client


def main():
    log = logging.getLogger("app")
    logging.basicConfig()
    log.setLevel(logging.WARNING)

    weaviate_key = os.environ["weaviate_key"]
    openai_api_key = os.environ["openai_api_key"]
    log.debug("Environment variables loaded.")

    connect(weaviate_key, openai_api_key, log)
    log.debug("Connected to Weaviate.")

if __name__ == "__main__":
    main()
