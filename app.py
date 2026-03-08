import streamlit as st
import anthropic
import pypdf

st.set_page_config(page_title="Hash AI", page_icon="⚡", layout="wide")

st.title("⚡ Hash AI")
st.caption("Ask anything about your documents")

if "document_text" not in st.session_state:
    st.session_state.document_text = ""
if "messages" not in st.session_state:
    st.session_state.messages = []

col1, col2 = st.columns([1, 2])

with col1:
    st.subheader("Documents")
    uploaded_files = st.file_uploader("Upload PDFs", type="pdf", accept_multiple_files=True)
    if uploaded_files:
        all_text = ""
        for f in uploaded_files:
            reader = pypdf.PdfReader(f)
            for page in reader.pages:
                all_text += page.extract_text() + "\n"
        st.session_state.document_text = all_text
        st.session_state.messages = []
        st.success(f"✓ {len(uploaded_files)} document(s) loaded")

with col2:
    st.subheader("Conversation")
    
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.write(msg["content"])

    question = st.chat_input("Ask a question about your documents...")

    if question and st.session_state.document_text:
        st.session_state.messages.append({"role": "user", "content": question})
        
        with st.chat_message("user"):
            st.write(question)

        client = anthropic.Anthropic()
        response = client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=1000,
            messages=[{
                "role": "user",
                "content": f"Based on these documents:\n\n{st.session_state.document_text[:10000]}\n\nAnswer this question: {question}"
            }]
        )
        answer = response.content[0].text
        st.session_state.messages.append({"role": "assistant", "content": answer})
        
        with st.chat_message("assistant"):
            st.write(answer)

    elif question and not st.session_state.document_text:
        st.warning("Please upload a document first.")