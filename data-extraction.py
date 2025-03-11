from util import generateToken
from openai import OpenAI
import os
import json

# Generate token
generateToken()

# Get OpenAI Client from Util
header_name = os.getenv('GATEWAY_HEADER_NAME')
header_value = os.getenv('GATEWAY_HEADER_VALUE')
headers = {
    header_name: header_value
}
client = OpenAI(default_headers=headers)

# Define the JSON Schema for an array of product reviews within an object
review_schema = {
    "type": "object",
    "properties": {
        "reviews": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "product_summary": {
                        "type": "string",
                        "description": "A brief summary of the product being reviewed."
                    },
                    "rating": {
                        "type": "number",
                        "description": "The rating given to the product, usually on a scale from 1 to 5."
                    },
                    "rating_text": {
                        "type": "string",
                        "description": "The rating text.",
                        "enum": ["bad", "excellent", "worst", "ok", "good"]
                    },
                    "review_text": {
                        "type": "string",
                        "description": "The detailed review text provided by the reviewer."
                    },
                    "reviewer": {
                        "type": "string",
                        "description": "The name or identifier of the reviewer."
                    },
                    "isReview": {
                        "type": "boolean",
                        "description": "Indicates whether input text is a review or not"
                    }
                },
                "required": ["product_summary", "rating", "rating_text", "review_text", "reviewer", "isReview"],
                "additionalProperties": False
            }
        }
    },
    "required": ["reviews"],
    "additionalProperties": False
}

print("Fetching data, please wait...")

# Use OpenAI's chat completion API with the JSON Schema
completion = client.chat.completions.create(
    model="gpt-4o-2024-08-06",
    temperature=0.5,
    messages=[
        {"role": "system", "content": "Extract the review details. For missing fields use NA"},
        {
            "role": "user",
            "content": """Suresh has reviewed laptop and mouse as 5 and 2.
            Bhavneet has reviewed chair as 1.
            Kunal has reviewed bus and car as 3 and 5."""
        }
    ],
    response_format={
        "type": "json_schema",
        "json_schema": {
            "name": "product_review",
            "strict": True,
            "schema": review_schema
        }
    }
)

# Extract the structured review information
rating = completion.choices[0].message.content
# Display the parsed review information
rating_json = json.loads(rating)
print(rating_json)