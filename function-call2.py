import requests
import json
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

# Replace with your API keys
news_api_key = "c86245eca72141828e351e1ea1e92fae"

# Define the `get_news` function to retrieve news articles based on a given topic
def get_news(topic):
    print(f"In get news about {topic}")
    url = (
        f"https://newsapi.org/v2/everything?q={topic}&apiKey={news_api_key}&pageSize=5"
    )
    try:
        response = requests.get(url)
        if response.status_code == 200:
            news = json.dumps(response.json(), indent=4)
            news_json = json.loads(news)

            # Access all the fields == loop through
            status = news_json["status"]
            total_results = news_json["totalResults"]
            articles = news_json["articles"]
            final_news = []

            # Loop through articles
            for article in articles:
                source_name = article["source"]["name"]
                author = article["author"]
                title = article["title"]
                description = article["description"]
                url = article["url"]
                content = article["content"]
                title_description = f"""
                   Title: {title},
                   Author: {author},
                   Source: {source_name},
                   Description: {description},
                   URL: {url},
                   Content: {content}
                """
                final_news.append(title_description)
            return final_news
        else:
            return []

    except requests.exceptions.RequestException as e:
        return f"Error occurred during API Request: {e}"

# Define the function schema for OpenAI API
get_news_function_schema = {
    "name": "get_news",
    "description": "Retrieve the latest news articles on a given topic.",
    "parameters": {
        "type": "object",
        "properties": {
            "topic": {
                "type": "string",
                "description": "The topic to search news articles for.",
            }
        },
        "required": ["topic"],
    },
}

# Initial user message
messages = [{"role": "user", "content": "Based on latest news of AI and Stocks, generate a brief summary and suggest potential areas for further exploration or discussion"}] 
# First API call: Ask the model to use the function
response = client.chat.completions.create(
    model="gpt-4o-2024-08-06",
    messages=messages,
    tools = [
        {
            "type":  "function",
            "function": get_news_function_schema
        }
    ],
    tool_choice="auto",  # Let the model decide if the function should be called
)

# Process the model's response
response_message = response.choices[0].message
messages.append(response_message)

print("Model's response:")
print(response_message)

# If the model suggests calling the function
if response_message.tool_calls:
    for tool_call  in response_message.tool_calls:
        function_name = tool_call.function.name
        function_args =json.loads(tool_call.function.arguments)
        if function_name == "get_news":
            # Call the function with arguments
            topic = function_args.get("topic")
            news_result = get_news(topic)

            # Format the results into a single string
            formatted_news = "\n".join(news_result)
            messages.append({
                    "tool_call_id": tool_call.id,
                    "role": "tool",
                    "name": "get_news",
                    "content": formatted_news,
                })
else:
    print("No tool calls were made by the model.")

# Second API call: Get the final response from the model
response = client.chat.completions.create(
    model="gpt-4o-2024-08-06",
    messages =  messages,
)

# Output the response
print("Response:", response.choices[0].message.content)

