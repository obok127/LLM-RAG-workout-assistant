import streamlit as st

def render_header():
    """헤더 컴포넌트 렌더링"""
    st.markdown("""
    <div class="main-header">
        <h1>💪 AI 운동 프로그램 어시스턴트</h1>
        <p>운동 프로그램 정보를 위한 지능형 검색 시스템</p>
    </div>
    """, unsafe_allow_html=True)

def render_quick_questions():
    """빠른 질문 버튼들 렌더링"""
    st.markdown("### 🚀 AI 운동 프로그램 어시스턴트에 오신 것을 환영합니다!")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("🏃‍♂️ 상체 운동 추천해줘", use_container_width=True):
            st.session_state["quick_question"] = "상체 운동 추천해줘"
        if st.button("🦵 하체 운동 추천해줘", use_container_width=True):
            st.session_state["quick_question"] = "하체 운동 추천해줘"
        if st.button("💪 코어 운동 추천해줘", use_container_width=True):
            st.session_state["quick_question"] = "코어 운동 추천해줘"
    
    with col2:
        if st.button("🧘‍♀️ 스트레칭 추천해줘", use_container_width=True):
            st.session_state["quick_question"] = "스트레칭 추천해줘"
        if st.button("🏋️‍♀️ 전신 운동 추천해줘", use_container_width=True):
            st.session_state["quick_question"] = "전신 운동 추천해줘"
        if st.button("🎯 목적별 운동 추천해줘", use_container_width=True):
            st.session_state["quick_question"] = "목적별 운동 추천해줘"

def render_metrics():
    """메트릭 카드들 렌더링"""
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown(f"""
        <div class="metric-card">
            <h3>📊 {st.session_state["system_stats"]["total_searches"]}</h3>
            <p>총 검색 횟수</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        avg_time = st.session_state["system_stats"]["avg_response_time"]
        st.markdown(f"""
        <div class="metric-card">
            <h3>⏱️ {avg_time:.1f}s</h3>
            <p>평균 응답 시간</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        datasets_count = len(st.session_state["system_stats"]["datasets_used"])
        st.markdown(f"""
        <div class="metric-card">
            <h3>📚 {datasets_count}</h3>
            <p>활용 데이터셋</p>
        </div>
        """, unsafe_allow_html=True)

def render_sidebar():
    """사이드바 컴포넌트 렌더링"""
    with st.sidebar:
        st.markdown("## 🔧 설정")
        
        # 데이터셋 선택
        st.markdown("### 📚 데이터셋 선택")
        dataset_options = ["실제 데이터", "샘플 데이터"]
        selected_dataset = st.selectbox(
            "사용할 데이터셋을 선택하세요:",
            dataset_options,
            index=0
        )
        
        # 검색 설정
        st.markdown("### 🔍 검색 설정")
        top_k = st.slider("검색 결과 수:", min_value=1, max_value=10, value=5)
        confidence_threshold = st.slider(
            "신뢰도 임계값:", 
            min_value=0.0, 
            max_value=1.0, 
            value=0.7, 
            step=0.1
        )
        
        # 시스템 정보
        st.markdown("### ℹ️ 시스템 정보")
        st.info("""
        **AI 운동 프로그램 어시스턴트**
        
        - **모델**: EEVE-Korean-10.8B
        - **임베딩**: BAAI/bge-m3
        - **검색**: FAISS + Cosine Similarity
        """)
        
        return {
            "selected_dataset": selected_dataset,
            "top_k": top_k,
            "confidence_threshold": confidence_threshold
        } 