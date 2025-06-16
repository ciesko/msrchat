import os
from dotenv import load_dotenv
from azure.cosmos import CosmosClient
import pandas as pd

def get_container_client():
    """Get the Cosmos DB container client."""

    # Read the Cosmos DB settings from environment variables
    endpoint = os.environ.get("COSMOSDB_ENDPOINT")
    key = os.environ.get("COSMOSDB_KEY")
    database_name = os.environ.get("COSMOSDB_DATABASE_NAME")
    container_name = os.environ.get("COSMOSDB_CONTAINER_NAME")

    # Initialize the Cosmos DB client
    client = CosmosClient(endpoint, key)
    database = client.get_database_client(database_name)
    container = database.get_container_client(container_name)

    return container

def get_conversations(start_date = None, end_date = None):
    """Get the chat history from Cosmos DB."""

    container = get_container_client()

    query_template = """
    SELECT c.id, c.timestamp, c.response_timestamp, c.user_input as user_query, c.conversation_id, c.tool as context, c.answer as chat_response
    FROM c 
    {where_clause}
    ORDER BY c.timestamp DESC
    """
    
    if start_date:
        start_date = start_date.strftime("%Y-%m-%d %H:%M:%S")
    if end_date:
        end_date = end_date.strftime("%Y-%m-%d %H:%M:%S")

    where_clause = ""
    if start_date and end_date:
        where_clause = f"WHERE c.timestamp BETWEEN '{start_date}' AND '{end_date}'"
    elif start_date:
        where_clause = f"WHERE c.timestamp >= '{start_date}'"
    elif end_date:
        where_clause = f"WHERE c.timestamp <= '{end_date}'"

    query = query_template.format(where_clause=where_clause)

    items = container.query_items(query, enable_cross_partition_query=True)
    return items

def extend_dataframe(df):
    # "Promote" the content form the user_query and chat_response columns to the top level of the dataframe
    df['user_input'] = df['user_query'].apply(lambda x: x['content'] if pd.notnull(x) and 'content' in x else None)
    df['answer'] = df['chat_response'].apply(
        lambda x: x['choices'][0]['messages'][0]['content'] 
        if pd.notnull(x) 
        and 'choices' in x 
        and len(x['choices']) > 0 
        and 'messages' in x['choices'][0] 
        and len(x['choices'][0]['messages']) > 0 
        and 'content' in x['choices'][0]['messages'][0] 
        else None)

    # Calculate the response time
    df['response_timestamp'] = pd.to_datetime(df['response_timestamp'], errors='coerce')
    df['timestamp'] = pd.to_datetime(df['timestamp'], errors='coerce')
    df['duration'] = (df['response_timestamp'] - df['timestamp']).dt.total_seconds()

    # Calculate number of turns for each 'conversation_id'
    df['turn_count'] = df['conversation_id'].apply(lambda x: len(df[df['conversation_id'] == x]))
