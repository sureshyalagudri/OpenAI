import os
import numpy as np
from opensearchpy import OpenSearch
from initialize_db import generate_embeddings # Python file of Step-1
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

# OpenSearch configuration
OPENSEARCH_CONFIG = {
    "hosts": [{"host": host, "port": port}],
    "http_auth": (username, password),
    "http_compress": True,
    "use_ssl": True,
    "verify_certs": False,
    "ssl_assert_hostname": False,
    "ssl_show_warn": False
}

INDEX_NAME = "gamefacts"

# Function to retrieve documents from OpenSearch based on cosine similarity
def retrieve_matching_documents(opensearch_client, user_query, limit=3):
    # Generate the embedding for the query
    user_query_embedding = generate_embeddings(user_query)[0]
    # Perform the OpenSearch search to get all documents   
    search_body = {        
        "_source": ["content"],  # Only retrieve necessary fields
        "query": {
            "knn": {
                "fact_embedding":{
                    "vector": user_query_embedding,
                    "k": limit,
                }
            }
        }
    }    
    response = opensearch_client.search(index=INDEX_NAME, body=search_body)    
    # Extract documents and their embeddings
    documents_string = ''
    # # match_all query returns all documents, so we need to filter based on cosine similarity
    for hit in response["hits"]["hits"]:
        doc = hit["_source"]
        documents_string += doc['content'] + " "
    return documents_string

# Function to interact with OpenAI and generate a response based on the retrieved documents
def generate_chat_response(user_query, retrieved_maching_string):
    completion = openai_client.chat.completions.create(
        model="gpt-4o-2024-08-06",
        messages=[
            #{"role": "system", "content": "You are a helpful assistant specialized about games. Provide your response base on information only in the context."},
            {"role": "system", "content": "You are a helpful assistant specialized about Animals. Provide your response including the information not necessary in the context."},
            {"role": "user", "content": f"Question: {user_query}  \n Context: {retrieved_maching_string} "},            
        ]
    )    
    return completion.choices[0].message.content

# Main function for testing
def main():
    # User query for information
    user_query = "I want to learn about indian cricket team"

    # Connect to OpenSearch
    opensearch_client = OpenSearch(**OPENSEARCH_CONFIG)

    # Retrieve documents based on the user query
    retrieved_maching_string = retrieve_matching_documents(opensearch_client, user_query, limit=5)
 
    print('---------------------------------- Retrieved Documents ----------------------------------')
    for ele in retrieved_maching_string.split('.'):
        print(ele, sep='\n')
    print('---------------------------------------------------------------------------------------------------')
    
    if retrieved_maching_string:
        # Generate a response based on the retrieved documents
        response = generate_chat_response(user_query, retrieved_maching_string)
        print("Response from OpenAI Assistant: ", response)
    else:
        print("No relevant documents found.")

if __name__ == "__main__":
    main()
