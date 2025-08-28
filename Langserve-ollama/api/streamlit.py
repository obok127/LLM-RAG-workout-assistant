import streamlit.web.bootstrap as bootstrap
import sys
import os

# Streamlit 앱 경로 설정
app_path = os.path.join(os.path.dirname(__file__), "..", "app", "main.py")

def run_streamlit():
    """Streamlit 앱을 실행하는 함수"""
    sys.argv = ["streamlit", "run", app_path, "--server.port", "8501", "--server.address", "0.0.0.0"]
    bootstrap.run()

if __name__ == "__main__":
    run_streamlit() 