from flask import Flask, render_template, request
import chromadb
from chromadb.utils import embedding_functions
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv(os.path.join(os.path.dirname(__file__), '..', '.env'))

app = Flask(__name__)

# Initialize ChromaDB Client
# Use the same database we imported the products into
client = chromadb.PersistentClient(path="./chroma_db")

# Setup Embedding Function
# Same as in the import script
openai_key = os.getenv("OPENAI_API_KEY")
if openai_key:
    emb_fn = embedding_functions.OpenAIEmbeddingFunction(
        api_key=openai_key,
        model_name="text-embedding-3-small"
    )
else:
    emb_fn = embedding_functions.DefaultEmbeddingFunction()

# Get the collection
collection = client.get_or_create_collection(
    name="product_collection",
    embedding_function=emb_fn
)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    data = request.get_json()
    if not data:
        return {"error": "Invalid JSON"}, 400
        
    user_message = data.get('message')
    session_id = data.get('session_id')
    
    if not user_message or not session_id:
        return {"error": "Missing message or session_id"}, 400
        
    # Import here to avoid circular dependencies if any, though top-level is fine too.
    from chatbot import generate_chat_response
    
    try:
        response_text = generate_chat_response(session_id, user_message, collection)
        return {"response": response_text}
    except Exception as e:
        print(f"Chat error: {e}")
        return {"error": "Internal server error"}, 500

@app.route('/search', methods=['POST'])
def search():
    query = request.form.get('query')
    if not query:
        return render_template('index.html', results=[])
    
    # Query ChromaDB for top 6 similar products
    # n_results=6 provides a nice grid layout
    results = collection.query(
        query_texts=[query],
        n_results=6
    )
    
    # Format the results for the template
    formatted_results = []
    for i in range(len(results['documents'][0])):
        formatted_results.append({
            'document': results['documents'][0][i],
            'metadata': results['metadatas'][0][i],
            'distance': results['distances'][0][i],
            'id': results['ids'][0][i]
        })
        
    return render_template('index.html', query=query, results=formatted_results)

if __name__ == '__main__':
    app.run(debug=True, port=5001)
