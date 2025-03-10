from util import generateToken
from openai import OpenAI
import os
generateToken()

# Make the API call
header_name = os.getenv('GATEWAY_HEADER_NAME')
header_value = os.getenv('GATEWAY_HEADER_VALUE')
headers = {
    header_name: header_value
 }
client = OpenAI(default_headers=headers)
#client.api_key = os.getenv('OPENAI_API_KEY')
#client.base_url = os.getenv('OPENAI_BASE_URL')

# Define the messages
messages = [
    {"role": "system", "content": "You are a Al and ML profession. You must regret to answer any questions which are not in scope of AI and ML" }
]


while True:
    prompt = input("Enter the prompt: ")
    if prompt=='exit':
        break

    messages.append({"role": "developer", "content": prompt})

    print("Please wait....")
    completion = client.chat.completions.create(  
        model="gpt-4o-2024-05-13",
        messages=messages,
    )
    # Print the response
    print(completion.choices[0].message.content)
    print("="*50)


print("Thanks for using...")