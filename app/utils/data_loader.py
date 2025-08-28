import pandas as pd
import numpy as np
import streamlit as st
from pathlib import Path
from typing import Dict, List, Optional, Tuple

# For embed_file utility
from langchain_community.document_loaders import UnstructuredFileLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.embeddings import CacheBackedEmbeddings
from langchain.storage import LocalFileStore

class DataLoader:
    """데이터 로딩 및 관리를 담당하는 클래스"""
    
    def __init__(self, data_dir: str = "./data"):
        self.data_dir = Path(data_dir)
        self.datasets = {}
        self.embeddings = {}
    
    def load_csv_data(self, file_path: str) -> Optional[pd.DataFrame]:
        """CSV 파일을 로드하는 함수"""
        try:
            full_path = self.data_dir / file_path
            if full_path.exists():
                df = pd.read_csv(full_path)
                st.success(f"✅ {file_path} 로드 완료 ({len(df)}행)")
                return df
            else:
                st.error(f"❌ 파일을 찾을 수 없습니다: {full_path}")
                return None
        except Exception as e:
            st.error(f"❌ CSV 로드 실패: {e}")
            return None
    
    def load_embeddings(self, file_path: str) -> Optional[np.ndarray]:
        """임베딩 파일을 로드하는 함수"""
        try:
            full_path = self.data_dir / file_path
            if full_path.exists():
                embeddings = np.load(full_path)
                st.success(f"✅ {file_path} 로드 완료 (차원: {embeddings.shape})")
                return embeddings
            else:
                st.warning(f"⚠️ 임베딩 파일을 찾을 수 없습니다: {full_path}")
                return None
        except Exception as e:
            st.warning(f"⚠️ 임베딩 로드 실패: {e}")
            return None
    
    def load_dataset(self, name: str, text_csv: str, full_csv: str, embeddings_npy: str) -> bool:
        """전체 데이터셋을 로드하는 함수"""
        try:
            # 텍스트 데이터 로드
            text_df = self.load_csv_data(text_csv)
            if text_df is None:
                return False
            
            # 전체 데이터 로드
            full_df = self.load_csv_data(full_csv)
            if full_df is None:
                return False
            
            # 임베딩 로드 (선택적)
            embeddings = self.load_embeddings(embeddings_npy)
            
            # 데이터셋 저장
            self.datasets[name] = {
                'text_df': text_df,
                'full_df': full_df,
                'embeddings': embeddings,
                'text_column': 'text',
                'use_embeddings': embeddings is not None
            }
            
            return True
            
        except Exception as e:
            st.error(f"❌ 데이터셋 '{name}' 로드 실패: {e}")
            return False
    
    def get_dataset_info(self, name: str) -> Optional[Dict]:
        """데이터셋 정보를 반환하는 함수"""
        if name not in self.datasets:
            return None
        
        dataset = self.datasets[name]
        text_df = dataset['text_df']
        full_df = dataset['full_df']
        embeddings = dataset['embeddings']
        
        info = {
            'name': name,
            'text_rows': len(text_df),
            'full_rows': len(full_df),
            'text_columns': list(text_df.columns),
            'full_columns': list(full_df.columns),
            'has_embeddings': embeddings is not None,
            'embedding_shape': embeddings.shape if embeddings is not None else None
        }
        
        return info
    
    def get_available_datasets(self) -> List[str]:
        """사용 가능한 데이터셋 목록을 반환하는 함수"""
        return list(self.datasets.keys())
    
    def validate_data_consistency(self, name: str) -> bool:
        """데이터 일관성을 검증하는 함수"""
        if name not in self.datasets:
            return False
        
        dataset = self.datasets[name]
        text_df = dataset['text_df']
        full_df = dataset['full_df']
        
        # 행 수 일치 확인
        if len(text_df) != len(full_df):
            st.error(f"❌ 데이터 불일치: text_df({len(text_df)}행) != full_df({len(full_df)}행)")
            return False
        
        # 임베딩 차원 확인
        if dataset['embeddings'] is not None:
            if len(dataset['embeddings']) != len(text_df):
                st.error(f"❌ 임베딩 차원 불일치: embeddings({len(dataset['embeddings'])}개) != text_df({len(text_df)}행)")
                return False
        
        st.success(f"✅ 데이터 일관성 검증 완료: {name}")
        return True
    
    def get_sample_data(self, name: str, n_samples: int = 5) -> Optional[Dict]:
        """샘플 데이터를 반환하는 함수"""
        if name not in self.datasets:
            return None
        
        dataset = self.datasets[name]
        text_df = dataset['text_df']
        full_df = dataset['full_df']
        
        # 랜덤 샘플 선택
        sample_indices = np.random.choice(len(text_df), min(n_samples, len(text_df)), replace=False)
        
        samples = []
        for idx in sample_indices:
            sample = {
                'text': text_df.iloc[idx][dataset['text_column']],
                'full_data': full_df.iloc[idx].to_dict(),
                'index': idx
            }
            samples.append(sample)
        
        return {
            'dataset_name': name,
            'samples': samples,
            'total_rows': len(text_df)
        }
    
    def search_text_data(self, query: str, name: str, top_k: int = 5) -> List[Dict]:
        """텍스트 기반 검색을 수행하는 함수"""
        if name not in self.datasets:
            return []
        
        dataset = self.datasets[name]
        text_df = dataset['text_df']
        full_df = dataset['full_df']
        
        query_lower = query.lower()
        results = []
        
        for idx, row in text_df.iterrows():
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
                    'full_data': full_df.iloc[idx].to_dict(),
                    'index': idx
                })
        
        # 점수 기준으로 정렬
        results.sort(key=lambda x: x['similarity'], reverse=True)
        return results[:top_k]


def embed_file(file):
    """업로드 파일을 분할/임베딩해 FAISS 리트리버를 반환합니다."""
    with st.spinner(f"📄 {getattr(file, 'name', 'uploaded')} 처리 중..."):
        # 저장 및 경로 준비
        save_dir = Path("./cache/files")
        save_dir.mkdir(parents=True, exist_ok=True)
        file_name = getattr(file, 'name', 'uploaded_file')
        file_path = save_dir / file_name
        # 파일 저장
        content = file.read()
        with open(file_path, "wb") as f_out:
            f_out.write(content)

        # 문서 로드/분할
        cache_dir = LocalFileStore(f"./.cache/embeddings/{file_name}")
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=500,
            chunk_overlap=50,
            separators=["\n\n", "\n", r"(?<=\.)", " ", ""],
            length_function=len,
        )
        loader = UnstructuredFileLoader(str(file_path))
        docs = loader.load_and_split(text_splitter=text_splitter)

        # 임베딩/벡터스토어
        embeddings = HuggingFaceEmbeddings(model_name="BAAI/bge-m3")
        cached_embeddings = CacheBackedEmbeddings.from_bytes_store(embeddings, cache_dir)
        vectorstore = FAISS.from_documents(docs, cached_embeddings)
        return vectorstore.as_retriever()

@st.cache_resource(show_spinner=False)
def create_data_loader() -> DataLoader:
    """데이터 로더 인스턴스를 생성하는 함수 (캐시됨)"""
    return DataLoader()

@st.cache_data(show_spinner=False)
def load_all_datasets() -> Dict[str, bool]:
    """모든 데이터셋을 로드하는 함수 (캐시됨)"""
    with st.spinner("🔄 데이터셋을 로딩하고 있습니다..."):
        loader = create_data_loader()
        
        datasets_config = {
            "실제 데이터": {
                "text_csv": "text_ex.csv",
                "full_csv": "full_data_ex.csv", 
                "embeddings": "embeddings_ex.npy"
            }
        }
        
        results = {}
        for name, config in datasets_config.items():
            success = loader.load_dataset(
                name, 
                config["text_csv"], 
                config["full_csv"], 
                config["embeddings"]
            )
            results[name] = success
            
            if success:
                loader.validate_data_consistency(name)
        
        return results 