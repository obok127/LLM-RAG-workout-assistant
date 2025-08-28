# CSS 스타일 정의

CUSTOM_CSS = """
<style>
    /* 메인 배경 */
    .main {
        background: white;
        padding: 0rem 1rem;
    }
    
    /* 사이드바 스타일링 */
    .css-1d391kg {
        background: linear-gradient(180deg, #2c3e50 0%, #34495e 100%);
    }
    
    /* 헤더 스타일링 */
    .main-header {
        background: rgba(255,255,255,0.95);
        padding: 2rem;
        border-radius: 15px;
        margin-bottom: 2rem;
        box-shadow: 0 4px 20px rgba(0,0,0,0.1);
        border-left: 6px solid #3498db;
    }
    
    .main-header h1 {
        color: #2c3e50;
        text-align: left;
        font-size: 2.5rem;
        margin-bottom: 0.5rem;
    }
    
    .main-header p {
        color: #7f8c8d;
        text-align: left;
        font-size: 1.1rem;
        margin: 0;
    }
    
    /* 카드 스타일링 */
    .info-card {
        background: rgba(255,255,255,0.95);
        padding: 1.5rem;
        border-radius: 12px;
        margin: 1rem 0;
        box-shadow: 0 4px 20px rgba(0,0,0,0.1);
        border-left: 4px solid #3498db;
    }
    
    .metric-card {
        background: rgba(255,255,255,0.95);
        padding: 1.5rem;
        border-radius: 12px;
        margin: 0.5rem 0;
        color: #2c3e50;
        text-align: left;
        box-shadow: 0 4px 20px rgba(0,0,0,0.1);
        border-left: 4px solid #3498db;
    }
    
    .metric-card h3 {
        margin: 0 0 0.5rem 0;
        font-size: 1.8rem;
        color: #2c3e50;
    }
    
    .metric-card p {
        margin: 0;
        color: #7f8c8d;
    }
    
    /* 채팅 스타일링 */
    .chat-container {
        background: rgba(255,255,255,0.95);
        border-radius: 15px;
        padding: 1rem;
        margin: 1rem 0;
        box-shadow: 0 4px 20px rgba(0,0,0,0.1);
        max-height: 500px;
        overflow-y: auto;
    }
    
    /* 모델 응답 배경색 */
    .stChatMessage[data-testid="assistant"] {
        background: white !important;
    }
    
    /* 버튼 스타일링 */
    .stButton > button {
        background: rgba(255,255,255,0.95);
        color: #2c3e50;
        border: 2px solid #3498db;
        padding: 1rem 1.5rem;
        border-radius: 12px;
        font-weight: 600;
        transition: all 0.3s ease;
        box-shadow: 0 4px 20px rgba(0,0,0,0.1);
        margin: 0.25rem 0;
        width: 100%;
        text-align: left;
    }
    
    .stButton > button:hover {
        background: rgba(52,152,219,0.05);
        border-color: #2980b9;
        transform: translateY(-2px);
        box-shadow: 0 6px 25px rgba(52,152,219,0.2);
    }
    
    /* 사이드바 카드 */
    .sidebar-card {
        background: rgba(255,255,255,0.1);
        padding: 1rem;
        border-radius: 10px;
        margin: 1rem 0;
        border: 1px solid rgba(255,255,255,0.2);
    }
    
    /* 상태 표시 */
    .status-success {
        background: #27ae60;
        color: white;
        padding: 0.5rem 1rem;
        border-radius: 20px;
        text-align: center;
        margin: 0.5rem 0;
    }
    
    .status-error {
        background: #e74c3c;
        color: white;
        padding: 0.5rem 1rem;
        border-radius: 20px;
        text-align: center;
        margin: 0.5rem 0;
    }
    
    /* 로딩 애니메이션 */
    .loading-spinner {
        display: flex;
        justify-content: center;
        align-items: center;
        height: 100px;
    }
    
    .spinner {
        border: 4px solid #f3f3f3;
        border-top: 4px solid #3498db;
        border-radius: 50%;
        width: 40px;
        height: 40px;
        animation: spin 1s linear infinite;
    }
    
    @keyframes spin {
        0% { transform: rotate(0deg); }
        100% { transform: rotate(360deg); }
    }
    
    /* 검색 결과 카드 */
    .search-result-card {
        background: rgba(255,255,255,0.9);
        padding: 1rem;
        border-radius: 10px;
        margin: 0.5rem 0;
        border-left: 4px solid #3498db;
        box-shadow: 0 2px 10px rgba(0,0,0,0.1);
    }
    
    .search-result-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 15px rgba(0,0,0,0.15);
        transition: all 0.3s ease;
    }
    
    /* 입력 필드 스타일링 */
    .stTextInput > div > div > input {
        background: rgba(255,255,255,0.9);
        border: 2px solid rgba(52,152,219,0.3);
        border-radius: 10px;
        padding: 0.75rem;
    }
    
    .stTextInput > div > div > input:focus {
        border-color: #3498db;
        box-shadow: 0 0 0 3px rgba(52,152,219,0.1);
    }
    
    /* 파일 업로더 스타일링 */
    .stFileUploader > div {
        background: rgba(255,255,255,0.9);
        border: 2px dashed rgba(52,152,219,0.3);
        border-radius: 10px;
        padding: 1rem;
    }
    
    .stFileUploader > div:hover {
        border-color: #3498db;
        background: rgba(52,152,219,0.05);
    }
</style>
""" 