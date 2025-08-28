import streamlit as st
from langchain.prompts import ChatPromptTemplate
from langchain_community.document_loaders import UnstructuredFileLoader, TextLoader, DirectoryLoader
from langchain.embeddings import CacheBackedEmbeddings
from langchain.schema.runnable import RunnablePassthrough
from langchain.storage import LocalFileStore
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_core.output_parsers import StrOutputParser
from langchain_community.llms import Ollama
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain.retrievers import EnsembleRetriever
import os
import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
import time
import plotly.graph_objects as go
import plotly.express as px

# 분리된 모듈들 import
from ui.styles import CUSTOM_CSS
from core.prompt_builder import AdvancedPromptBuilder, extract_body_part_and_goal, _analyze_question_type, generate_nori_prompt
from core.retriever import MultiDatasetRetriever, load_datasets
from utils.helpers import print_history, add_history, format_docs
from utils.data_loader import embed_file

# 페이지 설정
st.set_page_config(
    page_title="AI 운동자세 어시스턴트",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 커스텀 CSS 적용
st.markdown(CUSTOM_CSS, unsafe_allow_html=True)

# 헤더
st.markdown("""
<div class="main-header">
    <h1>💪 AI 운동 프로그램 어시스턴트</h1>
    <p>운동 프로그램 정보를 위한 지능형 검색 시스템</p>
</div>
""", unsafe_allow_html=True)

# 세션 상태 초기화
if "messages" not in st.session_state:
    st.session_state["messages"] = []
if "search_history" not in st.session_state:
    st.session_state["search_history"] = []
if "system_stats" not in st.session_state:
    st.session_state["system_stats"] = {
        "total_searches": 0,
        "avg_response_time": 0.0,
        "datasets_used": set()
    }





# 분리된 모듈들에서 클래스들을 import하여 사용

# 분리된 모듈들에서 클래스들을 import하여 사용

# 인스턴스 생성
prompt_builder = AdvancedPromptBuilder()

# 분리된 모듈들에서 함수들을 import하여 사용

# 사이드바 설정
with st.sidebar:
    st.markdown("### 🎛️ 시스템 설정")
    
    # 문서 소스 선택
    doc_source = st.radio(
        "📚 문서 소스",
        ["🗂️ 다중 데이터셋", "📁 파일 업로드"],
        help="데이터 소스를 선택하세요"
    )
    
    if doc_source == "🗂️ 다중 데이터셋":
        st.markdown('<div class="sidebar-card">', unsafe_allow_html=True)
        st.markdown("#### 📊 데이터셋 현황")
        
        # 데이터셋 로드
        multi_retriever, available_datasets = load_datasets()
        
        if available_datasets:
            st.markdown(f'<div class="status-success">✅ {len(available_datasets)}개 데이터셋 활성화</div>', unsafe_allow_html=True)
            
            # 데이터셋 선택
            selected_datasets = st.multiselect(
                "검색 대상 선택",
                available_datasets,
                default=available_datasets[:3],  # 처음 3개만 기본 선택
                help="검색할 데이터셋을 선택하세요"
            )
            
            # 고급 설정
            with st.expander("⚙️ 고급 설정"):
                top_k = st.slider("검색 결과 개수", 1, 20, 5)
                confidence_threshold = st.slider("신뢰도 임계값", 0.1, 1.0, 0.7, 0.1)
                
        else:
            st.markdown('<div class="status-error">❌ 데이터셋 로드 실패</div>', unsafe_allow_html=True)
            selected_datasets = []
            
        st.markdown('</div>', unsafe_allow_html=True)
            
    else:  # 파일 업로드
        st.markdown('<div class="sidebar-card">', unsafe_allow_html=True)
        st.markdown("#### 📁 파일 업로드")
        
        files = st.file_uploader(
            "파일 선택", 
            type=["pdf", "txt", "docx"], 
            accept_multiple_files=True,
            help="PDF, TXT, DOCX 파일을 업로드하세요"
        )
        
        retriever = None
        if files:
            st.markdown(f'<div class="status-success">✅ {len(files)}개 파일 업로드됨</div>', unsafe_allow_html=True)
            retrievers = [embed_file(f) for f in files]
            retriever = EnsembleRetriever(retrievers=retrievers)
            
        st.markdown('</div>', unsafe_allow_html=True)
    
    # 시스템 통계
    st.markdown("### 📈 시스템 통계")
    stats = st.session_state["system_stats"]
    
    st.markdown(f"""
    <div class="metric-card">
        <h3>{stats['total_searches']}</h3>
        <p>총 검색 횟수</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown(f"""
    <div class="metric-card">
        <h3>{stats['avg_response_time']:.2f}s</h3>
        <p>평균 응답 시간</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown(f"""
    <div class="metric-card">
        <h3>{len(stats['datasets_used'])}</h3>
        <p>사용된 데이터셋</p>
    </div>
    """, unsafe_allow_html=True)

# 프롬프트 빌더 초기화
prompt_builder = AdvancedPromptBuilder()

# 메인 채팅 영역
st.markdown("### 🚀 AI 운동 프로그램 어시스턴트에 오신 것을 환영합니다!")

# 채팅 기록 표시
if st.session_state["messages"]:
    print_history()
else:

    
    # 예시 질문 버튼들
    st.markdown("### 💡 빠른 질문하기")
    
    # 버튼 1
    if st.button("💪 상체 운동을 알려주세요", key="btn1", use_container_width=True):
        st.session_state["quick_question"] = "상체 운동을 알려주세요"
        st.rerun()
    
    # 버튼 2
    if st.button("🦵 하체 강화 운동 프로그램을 찾아주세요", key="btn2", use_container_width=True):
        st.session_state["quick_question"] = "하체 강화 운동 프로그램을 찾아주세요"
        st.rerun()
    
    # 버튼 3
    if st.button("🏋️ 복근 운동을 추천해주세요", key="btn3", use_container_width=True):
        st.session_state["quick_question"] = "복근 운동을 추천해주세요"
        st.rerun()
    
    # 버튼 4
    if st.button("✋ 손목이 아플 때는 어떤 운동을 할 수 있나요?", key="btn4", use_container_width=True):
        st.session_state["quick_question"] = "손목이 아플 때는 어떤 운동을 할 수 있나요?"
        st.rerun()

# 사용자 입력 - 사이드바 밖으로 이동
user_input = st.chat_input("💭 질문을 입력하세요...")

# 빠른 질문 버튼 처리
if "quick_question" in st.session_state:
    user_input = st.session_state["quick_question"]
    del st.session_state["quick_question"]  # 한 번 사용 후 삭제

if user_input:
    # 응답 시간 측정 시작
    start_time = time.time()
    
    add_history("user", user_input)
    
    # 사용자 메시지 표시
    st.markdown(f"""
    <div style="background: #2c3e50; 
               color: white; padding: 1rem; border-radius: 10px; 
               margin: 0.5rem 0; margin-left: 20%;">
        <strong>🙋‍♂️ 사용자:</strong> {user_input}
    </div>
    """, unsafe_allow_html=True)
    
    # AI 응답 생성
    with st.spinner("🤖 AI가 답변을 생성하고 있습니다..."):
        # Ollama 연결 설정
        ollama_base_url = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
        ollama = Ollama(model="eeve-korean-10-8b", base_url=ollama_base_url)
        
        if doc_source == "🗂️ 다중 데이터셋" and selected_datasets:
            # 다중 데이터셋 검색
            all_results = []
            for dataset_name in selected_datasets:
                results = multi_retriever.search_similar_docs(user_input, dataset_name, top_k)
                for result in results:
                    result['dataset'] = dataset_name
                    all_results.append(result)
            
            # 유사도 기준으로 정렬
            all_results.sort(key=lambda x: x['similarity'], reverse=True)
            top_results = all_results[:top_k]
            
            if top_results:
                # 컨텍스트 생성 - 운동 데이터를 더 명확하게 구조화
                context_parts = []
                for i, result in enumerate(top_results, 1):
                    # full_data에서 운동 정보 추출
                    full_data = result['full_data']
                    exercise_info = f"""
=== 운동 데이터 {i} (유사도: {result['similarity']:.3f}) ===
운동명: {full_data.get('운동명', 'N/A')}
목적: {full_data.get('목적', 'N/A')}
설명: {full_data.get('설명', 'N/A')}
체력 요소: {full_data.get('체력 요소', 'N/A')}
운동 부위: {full_data.get('운동 부위', 'N/A')}
도구: {full_data.get('도구', 'N/A')}
제작연도: {full_data.get('제작연도', 'N/A')}
영상 링크: {full_data.get('영상 링크', 'N/A')}
"""
                    context_parts.append(exercise_info)
                
                context = "\n\n".join(context_parts)
                
                # 평균 신뢰도 계산
                avg_confidence = sum(r['similarity'] for r in top_results) / len(top_results)
                
                # 신뢰도가 낮으면 일반 대화 + RAG 정보 제공
                if avg_confidence < 0.3:
                    hybrid_prompt = f"""당신은 운동 전문 AI 어시스턴트입니다.
사용자의 질문에 정확하고 도움이 되는 답변을 제공하세요.

다음은 관련될 수 있는 참고 정보입니다 (신뢰도가 낮아 참고용으로만 활용):
{context}

사용자 질문: {user_input}

답변 (운동 관련 질문인 경우 4개 운동 프로그램 형태로, 일반 질문인 경우 자연스럽게 대화):"""
                    answer = ollama.invoke(hybrid_prompt)
                else:
                    # 프롬프트 생성
                    rag_prompt = prompt_builder.build_rag_prompt(
                        context=context,
                        question=user_input,
                        data_types=selected_datasets,
                        confidence_threshold=confidence_threshold
                    )
                    
                    # 답변 생성
                    answer = ollama.invoke(rag_prompt)
                
                # 검색 결과 표시
                with st.expander("🔍 검색된 문서 정보"):
                    for i, result in enumerate(top_results):
                        st.markdown(f"""
                        <div class="search-result-card">
                            <strong>{i+1}. [{result['dataset']}] (유사도: {result['similarity']:.3f})</strong><br>
                            <small>내용: {result['content'][:200]}...</small>
                        </div>
                        """, unsafe_allow_html=True)
                
                # 통계 업데이트
                response_time = time.time() - start_time
                st.session_state["system_stats"]["total_searches"] += 1
                st.session_state["system_stats"]["datasets_used"].update(selected_datasets)
                
                # 평균 응답 시간 업데이트
                current_avg = st.session_state["system_stats"]["avg_response_time"]
                total_searches = st.session_state["system_stats"]["total_searches"]
                new_avg = (current_avg * (total_searches - 1) + response_time) / total_searches
                st.session_state["system_stats"]["avg_response_time"] = new_avg
                
            else:
                # RAG 검색 실패 시 일반 대화 모드로 전환
                general_prompt = f"""당신은 운동 전문 AI 어시스턴트입니다.
사용자의 질문에 정확하고 도움이 되는 답변을 제공하세요.

운동 관련 질문인 경우:
- 4개 운동 프로그램 형태로 답변
- 목적에 맞는 구체적인 운동 추천
- 각 운동별 상세 설명 제공

일반 질문인 경우:
- 친근하고 자연스럽게 대화

사용자 질문: {user_input}

답변:"""
                
                answer = ollama.invoke(general_prompt)
                
                # 통계 업데이트
                response_time = time.time() - start_time
                st.session_state["system_stats"]["total_searches"] += 1
                
                current_avg = st.session_state["system_stats"]["avg_response_time"]
                total_searches = st.session_state["system_stats"]["total_searches"]
                new_avg = (current_avg * (total_searches - 1) + response_time) / total_searches
                st.session_state["system_stats"]["avg_response_time"] = new_avg
                
        elif doc_source == "📁 파일 업로드" and retriever:
            # 파일 업로드 방식
            retrieved_docs = retriever.invoke(user_input)
            context = format_docs(retrieved_docs)
            
            rag_prompt = prompt_builder.build_rag_prompt(
                context=context,
                question=user_input,
                data_types=["업로드된 파일"]
            )
            
            answer = ollama.invoke(rag_prompt)
            
            # 통계 업데이트
            response_time = time.time() - start_time
            st.session_state["system_stats"]["total_searches"] += 1
            
            current_avg = st.session_state["system_stats"]["avg_response_time"]
            total_searches = st.session_state["system_stats"]["total_searches"]
            new_avg = (current_avg * (total_searches - 1) + response_time) / total_searches
            st.session_state["system_stats"]["avg_response_time"] = new_avg
            
        else:
            # 일반 질문 (데이터 없이)
            if doc_source == "🗂️ 다중 데이터셋":
                answer = "❌ 데이터셋을 선택해주세요."
            else:
                answer = "❌ 파일을 업로드해주세요."
        
        # AI 응답 표시
        st.markdown(f"""
        <div style="background: #f8f9fa; 
                   padding: 1.5rem; border-radius: 15px; 
                   margin: 0.5rem 0; margin-right: 20%;
                   border-left: 5px solid #3498db;
                   box-shadow: 0 4px 15px rgba(0,0,0,0.1);
                   color: #2c3e50;">
            <strong style="color: #3498db; font-size: 1.1em;">🤖 AI 어시스턴트:</strong><br><br>
            <div style="line-height: 1.6; color: #2c3e50;">{answer}</div>
        </div>
        """, unsafe_allow_html=True)
        
        add_history("assistant", answer)
        
        # 페이지 새로고침
        st.rerun() 