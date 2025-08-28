import streamlit as st
import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from langchain_community.embeddings import HuggingFaceEmbeddings
import os

class MultiDatasetRetriever:
    def __init__(self):
        self.datasets = {}
        self.embeddings_model = None
        
    def load_dataset(self, name, text_csv_path, full_csv_path, embeddings_npy_path):
        try:
            text_df = pd.read_csv(text_csv_path)
            full_df = pd.read_csv(full_csv_path)
            
            # 임베딩 파일 로드 시도 (실패해도 텍스트 검색으로 대체)
            try:
                embeddings = np.load(embeddings_npy_path)
                use_embeddings = True
            except:
                embeddings = None
                use_embeddings = False
                st.warning(f"임베딩 파일을 로드할 수 없어 텍스트 기반 검색을 사용합니다.")
            
            self.datasets[name] = {
                'text_df': text_df,
                'full_df': full_df,
                'embeddings': embeddings,
                'text_column': 'text',
                'use_embeddings': use_embeddings
            }
            
            return True
            
        except Exception as e:
            st.error(f"데이터셋 '{name}' 로드 실패: {e}")
            return False
    
    def search_similar_docs(self, query, dataset_name, top_k=5):
        if dataset_name not in self.datasets:
            return []
            
        dataset = self.datasets[dataset_name]
        
        if dataset['use_embeddings'] and dataset['embeddings'] is not None:
            # 임베딩 기반 검색
            try:
                if self.embeddings_model is None:
                    # 차원을 명시적으로 설정하여 일관성 보장
                    self.embeddings_model = HuggingFaceEmbeddings(
                        model_name="BAAI/bge-m3",
                        model_kwargs={'device': 'cpu'},
                        encode_kwargs={'normalize_embeddings': True}
                    )
                
                query_embedding = self.embeddings_model.embed_query(query)
                query_embedding = np.array(query_embedding).reshape(1, -1)
                
                similarities = cosine_similarity(query_embedding, dataset['embeddings'])[0]
                top_indices = np.argsort(similarities)[::-1][:top_k]
                
                results = []
                for idx in top_indices:
                    similarity_score = similarities[idx]
                    text_content = dataset['text_df'].iloc[idx][dataset['text_column']]
                    full_data = dataset['full_df'].iloc[idx].to_dict()
                    
                    results.append({
                        'content': text_content,
                        'similarity': similarity_score,
                        'full_data': full_data,
                        'index': idx
                    })
                    
                return results
                
            except Exception as e:
                st.warning(f"임베딩 검색 실패, 텍스트 검색으로 대체: {e}")
                dataset['use_embeddings'] = False
        
        # 텍스트 기반 검색 (임베딩 실패 시)
        if not dataset['use_embeddings']:
            query_lower = query.lower()
            results = []
            
            for idx, row in dataset['text_df'].iterrows():
                text_content = row[dataset['text_column']]
                text_lower = text_content.lower()
                
                # 키워드 매칭 점수 계산
                score = 0
                for word in query_lower.split():
                    if word in text_lower:
                        score += 1
                
                if score > 0:
                    results.append({
                        'content': text_content,
                        'similarity': score / len(query_lower.split()),  # 정규화된 점수
                        'full_data': dataset['full_df'].iloc[idx].to_dict(),
                        'index': idx
                    })
            
            # 점수 기준으로 정렬
            results.sort(key=lambda x: x['similarity'], reverse=True)
            return results[:top_k]
        
        return []
    
    def get_available_datasets(self):
        return list(self.datasets.keys())

@st.cache_resource(show_spinner=False)
def load_datasets():
    with st.spinner("🔄 데이터셋을 로딩하고 있습니다..."):
        retriever = MultiDatasetRetriever()
        
        datasets_config = {
            "실제 데이터": {
                "text_csv": "./data/text_ex.csv",
                "full_csv": "./data/full_data_ex.csv", 
                "embeddings": "./data/embeddings_ex.npy"
            }
        }
        
        loaded_datasets = []
        for name, config in datasets_config.items():
            if retriever.load_dataset(name, config["text_csv"], config["full_csv"], config["embeddings"]):
                loaded_datasets.append(name)
        
        return retriever, loaded_datasets 