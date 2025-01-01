import streamlit as st
import PyPDF2
from llama_index.llms.ollama import Ollama

# Initialize the Ollama model
llm = Ollama(model="llama3.1:latest", base_url="http://10.0.11i.180:11434", request_timeout=60.0)

# Function to extract text from PDF
def extract_text_from_pdf(pdf_file):
    reader = PyPDF2.PdfReader(pdf_file)
    text = ""
    for page in reader.pages:
        text += page.extract_text()
    return text

# Streamlit App
st.title("📄 PDF Chatbot with Ollama")

# Upload PDF file
uploaded_file = st.file_uploader("Upload a PDF file", type="pdf")

# Initialize session state for chat history
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if uploaded_file is not None:
    # Extract text from PDF
    pdf_text = extract_text_from_pdf(uploaded_file)
    st.success("PDF uploaded and text extracted successfully!")

    # Separate interface for conversation
    st.subheader("Conversation History")

    # Display chat history in a structured format
    for i, message in enumerate(st.session_state.chat_history):
        if message["role"] == "user":
            st.markdown(f"**Query {i//2 + 1}:** {message['content']}")
        elif message["role"] == "assistant":
            st.markdown(f"**Response {i//2 + 1}:** {message['content']}")
            st.markdown("---")  # Add a separator between query-response pairs

    # Chat input
    user_input = st.text_input("Ask a question about the PDF:")

    if user_input:
        # Add user question to chat history
        st.session_state.chat_history.append({"role": "user", "content": user_input})

        # Combine PDF text with user input
        prompt = f"PDF Content: {pdf_text}\n\nUser Question: {user_input}"

        # Generate response using Ollama
        with st.spinner("Generating response..."):
            response = llm.complete(prompt)

        # Add bot response to chat history
        st.session_state.chat_history.append({"role": "assistant", "content": str(response)})

        # Rerun the app to update the conversation history
        st.rerun()
else:
    st.info("Please upload a PDF file to get started.")
