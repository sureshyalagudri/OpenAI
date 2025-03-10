from openai import OpenAI
import os

from util import generateToken

generateToken()
header_name = os.getenv('GATEWAY_HEADER_NAME')
header_value = os.getenv('GATEWAY_HEADER_VALUE')
headers = {
    header_name: header_value
 }
client = OpenAI(default_headers=headers)

messages = [
    {
        "role": "system",
        "content": """
                You are a poet.                
                You can write poems with variable number of  lines in each stanza. 
                Please use the below json format for output
                {
                    "stanza":  [           
                            {               
                            "lines: [
                                    "Line 1"                        
                            ],
                            "lines_count": 3
                            }            
                    ]
                }
                """,
    },
    {
        "role": "user",
        "content": "Write a poem on Weather"
    },
]
completion = client.chat.completions.create(
    model="gpt-4o-2024-05-13",
    messages=messages,
    temperature=0.3,
    top_p=0.3,
    response_format={"type": "json_object"},
)

# Print the response
print(completion.choices[0].message.content)
