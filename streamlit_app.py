import streamlit as st
from dotenv import load_dotenv
from streamlit_google_picker import google_picker

from app.services.rag_service import RAGService
from app.services.web_search import WebSearch
from app.llm.openrouter import OpenRouterLLM
from app.ingestion.ingest import IngestionPipeline


# ============================================================
# CONFIG
# ============================================================

load_dotenv()

st.set_page_config(
    page_title="Smart RAG",
    page_icon="🤖",
    layout="wide",
)


# ============================================================
# SERVICES
# ============================================================

rag = RAGService()
web_search = WebSearch()
llm = OpenRouterLLM()
pipeline = IngestionPipeline()


# ============================================================
# LOCAL PDF UPLOAD
# ============================================================

def render_local_upload():

    st.subheader("📂 Upload Documents")

    uploaded_files = st.file_uploader(
        "Upload PDF files",
        type=["pdf"],
        accept_multiple_files=True,
        key="local_pdf_upload",
    )

    if not uploaded_files:
        return

    st.write("Selected files:")

    for uploaded_file in uploaded_files:
        st.write(f"📄 {uploaded_file.name}")

    if st.button(
        "🚀 Ingest Documents",
        key="local_ingest",
    ):

        for uploaded_file in uploaded_files:

            file_path = (
                f"data/uploads/{uploaded_file.name}"
            )

            # Save PDF
            with open(file_path, "wb") as file:
                file.write(
                    uploaded_file.getbuffer()
                )

            # Ingest PDF
            with st.spinner(
                f"Processing {uploaded_file.name}..."
            ):

                document_pipeline = IngestionPipeline(
                    file_path
                )

                document_pipeline.run()

            st.success(
                f"✅ {uploaded_file.name} indexed successfully!"
            )


# ============================================================
# GOOGLE DRIVE
# ============================================================

def render_google_drive():

    st.subheader("☁️ Google Drive")

    # --------------------------------------------------------
    # LOGIN STATUS
    # --------------------------------------------------------

    if not st.user.is_logged_in:

        st.info(
            "Connect your Google account to select "
            "PDFs from Google Drive."
        )

        if st.button(
            "🔐 Login with Google",
            key="google_login",
        ):
            st.login()

        # IMPORTANT:
        # Do NOT use st.stop() here.
        # Otherwise RAG and Web Search also stop.
        return

    # --------------------------------------------------------
    # LOGGED IN
    # --------------------------------------------------------

    st.success(
        f"Connected as {st.user.name}"
    )

    if st.button(
        "Logout",
        key="google_logout",
    ):

        # pipeline.reset_collection()
        st.logout()
        return

    # --------------------------------------------------------
    # ACCESS TOKEN
    # --------------------------------------------------------

    if "access" not in st.user.tokens:

        st.error(
            "❌ Google access token is not available."
        )

        return

    access_token = st.user.tokens["access"]

    # --------------------------------------------------------
    # GOOGLE CLOUD SETTINGS
    # --------------------------------------------------------

    try:

        google_api_key = st.secrets[
            "google"
        ]["api_key"]

        google_project_number = st.secrets[
            "google"
        ]["project_number"]

    except Exception:

        st.error(
            "❌ Google API configuration is missing "
            "from .streamlit/secrets.toml."
        )

        return

    # --------------------------------------------------------
    # GOOGLE PICKER
    # --------------------------------------------------------

    selected_files = google_picker(
        label="📁 Select PDF from Google Drive",

        token=access_token,

        apiKey=google_api_key,

        appId=google_project_number,

        accept_multiple_files=True,

        type=["pdf"],

        nav_hidden=False,

        key="google_pdf_picker",
    )

    # --------------------------------------------------------
    # SELECTED FILES
    # --------------------------------------------------------

    if not selected_files:
        return

    st.success(
        f"Selected {len(selected_files)} PDF(s)."
    )

    for file in selected_files:

        st.write(
            f"📄 **{file.name}**"
        )

        st.caption(
            f"File ID: {file.id}"
        )

    # --------------------------------------------------------
    # INGEST GOOGLE DRIVE FILES
    # --------------------------------------------------------

    if st.button(
        "🚀 Ingest into ChromaDB",
        key="drive_ingest",
    ):

        for file in selected_files:

            with st.spinner(
                f"Ingesting {file.name}..."
            ):

                try:

                    # Google Drive → memory
                    pdf_bytes = file.read()

                    # memory → PDF → chunks → embeddings → ChromaDB
                    document_pipeline = (
                        IngestionPipeline()
                    )

                    document_pipeline.run_from_bytes(
                        pdf_bytes=pdf_bytes,
                        file_name=file.name,
                        file_id=file.id,
                    )

                    st.success(
                        f"✅ {file.name} indexed successfully!"
                    )

                except Exception as e:

                    st.error(
                        f"❌ Failed to ingest "
                        f"{file.name}: {e}"
                    )


# ============================================================
# DELETE DOCUMENTS
# ============================================================

def render_delete_button():

    st.divider()

    if st.button(
        "🗑️ Delete All Documents",
        key="delete_documents",
    ):

        try:

            pipeline.reset_collection()

            st.success(
                "🗑️ All documents removed from ChromaDB."
            )

        except Exception as e:

            st.error(
                f"❌ Failed to delete documents: {e}"
            )


# ============================================================
# CHAT / RAG / WEB SEARCH
# ============================================================

def render_chat(enable_web_search):

    question = st.chat_input(
        "Ask a question about your documents..."
    )

    if not question:
        return

    # --------------------------------------------------------
    # USER MESSAGE
    # --------------------------------------------------------

    with st.chat_message("user"):
        st.write(question)

    # --------------------------------------------------------
    # ASSISTANT
    # --------------------------------------------------------

    with st.chat_message("assistant"):

        # ----------------------------------------------------
        # RAG
        # ----------------------------------------------------

        with st.spinner("Searching your documents..."):

            response = rag.ask(question)

        rag_answer = response.answer

        # ----------------------------------------------------
        # IMPORTANT:
        # Use is_relevant instead of checking the text.
        # ----------------------------------------------------

        if response.is_relevant:

            final_answer = rag_answer

        # ----------------------------------------------------
        # RAG DID NOT FIND AN ANSWER
        # ----------------------------------------------------

        elif enable_web_search:

            with st.spinner("Searching the web..."):

                try:

                    web_context = web_search.search_web(
                        question
                    )

                except Exception as e:

                    st.error(
                        f"❌ Web search failed: {e}"
                    )

                    return

            # ------------------------------------------------
            # WEB SEARCH RETURNED SOMETHING
            # ------------------------------------------------

            if web_context:

                with st.spinner(
                    "Generating answer..."
                ):

                    final_answer = llm.generate(
                        f"""
Answer the user's question using the
web information below.

Web information:
{web_context}

Question:
{question}

Give a clear and accurate answer.
"""
                    )

            else:

                final_answer = (
                    "I couldn't find an answer "
                    "in your documents or on the web."
                )

        # ----------------------------------------------------
        # RAG FAILED + WEB SEARCH OFF
        # ----------------------------------------------------

        else:

            final_answer = (
                "I couldn't find the answer "
                "in your documents."
            )

        # ----------------------------------------------------
        # DISPLAY ANSWER
        # ----------------------------------------------------

        st.write(final_answer)


# ============================================================
# MAIN UI
# ============================================================

st.title("🤖 Smart RAG")

st.caption(
    "Chat with your PDFs using "
    "Retrieval-Augmented Generation (RAG)"
)


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.header("⚙️ Settings")

    # --------------------------------------------------------
    # WEB SEARCH
    # --------------------------------------------------------

    enable_web_search = st.toggle(
        "🌐 Web Search",
        value=False,
        key="enable_web_search",
    )

    st.divider()

    # --------------------------------------------------------
    # LOCAL UPLOAD
    # --------------------------------------------------------

    render_local_upload()

    # --------------------------------------------------------
    # GOOGLE DRIVE
    # --------------------------------------------------------

    st.divider()

    render_google_drive()

    # --------------------------------------------------------
    # DELETE
    # --------------------------------------------------------

    render_delete_button()


# ============================================================
# CHAT
# ============================================================

render_chat(enable_web_search)