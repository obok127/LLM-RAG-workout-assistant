from langchain_community.chat_models import ChatOllama
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

llm = ChatOllama(model="eeve-korean-10-8b:latest")

prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You are a helpful AI Assistant. Your name is '라마2'. You must answer in Korean."
        ),
        MessagesPlaceholder(variable_name="messages")
    ]
)

chain = prompt | llm | StrOutputParser()
