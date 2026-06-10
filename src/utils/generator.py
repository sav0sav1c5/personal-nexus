# Generates an answer using Groq LLM based on retrieved context

import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

def build_prompt(query, retrieved_chunks):

    context_parts = []

    for i, chunk in enumerate(retrieved_chunks):
        source = chunk['metadata'].get('name', 'unknown')
        content = chunk['content']
        context_parts.append(f"[Source {i+1}: {source}]\n{content}")

    context_block = "\n\n".join(context_parts)

    prompt = f"""You are a helpful assistant. Answer the user's question based ONLY on the provided context.
If the answer is not found in the context, say that you don't have enough information.
Always cite which source(s) you used at the end of your answer.

Context:
{context_block}

Question: {query}

Answer:"""

    return prompt


def generate(query, retrieved_chunks):

    print("\n\nPhase 6: Answer generation starting...")

    if not retrieved_chunks:
        print('- No chunks provided, cannot generate answer!')
        return "No relevant information found."

    # Build the full prompt
    prompt = build_prompt(query, retrieved_chunks)
    print(f'- Prompt built with {len(retrieved_chunks)} context chunks')

    # Initialize Groq client
    client = Groq(api_key=os.getenv('GROQ_API_KEY'))

    # Send request to LLM
    print('- Sending request to Groq (llama-3.3-70b-versatile)...')
    response = client.chat.completions.create(
        model='llama-3.3-70b-versatile',
        messages=[
            {
                'role': 'user',
                'content': prompt
            }
        ],
        # Low temperature = more focused, less creative answers
        temperature=0.2,
        max_tokens=512
    )

    # Extract the text answer from the response object
    answer = response.choices[0].message.content

    print("Phase 6: Answer generation finished!")

    return answer