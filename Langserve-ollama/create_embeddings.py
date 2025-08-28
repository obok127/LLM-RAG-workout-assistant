import pandas as pd
import numpy as np
from langchain_community.embeddings import HuggingFaceEmbeddings
import os

def create_sample_embeddings():
    """샘플 데이터의 임베딩을 생성하는 함수"""
    
    # 데이터 로드
    text_df = pd.read_csv("./data/text_ex.csv")
    
    # 임베딩 모델 초기화 (main.py와 동일한 설정)
    embeddings_model = HuggingFaceEmbeddings(
        model_name="BAAI/bge-m3",
        model_kwargs={'device': 'cpu'},
        encode_kwargs={'normalize_embeddings': True}
    )
    
    print("임베딩 생성 중...")
    
    # 각 텍스트에 대해 임베딩 생성
    embeddings_list = []
    for text in text_df['text']:
        embedding = embeddings_model.embed_query(text)
        embeddings_list.append(embedding)
    
    # numpy 배열로 변환
    embeddings_array = np.array(embeddings_list)
    
    # 저장
    np.save("./data/embeddings_ex.npy", embeddings_array)
    
    print(f"임베딩 생성 완료! 형태: {embeddings_array.shape}")
    print(f"저장 위치: ./data/embeddings_ex.npy")

if __name__ == "__main__":
    create_sample_embeddings() 