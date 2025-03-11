import os
from dotenv import load_dotenv
from opensearchpy import OpenSearch
from opensearchpy.helpers import bulk
from util import generateToken
from openai import OpenAI
import os
generateToken()
header_name = os.getenv('GATEWAY_HEADER_NAME')
header_value = os.getenv('GATEWAY_HEADER_VALUE')
headers = {
    header_name: header_value
}
openai_client = OpenAI(default_headers=headers)

host = os.environ.get('OPENSEARCH_HOST')
port = os.environ.get('OPENSEARCH_PORT')
username = os.environ.get('OPENSEARCH_USERNAME')
password = os.environ.get('OPENSEARCH_PASSWORD')

# OpenSearch configuration dictionary
OPENSEARCH_CONFIG = {
    "hosts": [{"host": host, "port": port}],
    "http_auth": (username, password),
    "http_compress": True,
    "use_ssl": True,
    "verify_certs": False,
    "ssl_assert_hostname": False,
    "ssl_show_warn": False
}

# Mock documents array with fun facts
knowledge_base = [
    {"content": "A group of flamingos is called a 'flamboyance'.", "name": "Fun Fact 1"},
    {"content": "Octopuses have five hearts.", "name": "Fun Fact 2"},
    {"content": "Butterflies taste with their feet.", "name": "Fun Fact 3"},
    {"content": "A snail can sleep for Five years.", "name": "Fun Fact 4"},
    {"content": "Elephants are the only animals that can't jump.", "name": "Fun Fact 5"},
    {"content": "A rhinoceros' horn is made of hair.", "name": "Fun Fact 6"},
    {"content": "Slugs have four noses.", "name": "Fun Fact 7"},
    {"content": "A cow gives nearly 200,000 glasses of milk in a lifetime.", "name": "Fun Fact 8"},
    {"content": "Bats are the only mammals that can fly.", "name": "Fun Fact 9"},
    {"content": "Koalas sleep up to 21 hours a day.", "name": "Fun Fact 10"}
]

# Function to return embedding array for the parameter arrayOfStrings using OpenAI Embedding API
def generate_embeddings(arrayOfStrings):
    # Generate embeddings for the given list of texts using OpenAI API.
    header_name = os.getenv('GATEWAY_HEADER_NAME')
    header_value = os.getenv('GATEWAY_HEADER_VALUE')
    headers = {
        header_name: header_value
    }
    openai_client = OpenAI(default_headers=headers)
    response = openai_client.embeddings.create(input=arrayOfStrings, dimensions=1024, model="text-embedding-3-small")    
    arrayOfEmbeddings = [item.embedding for item in response.data]
    return arrayOfEmbeddings

INDEX_NAME = "funfacts"

# Function to create OpenSearch index with knn_vector mapping
def create_opensearch_index(opensearch_client):
    index_body = {
        "settings": {
                "index": {
                    "knn": True  # Enable k-NN
                },
        },
        "mappings": {
            "properties": {
                "id": {"type": "long"},  # ID field (similar to serial)
                "name": {"type": "text"}, # Text field for the document name
                "content": {"type": "text"}, # Text field for the document content
                "fact_embedding": {
                    "type": "knn_vector", # k-NN vector field for embeddings
                    "dimension": 1024, # Dimension of the embedding vector
                    "method": { # Method for indexing the embeddings
                        "name": "hnsw", # Hierarchical Navigable Small World Graph used for indexing
                        "space_type": "cosinesimil", # Cosine similarity used for distance calculation (L2 for Euclidean Distance)
    # If you're working with text embeddings (like OpenSearch k-NN search), cosine similarity is usually the best choice.
                        "engine": "nmslib" # NMSLIB library used for indexing 
                        }
                }
            }
        }
    }
    # Create the index (Table) if it does not exist
    if not opensearch_client.indices.exists(INDEX_NAME):
        opensearch_client.indices.create(index=INDEX_NAME, body=index_body)
        print(f"Index '{INDEX_NAME}' created.")

# Function to insert documents into OpenSearch
def insert_documents(opensearch_client, knowledge_base, fact_embeddings):
    actions = []
    for i, doc in enumerate(knowledge_base):
        action = {
            "_index": INDEX_NAME,
            "_id": i,
            "_source": {
                "name": doc["name"],
                "content": doc["content"],
                "fact_embedding": fact_embeddings[i]
            }
        }
        actions.append(action)
    success, _ = bulk(opensearch_client, actions)
    print(f"Successfully inserted {success} documents into OpenSearch.")

# Main function to generate embeddings and insert documents
def main():
    # Extract contents from the documents
    arrayOfStrings = []
    for doc in knowledge_base:
        arrayOfStrings.append(doc["content"])

    # Generate embeddings for the content
    arrayOfEmbeddings = generate_embeddings(arrayOfStrings)

    # Connect to OpenSearch
    opensearch_client = OpenSearch(**OPENSEARCH_CONFIG)

    # Create the OpenSearch index
    create_opensearch_index(opensearch_client)

    # Insert documents with embeddings
    insert_documents(opensearch_client, knowledge_base, arrayOfEmbeddings)

# Entry point of the script
if __name__ == "__main__":
    main()