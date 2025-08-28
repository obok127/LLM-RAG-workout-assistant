import streamlit as st

def print_history():
    """대화 기록 표시 (향상된 스타일)"""
    st.markdown('<div class="chat-container">', unsafe_allow_html=True)
    
    for message in st.session_state["messages"]:
        if message["role"] == "user":
            st.markdown(f"""
            <div style="background: #3498db; color: white; padding: 1rem; border-radius: 15px; margin: 0.5rem 0; text-align: right;">
                <strong>사용자:</strong> {message["content"]}
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div style="background: #ecf0f1; color: #2c3e50; padding: 1rem; border-radius: 15px; margin: 0.5rem 0; border-left: 4px solid #3498db;">
                <strong>노리:</strong> {message["content"]}
            </div>
            """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

def add_history(role, content):
    st.session_state["messages"].append({"role": role, "content": content})

def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs) 