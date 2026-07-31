import streamlit as st
from app.services.rag_service import RAGService
from app.services.web_search import WebSearch
from app.llm.openrouter import OpenRouterLLM

rag = RAGService() 
web_search = WebSearch()
llm = OpenRouterLLM()

st.set_page_config( 
    page_title="Smart RAG",
      page_icon="🤖", 
      layout="wide", 
      ) 

st.title("🤖 Smart RAG") 

st.caption("Chat with your PDFs using Retrieval-Augmented Generation (RAG)") 

with st.sidebar: 
    st.header("Settings") 
    
    enable_web_search = st.toggle( 
        "Enable Web Search",
          value=False, 
          ) 
    
    st.divider() 
    
    st.subheader("📂 Upload Documents") 
    
    uploaded_files = st.file_uploader( 
        "Upload PDF files", 
        type=["pdf"], 
        accept_multiple_files=True 
        ) 
    

            
    
question = st.chat_input( "Ask a question about your documents..." ) 

if question:

    with st.chat_message("user"):
        st.write(question)


    with st.spinner("Thinking..."):

        response = rag.ask(question)


        if response.answer != "I couldn't find the answer in the uploaded documents.":

            final_answer = response.answer


        elif enable_web_search:

            web_context = web_search.search_web(question)


            final_answer = llm.generate(
                f"""
                Answer the question using this web information.

                Context:
                {web_context}

                Question:
                {question}
                """
            )


        else:

            final_answer = (
                "I couldn't find the answer in your documents."
            )


    with st.chat_message("assistant"):
        st.write(final_answer)



    
    
   