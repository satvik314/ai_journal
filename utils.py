import os
import uuid
import typing
import time
import ast
import pandas as pd
import numpy as np
from numpy.linalg import norm
from supabase import create_client, Client
from langchain.chat_models import ChatOpenAI
from typing import Dict
import openai
from langchain.embeddings import OpenAIEmbeddings
from dotenv import load_dotenv
load_dotenv()

url: str = os.getenv("SUPABASE_URL")
key: str = os.getenv("SUPABASE_KEY")
supabase: Client = create_client(url, key)
openai.api_key = os.getenv("OPENAI_API_KEY")

llm = ChatOpenAI(temperature= 0.2)

def insert_into_db(journal_info : Dict):
    inserted_row, error = supabase.table("daily_journal").insert(journal_info).execute()
    if error:
        print(f"An error occurred: {error}")
    else:
        print("Row inserted successfully")

# def embed_text(text: str):
#     embeddings = OpenAIEmbeddings()
#     result = embeddings.embed_query(text)
#     return result

def embed_text(text, model="text-embedding-ada-002"):
   text = text.replace("\n", " ")
   return openai.Embedding.create(input = [text], model=model)['data'][0]['embedding']

def journal_summary(notes: str):
    prompt = f"""The following is my daily journal note <{notes}>. 
    Please summarise this in one sentence how the I am feeling."""

    note_summary = llm.predict(prompt)

    return note_summary

def cosine_similarity(A, B):
    return np.dot(A, B) / (norm(A) * norm(B))


def match_documents_pd(query, match_count=2, threshold=0.7):
    # embeddings = OpenAIEmbeddings()
    # query_embedding = embeddings.embed_query(query)
    query_embedding = embed_text(query)
    data = supabase.table("daily_journal").select("notes, notes_vec, description").execute()
    df = pd.DataFrame(data.data)
    df['notes_vec'] = df['notes_vec'].apply(lambda x: np.array(ast.literal_eval(x)))
    df['similarity'] = df['notes_vec'].apply(lambda x: cosine_similarity(query_embedding, x))
    df = df.sort_values(by=['similarity'], ascending=False)
    df = df[df['similarity'] >= threshold]
    df = df.head(match_count)
    df = df.drop(columns=['notes_vec'])
    # result_dict = {row['description']: row['similarity'] for row in df.to_dict('records')}
    result_list = df['description'].tolist()
    return result_list


def match_documents(query, match_count=2, threshold=0.7):
    query_vec = embed_text(query)

    response, count = supabase.rpc('match_journals', {
        'query_vec': query_vec,
        'match_count': match_count
             }).execute()
    
    _, data = response

    filtered_docs = [journal['description'] for journal in data if journal['similarity'] > threshold]

    return filtered_docs


def create_prompt(query):
    entries = match_documents(query)
    entries_text = " ".join(entries)

    if len(entries_text) > 0:
        prompt = """The enclosed statements were extracted from the personal journal. Keep these in mind and give suggestions."""
        prompt += "<" + entries_text + ">" + "\n" + "Query: " + query
    else:
        prompt = "Query: " + query

    return prompt

# print(match_documents("I am feeling burnt out"))

print(create_prompt("I am feeling berseck"))



