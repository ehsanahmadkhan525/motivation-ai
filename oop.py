from openai import OpenAI
import os
from dotenv import load_dotenv
load_dotenv()
from langchain_openai import AzureChatOpenAI, ChatOpenAI

llm = ChatOpenAI( api_key=os.getenv("GEMINI_API_KEY"),
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/", model="gemini-1.5-flash")

print(llm.invoke("Hello, how are you?"))

# client = OpenAI(
#     api_key=os.getenv("GEMINI_API_KEY"),
#     base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
# )

# response = client.chat.completions.create(
#     model="gemini-1.5-flash",
#     messages=[
#         {"role": "system", "content": "You are a helpful assistant."},
#         {"role": "user", "content": "Explain to me how AI works."}
#     ]
# )

