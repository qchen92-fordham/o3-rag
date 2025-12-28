from openai import OpenAI
from rag_example import search_in_vectorstore

client = OpenAI()

def chat(query, chat_history):
    # user_input = input("Enter your message: ")
    # context = search_in_vectorstore(user_input)
    context = search_in_vectorstore(query)
    prompt_with_context = f"Context: {context}\n\nUser input: {query}"

    # save the conversation history
    chat_history.append({"role": "user", "content": prompt_with_context})

    response = client.chat.completions.create(
        model="o3-mini-2025-01-31",
        messages=chat_history,
        stream=True, #stream response, like ChatGPT generates live response
    )

    # store the response in chat history
    complete_response = ""

    for chunk in response:
        if chunk.choices[0].delta.content is not None:
            complete_response += chunk.choices[0].delta.content
            yield chunk.choices[0].delta.content

# for chunk in chat("Where is the closest bike station? I live near Berlin Ostbahnhof.\
#                   Please list all locations that are neaby." #if you add this, you will see the result chunk by chunk
#                   #just like ChatGPT streaming the response.
#                   ):
#     print(chunk, end="", flush=True)

    chat_history.append({"role": "assistant", "content": complete_response})