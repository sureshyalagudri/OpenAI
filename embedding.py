import openai
import numpy as np
from util import generateToken
from openai import OpenAI
import os
generateToken()
header_name = os.getenv('GATEWAY_HEADER_NAME')
header_value = os.getenv('GATEWAY_HEADER_VALUE')
headers = {
    header_name: header_value
}
client = OpenAI(default_headers=headers)

# Sentences to be embedded
sentences = [
    "This is a Sample Code of OpenAI",
    "OpenAI Sample Code:",
    "Today is a holiday"
]
# Function to get embeddings from OpenAI
def get_embeddings(texts):
    response = client.embeddings.create(
        input=texts,     
        dimensions=256,
        model="text-embedding-3-small"
    )
    #print(response.data)    
    embeddings = []
    for data in response.data:
        embeddings.append(data.embedding)
        print(len(data.embedding))
    return embeddings

# Calculate Cosine Similariy
def cosine_similarity(a, b):
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

# Calculate Euclidean distance
def euclidean_distance(a,b):
    return np.linalg.norm(np.array(a) - np.array(b))

# Get embeddings
embeddings = get_embeddings(sentences)

#print("embeddings", embeddings)

# Print cosine similarities between all texts in sentences array
print("Cosine Similarities:")
for i in range(len(sentences)):
    for j in range(i + 1, len(sentences)):
        similarity = cosine_similarity(embeddings[i], embeddings[j])
        print(f"Similarity between '{sentences[i]}' and '{sentences[j]}': {similarity}")

print("cosine_similarity", cosine_similarity(embeddings[0], embeddings[1]))
print("euclidean_distance", euclidean_distance(embeddings[0], embeddings[1]))
