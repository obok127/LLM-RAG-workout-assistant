#LangServe에서 Ollama 체인 생성
from langchain_community.chat_models import ChatOllama
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate

# LLM 지정 (Ollama + 모델명)
llm = ChatOllama(model="eeve-korean-10-8b:latest")

# 프롬프트 템플릿
prompt = ChatPromptTemplate.from_template(
    "다음 질문에 한국어로 답변하세요:\n{user_prompt}"
)


# LangChain expression chain
chain = prompt | llm | StrOutputParser()

