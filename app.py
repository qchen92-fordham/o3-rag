from openai import OpenAI
from rag_example import search_in_vectorstore

client = OpenAI()

def chat(query):
    # user_input = input("Enter your message: ")
    # context = search_in_vectorstore(user_input)
    context = search_in_vectorstore(query)
    prompt_with_context = f"Context: {context}\n\nUser input: {query}"

    response = client.chat.completions.create(
        model="o3-mini-2025-01-31",
        messages=[{"role": "user", "content": prompt_with_context}],
    )

    return response.choices[0].message.content

print(chat("Where is the closest bike station? I live near Berlin Ostbahnhof."))
