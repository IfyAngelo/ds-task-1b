# Let's start by loading the necessary libraries and modifying the code accordingly.

import os
import openai
import docx
from sentence_transformers import SentenceTransformer
from pinecone import Pinecone

# Setting up the API key for OpenAI
os.environ['OPENAI_API_KEY'] = "openai-api"
openai.api_key = os.environ['OPENAI_API_KEY']

# Initialize Pinecone and OpenAI
pc = Pinecone(api_key="pinecone-index-api", environment="")
index = pc.Index("pinecone-name", host="pinecone-index-host")

# Loading the Sentence Transformer model
model = SentenceTransformer('all-MiniLM-L6-v2')

# Function to split long documents into smaller chunks
def split_text_into_chunks(plain_text, max_chars=2000):
    text_chunks = []
    current_chunk = ""
    for line in plain_text.split("\n"):
        if len(current_chunk) + len(line) + 1 <= max_chars:
            current_chunk += line + " "
        else:
            text_chunks.append(current_chunk.strip())
            current_chunk = line + " "
    if current_chunk:
        text_chunks.append(current_chunk.strip())
    return text_chunks

# Function to add data to the Pinecone vector database
def add_data(corpus_data):
    id = index.describe_index_stats()['total_vector_count']
    for i in range(len(corpus_data)):
        chunk = corpus_data[i]
        chunk_info = (str(id + i),
                      model.encode(chunk).tolist(),
                      {'context': chunk})
        index.upsert(vectors=[chunk_info])

# This function is responsible for matching the input string with already existing data on the vector database.
def find_match(query, k):
    query_em = model.encode(query).tolist()
    index = pc.Index("pinecone-name", host="pincone-index-host") # Fill out with index name
    #result = index.query(query_em, top_k=k, include_metadata=True)
    result = index.query(vector=query_em, top_k=k, include_metadata=True)
    return [result['matches'][i]['metadata']['context'] for i in range(min(k, len(result['matches'])))]

# Create a prompt using the process discussed above
def create_prompt(contexts, query):
    prompt = f"Context: {', '.join(contexts)}\n\nQuestion: {query}\n\nAnswer:"
    return prompt

# Function to generate an answer using GPT-3
def generate_answer(prompt):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",  # Specify the correct GPT-3 model here
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.7,
        max_tokens=150
    )
    return response.choices[0].message["content"].strip()

# Function to handle user queries
def user_query(query):
    # Find the best matching context based on the query
    best_context = find_match(query, k=1)[0]

    # Create a prompt using the best context and the query
    prompt = create_prompt(best_context, query)

    # Generate an answer using GPT-3
    answer = generate_answer(prompt)

    return answer

# Load the docx file and split it into chunks
def load_and_process_docx(file_path):
    doc = docx.Document(file_path)
    text = ""
    for paragraph in doc.paragraphs:
        text += paragraph.text + "\n"
    chunks = split_text_into_chunks(text)
    add_data(chunks)
    return chunks


# Test the process

docx_file_path = "path-to-knowledge-docx"
chunks = load_and_process_docx(docx_file_path)
print("Document loaded and processed successfully.")

# Now, we can use user_query function to get answers for queries.
# Let's define a sample query and get an answer.
query = "What are the implications of climate change?"
answer = user_query(query)
print("Answer:", answer)

