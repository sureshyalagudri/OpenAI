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

{"content": "Honey never spoils. Archaeologists have found pots of honey in ancient Egyptian tombs that are over 3,000 years old and still edible.", "name": "Fun Fact 1"},

{"content": "Bananas are berries, but strawberries aren't.", "name": "Fun Fact 2"},

{"content": "A day on Venus is longer than a year on Venus.", "name": "Fun Fact 3"},

{"content": "Wombat poop is cube-shaped.", "name": "Fun Fact 4"},

{"content": "There are more stars in the universe than grains of sand on all the world's beaches.", "name": "Fun Fact 5"},

{"content": "A single strand of spaghetti is called a 'spaghetto'.", "name": "Fun Fact 6"},

{"content": "The shortest war in history lasted 38 minutes.", "name": "Fun Fact 7"},

{"content": "A bolt of lightning contains enough energy to toast 100,000 slices of bread.", "name": "Fun Fact 8"},

{"content": "The Eiffel Tower can be 15 cm taller during the summer due to thermal expansion.", "name": "Fun Fact 9"},

{"content": "A group of crows is called a 'murder'.", "name": "Fun Fact 10"},

{"content": "Octopuses have three hearts.", "name": "Fun Fact 11"},

{"content": "Butterflies taste with their feet.", "name": "Fun Fact 12"},

{"content": "A snail can sleep for three years.", "name": "Fun Fact 13"},

{"content": "Elephants are the only animals that can't jump.", "name": "Fun Fact 14"},

{"content": "A rhinoceros' horn is made of hair.", "name": "Fun Fact 15"},

{"content": "Slugs have four noses.", "name": "Fun Fact 16"},

{"content": "A cow gives nearly 200,000 glasses of milk in a lifetime.", "name": "Fun Fact 17"},

{"content": "Bats are the only mammals that can fly.", "name": "Fun Fact 18"},

{"content": "Koalas sleep up to 21 hours a day.", "name": "Fun Fact 19"},

{"content": "A group of flamingos is called a 'flamboyance'.", "name": "Fun Fact 20"},

{"content": "Sharks are the only fish that can blink with both eyes.", "name": "Fun Fact 21"},

{"content": "A group of jellyfish is called a 'smack'.", "name": "Fun Fact 22"},

{"content": "The longest recorded flight of a chicken is 13 seconds.", "name": "Fun Fact 23"},

{"content": "A crocodile cannot stick its tongue out.", "name": "Fun Fact 24"},

{"content": "Starfish do not have a brain.", "name": "Fun Fact 25"},

{"content": "Polar bear skin is black, and their fur is actually clear.", "name": "Fun Fact 26"},

{"content": "A shrimp's heart is in its head.", "name": "Fun Fact 27"},

{"content": "A group of frogs is called an 'army'.", "name": "Fun Fact 28"},

{"content": "The fingerprints of a koala are so indistinguishable from humans that they have on occasion been confused at a crime scene.", "name": "Fun Fact 29"},

{"content": "A group of owls is called a 'parliament'.", "name": "Fun Fact 30"},

{"content": "A group of ravens is called an 'unkindness'.", "name": "Fun Fact 31"},

{"content": "A group of giraffes is called a 'tower'.", "name": "Fun Fact 32"},

{"content": "A group of kangaroos is called a 'mob'.", "name": "Fun Fact 33"},

{"content": "A group of lions is called a 'pride'.", "name": "Fun Fact 34"},

{"content": "A group of whales is called a 'pod'.", "name": "Fun Fact 35"},

{"content": "A group of geese is called a 'gaggle'.", "name": "Fun Fact 36"},

{"content": "A group of crows is called a 'murder'.", "name": "Fun Fact 37"},

{"content": "A group of parrots is called a 'pandemonium'.", "name": "Fun Fact 38"},

{"content": "A group of rhinos is called a 'crash'.", "name": "Fun Fact 39"},

{"content": "A group of eagles is called a 'convocation'.", "name": "Fun Fact 40"},

{"content": "A group of flamingos is called a 'flamboyance'.", "name": "Fun Fact 41"},

{"content": "A group of peacocks is called an 'ostentation'.", "name": "Fun Fact 42"},

{"content": "A group of porcupines is called a 'prickle'.", "name": "Fun Fact 43"},

{"content": "A group of turkeys is called a 'rafter'.", "name": "Fun Fact 44"},

{"content": "A group of vultures is called a 'wake'.", "name": "Fun Fact 45"},

{"content": "A group of zebras is called a 'zeal'.", "name": "Fun Fact 46"},

{"content": "A group of lemurs is called a 'conspiracy'.", "name": "Fun Fact 47"},

{"content": "A group of ferrets is called a 'business'.", "name": "Fun Fact 48"},

{"content": "A group of larks is called an 'exaltation'.", "name": "Fun Fact 49"},

{"content": "A group of finches is called a 'charm'.", "name": "Fun Fact 50"},

{"content": "The first video game ever created was 'Tennis for Two', developed in 1958.", "name": "Game Fact 1"},

{"content": "The best-selling video game of all time is 'Minecraft', with over 200 million copies sold.", "name": "Game Fact 2"},

{"content": "The longest Monopoly game ever played lasted 70 days.", "name": "Game Fact 3"},

{"content": "The original name for Pac-Man was 'Puck Man', but it was changed to avoid vandalism.", "name": "Game Fact 4"},

{"content": "The world record for the highest score in Tetris is held by Joseph Saelee, with a score of 1,357,428.", "name": "Game Fact 5"},

{"content": "The first home video game console was the Magnavox Odyssey, released in 1972.", "name": "Game Fact 6"},

{"content": "The most expensive video game ever developed is 'Grand Theft Auto V', with a budget of $265 million.", "name": "Game Fact 7"},

{"content": "The longest chess game theoretically possible is 5,949 moves.", "name": "Game Fact 8"},

{"content": "The highest-grossing arcade game of all time is 'Pac-Man', generating over $2.5 billion in quarters.", "name": "Game Fact 9"},

{"content": "The first esports tournament was held in 1972 for the game 'Spacewar!'.", "name": "Game Fact 10"},

{"content": "The most popular board game in the world is 'Chess', with millions of players worldwide.", "name": "Game Fact 11"},

{"content": "The first handheld gaming device was the Microvision, released in 1979.", "name": "Game Fact 12"},

{"content": "The longest video game marathon lasted 35 hours and 35 minutes, playing 'Call of Duty: Modern Warfare 3'.", "name": "Game Fact 13"},

{"content": "The most-played online game is 'League of Legends', with millions of active players daily.", "name": "Game Fact 14"},

{"content": "The first 3D video game was 'Battlezone', released in 1980.", "name": "Game Fact 15"},

{"content": "The most expensive board game ever sold is a gold and diamond-encrusted Monopoly set, valued at $2 million.", "name": "Game Fact 16"},

{"content": "The first game to feature a 'boss fight' was 'Space Invaders', released in 1978.", "name": "Game Fact 17"},

{"content": "The most popular mobile game is 'Candy Crush Saga', with billions of downloads.", "name": "Game Fact 18"},

{"content": "The first game to feature multiplayer was 'Maze War', released in 1974.", "name": "Game Fact 19"}
]

knowledge_base.extend([

{"content": "The longest Dungeons & Dragons campaign lasted over 38 years.", "name": "Game Fact 20"},

{"content": "The first video game to be played in space was 'Starcraft', played by astronaut Daniel T. Barry in 1999.", "name": "Game Fact 21"},

{"content": "The most popular card game in the world is 'Poker'.", "name": "Game Fact 22"},

{"content": "The first video game character to have a balloon in the Macy's Thanksgiving Day Parade was Sonic the Hedgehog.", "name": "Game Fact 23"},

{"content": "The most expensive video game ever sold is a sealed copy of 'Super Mario Bros.', which sold for $2 million.", "name": "Game Fact 24"},

{"content": "The first video game to feature a save game function was 'The Legend of Zelda', released in 1986.", "name": "Game Fact 25"},

{"content": "The longest video game development period is held by 'Duke Nukem Forever', which took 15 years to develop.", "name": "Game Fact 26"},

{"content": "The first video game to be adapted into a movie was 'Super Mario Bros.', released in 1993.", "name": "Game Fact 27"},

{"content": "The most popular sports video game series is 'FIFA', with millions of copies sold annually.", "name": "Game Fact 28"},

{"content": "The first video game to feature a female protagonist was 'Metroid', released in 1986.", "name": "Game Fact 29"},

{"content": "The most popular puzzle video game is 'Tetris', with billions of players worldwide.", "name": "Game Fact 30"},

{"content": "The first video game to feature voice acting was 'Berserk', released in 1980.", "name": "Game Fact 31"},

{"content": "The most popular racing video game series is 'Mario Kart', with millions of copies sold.", "name": "Game Fact 32"},

{"content": "The first video game to feature online multiplayer was 'Spasim', released in 1974.", "name": "Game Fact 33"},

{"content": "The most popular fighting video game series is 'Street Fighter', with millions of players worldwide.", "name": "Game Fact 34"},

{"content": "The first video game to feature a 3D environment was 'Wolfenstein 3D', released in 1992.", "name": "Game Fact 35"},

{"content": "The most popular simulation video game series is 'The Sims', with millions of copies sold.", "name": "Game Fact 36"},

{"content": "The first video game to feature a sandbox environment was 'Minecraft', released in 2011.", "name": "Game Fact 37"},

{"content": "The most popular strategy video game series is 'Civilization', with millions of players worldwide.", "name": "Game Fact 38"},

{"content": "The first video game to feature a virtual reality environment was 'Dactyl Nightmare', released in 1991.", "name": "Game Fact 39"},

{"content": "The most popular horror video game series is 'Resident Evil', with millions of copies sold.", "name": "Game Fact 40"},

{"content": "The first video game to feature a procedurally generated environment was 'Rogue', released in 1980.", "name": "Game Fact 41"},

{"content": "The most popular rhythm video game series is 'Dance Dance Revolution', with millions of players worldwide.", "name": "Game Fact 42"},

{"content": "The first video game to feature a physics engine was 'Half-Life', released in 1998.", "name": "Game Fact 43"},

{"content": "The most popular adventure video game series is 'The Legend of Zelda', with millions of copies sold.", "name": "Game Fact 44"},

{"content": "The first video game to feature a dynamic weather system was 'The Elder Scrolls III: Morrowind', released in 2002.", "name": "Game Fact 45"},

{"content": "The most popular sandbox video game series is 'Grand Theft Auto', with millions of players worldwide.", "name": "Game Fact 46"},

{"content": "The first video game to feature a destructible environment was 'Red Faction', released in 2001.", "name": "Game Fact 47"},

{"content": "The most popular survival video game series is 'Minecraft', with millions of copies sold.", "name": "Game Fact 48"},

{"content": "The first video game to feature a crafting system was 'Ultima Online', released in 1997.", "name": "Game Fact 49"},

{"content": "The most popular role-playing video game series is 'Final Fantasy', with millions of players worldwide.", "name": "Game Fact 50"},

{"content": "The first video game to feature a morality system was 'Fable', released in 2004.", "name": "Game Fact 51"},

{"content": "The most popular open-world video game series is 'The Elder Scrolls', with millions of copies sold.", "name": "Game Fact 52"},

{"content": "The first video game to feature a branching storyline was 'Mass Effect', released in 2007.", "name": "Game Fact 53"},

{"content": "The most popular stealth video game series is 'Metal Gear Solid', with millions of players worldwide.", "name": "Game Fact 54"},

{"content": "The first video game to feature a cover system was 'Gears of War', released in 2006.", "name": "Game Fact 55"},

{"content": "The most popular shooter video game series is 'Call of Duty', with millions of copies sold.", "name": "Game Fact 56"},

{"content": "The first video game to feature a parkour system was 'Mirror's Edge', released in 2008.", "name": "Game Fact 57"},

{"content": "The most popular platformer video game series is 'Super Mario', with millions of players worldwide.", "name": "Game Fact 58"},

{"content": "The first video game to feature a time travel mechanic was 'Chrono Trigger', released in 1995.", "name": "Game Fact 59"},

{"content": "The most popular puzzle video game series is 'Portal', with millions of copies sold.", "name": "Game Fact 60"},

{"content": "The first video game to feature a roguelike mechanic was 'NetHack', released in 1987.", "name": "Game Fact 61"},

{"content": "The most popular racing video game series is 'Need for Speed', with millions of players worldwide.", "name": "Game Fact 62"},

{"content": "The first video game to feature a sandbox mechanic was 'SimCity', released in 1989.", "name": "Game Fact 63"},

{"content": "The most popular simulation video game series is 'Flight Simulator', with millions of copies sold.", "name": "Game Fact 64"},

{"content": "The first video game to feature a survival mechanic was 'Resident Evil', released in 1996.", "name": "Game Fact 65"},

{"content": "The most popular strategy video game series is 'StarCraft', with millions of players worldwide.", "name": "Game Fact 66"},

{"content": "The first video game to feature a crafting mechanic was 'Minecraft', released in 2011.", "name": "Game Fact 67"},

{"content": "The most popular role-playing video game series is 'The Witcher', with millions of copies sold.", "name": "Game Fact 68"},

{"content": "The first video game to feature a morality mechanic was 'Fallout', released in 1997.", "name": "Game Fact 69"},

{"content": "The most popular open-world video game series is 'Assassin's Creed', with millions of players worldwide.", "name": "Game Fact 70"},

{"content": "The first video game to feature a branching storyline mechanic was 'The Walking Dead', released in 2012.", "name": "Game Fact 71"},

{"content": "The most popular stealth video game series is 'Splinter Cell', with millions of copies sold.", "name": "Game Fact 72"},

{"content": "The first video game to feature a cover mechanic was 'Rainbow Six', released in 1998.", "name": "Game Fact 73"},

{"content": "The most popular shooter video game series is 'Halo', with millions of players worldwide.", "name": "Game Fact 74"},

{"content": "The first video game to feature a parkour mechanic was 'Prince of Persia', released in 1989.", "name": "Game Fact 75"},

{"content": "The most popular platformer video game series is 'Crash Bandicoot', with millions of copies sold.", "name": "Game Fact 76"},

{"content": "The first video game to feature a time travel mechanic was 'Day of the Tentacle', released in 1993.", "name": "Game Fact 77"},

{"content": "The most popular puzzle video game series is 'Professor Layton', with millions of players worldwide.", "name": "Game Fact 78"}
])

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

INDEX_NAME = "gamefacts"

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