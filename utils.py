import os
import uuid
import typing
import time
from supabase import create_client, Client
from langchain.chat_models import ChatOpenAI
from typing import Dict
from langchain.embeddings import OpenAIEmbeddings
from dotenv import load_dotenv
load_dotenv()

url: str = os.getenv("SUPABASE_URL")
key: str = os.getenv("SUPABASE_KEY")
supabase: Client = create_client(url, key)

llm = ChatOpenAI(temperature= 0.2)

def insert_into_db(journal_info : Dict):
    inserted_row, error = supabase.table("daily_journal").insert(journal_info).execute()
    if error:
        print(f"An error occurred: {error}")
    else:
        print("Row inserted successfully")

def embed_text(text: str):
    embeddings = OpenAIEmbeddings()
    result = embeddings.embed_query(text)
    return result

def journal_summary(notes: str):
    prompt = f"""The following is my daily journal note <{notes}>. 
    Please summarise this in one sentence how the I am feeling."""

    note_summary = llm.predict(prompt)

    return note_summary
    








