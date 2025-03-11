from util import generateToken
from pydantic import BaseModel, Field
from openai import OpenAI
from typing import Literal
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


# Define Pydantic models for the schema
class Review(BaseModel):
    product_summary: list[str] = Field(..., description="A brief summary of the product being reviewed.")
    rating: float = Field(..., description="The rating given to the product, usually on a scale from 1 to 5.")
    rating_text: Literal["bad", "excellent", "average", "worst", "poor"] = Field(..., description="The rating in text format.")
    review_text: str = Field(..., description="The detailed review text provided by the reviewer.")
    reviewer: str = Field(..., description="The name or identifier of the reviewer.")
    isReview: bool = Field(..., description="If the text is a valid review, set the value to true otherwise set it to false.")

class Reviews(BaseModel):
    items: list[Review] = Field(..., description="A list of reviews for different products.")

print("Fetching data, please wait...")

# Use OpenAI's chat completion API with the JSON Schema
completion = client.beta.chat.completions.parse(
    model="gpt-4o-2024-08-06",
    temperature=0.5,
    messages=[
        {"role": "system", "content": "Extract the review details. For missing fields use NA"},
        {
            "role": "user",
            "content": """Suresh has reviewed laptop and mouse as 5 and 2.
            Bhavneet has reviewed chair as 1.
            Kunal has reviewed bus and car as 3 and 5.
            Sandeep has not rated anything."""
        }
    ],
    response_format=Reviews
)

# Extract the structured review information
rating = completion.choices[0].message.content
# Display the parsed review information
rating_json = json.loads(rating)

# Print in good format
reviews = completion.choices[0].message.parsed
for review in reviews.items:
    print(f"Reviewer: {review.reviewer}")
    print(f"Product Summary: {review.product_summary}")
    print(f"Rating: {review.rating} ({review.rating_text})")
    print(f"Review Text: {review.review_text}")
    print(f"Is Review: {review.isReview}")
    print()