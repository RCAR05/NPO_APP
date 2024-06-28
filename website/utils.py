import os

from groq import Groq


def get_ai_project(human_project_desc: str):

    prompt = (
        "Rewrite the description below in concise yet compelling "
        "business language. The description should entice a prospective "
        "joiner to apply for participation in the project. The response "
        "should be no longer than 100 words. Do not tell me that you are rewriting. \n\n Initial description: "
        f"'{human_project_desc}'."
    )

    ai_project_desc = get_groq_response(prompt)
    return ai_project_desc.choices[0].message.content

def get_groq_response(prompt: str):
    client = Groq(
        api_key=os.environ.get("GROQ_API_KEY"),
    )
    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": prompt,
            }
        ],
        model="llama3-8b-8192",
    )
    return chat_completion
