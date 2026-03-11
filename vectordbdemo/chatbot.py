from memory import get_history, save_message
from llm_client import ask_llm

# We will need the chromadb collection passed or accessible to this module.
# To keep things clean, we can initialize it here or import it from app.py.
# However, importing from app.py can cause circular dependencies.
# We'll expect app.py to pass the collection to the function.

def generate_chat_response(session_id: str, user_message: str, collection) -> str:
    """
    Generates a response using ChromaDB context and Gemini.
    """
    # 1. Product Count Feature
    lower_msg = user_message.lower()
    if any(phrase in lower_msg for phrase in ["how many products", "total products", "number of products", "count of products"]):
        try:
            count = collection.count()
            response_text = f"There are {count} products available in this store."
            save_message(session_id, "user", user_message)
            save_message(session_id, "assistant", response_text)
            return response_text
        except Exception as e:
            return f"Error retrieving product count: {e}"

    # 2. Retrieve conversation history
    history = get_history(session_id)
    history_text = "\n".join([f"{msg['role'].upper()}: {msg['content']}" for msg in history])
    if not history_text:
        history_text = "No previous context."

    # 3. Query ChromaDB for top 5 products matching the user message
    try:
        results = collection.query(
            query_texts=[user_message],
            n_results=5
        )
        
        retrieved_products = ""
        # Build context string
        if results['documents'] and results['documents'][0]:
            for i in range(len(results['documents'][0])):
                doc = results['documents'][0][i]
                meta = results['metadatas'][0][i] if results['metadatas'] else {}
                price = meta.get("price", "N/A")
                retrieved_products += f"- Product: {doc} | Price: €{price}\n"
        else:
            retrieved_products = "No relevant products found."
            
    except Exception as e:
        print(f"Error querying ChromaDB: {e}")
        retrieved_products = "Error retrieving product data."

    # 4. Construct Prompt
    prompt = f"""You are an AI shopping assistant for an ecommerce store.
You must ONLY answer using the provided product information.
If the user asks something unrelated to products, respond EXACTLY with:
"I can only help with products available in this store."

Do not answer general knowledge questions.

PRODUCT DATA:
{retrieved_products}

CHAT HISTORY:
{history_text}

USER QUESTION:
{user_message}

Answer helpfully based on the PRODUCT DATA and CHAT HISTORY.
"""
    
    # 5. Call LLM
    response_text = ask_llm(prompt)

    # 6. Save messages to memory
    save_message(session_id, "user", user_message)
    save_message(session_id, "assistant", response_text)

    # 7. Return response
    return response_text
