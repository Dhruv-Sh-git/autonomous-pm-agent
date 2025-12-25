from groq import Groq
import os


client = Groq(api_key=os.getenv("GROQ_API_KEY"))


def generate_answer(query, context):
    prompt = f"""
Use the context below to answer the question.

Context:
{context}

Question:
{query}
"""
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",  # or any other Groq model you prefer
        messages=[{"role": "user", "content": prompt}],
    )
    return response.choices[0].message.content
