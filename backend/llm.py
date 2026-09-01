import os

from dotenv import load_dotenv

from langchain_huggingface import ChatHuggingFace
from langchain_huggingface import HuggingFaceEndpoint


load_dotenv()


HF_API_KEY = os.getenv("HF_API_KEY")

if not HF_API_KEY:
    raise ValueError(
        "HF_API_KEY is not configured"
    )


llm = HuggingFaceEndpoint(
    repo_id="meta-llama/Llama-3.1-8B-Instruct",
    huggingfacehub_api_token=HF_API_KEY,
    max_new_tokens=512,
    temperature=0.1
)


chat_model = ChatHuggingFace(
    llm=llm
)