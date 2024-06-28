import os

from groq import Groq

# [RC Note:] This was the feature I was probably most stressed about but because there is so much information on the LLM integration
# it was actually very easy to follow the instructions, additionally we had learned about the API key previously and so it 
# was not completely foreign. I did not play too much with the prompt as the initial outputs were sufficient for the demo. 
# In the future it would be interesting to expand this to maybe summarizing a profile using AI rather than just one section. 
# Additionally, expanding this to the student profiles. 
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
        # The Groq API key was actually saved in my terminal as an export. I learned that this was the most secure way to save
        # the key. I don't expect that you will try run the code because you have seen the demo, but if you want the API code- let me know :)
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
