from langchain_core.prompts import ChatPromptTemplate
from langchain_core.documents import Document


RAG_PROMPT = ChatPromptTemplate.from_template(
    """
    You are an intelligent AI assistant.

Your task is to answer the user's question ONLY using the provided context.

Rules:
1. Use only the information present in the context.
2. Do not use your own knowledge.
3. If the answer cannot be found in the context, reply:
   "I couldn't find the answer in the uploaded documents."
4. Keep the answer concise and accurate.
5. If possible, explain the answer in a clear and structured manner.

Context:
{context}

Question:
{question}

Answer:
"""
)

def build_prompt(question: str, documents: list[Document]) -> str:
    context = "\n\n".join(doc.page_content for doc in documents)

    prompt = RAG_PROMPT.format(
        context=context,
        question=question,
    )

    return prompt