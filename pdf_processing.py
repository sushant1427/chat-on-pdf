import fitz  # PyMuPDF
from langchain_text_splitters import RecursiveCharacterTextSplitter

def get_pdf_chunks(uploaded_file):
    """Extract text from PDF and split into chunks"""
    pdf_document = fitz.open(stream=uploaded_file.read(), filetype="pdf")
    full_text = ""
    for page in pdf_document:
        full_text += page.get_text()

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
        length_function=len
    )
    return text_splitter.split_text(full_text)


def get_relevant_context(question, chunks, top_k=3):
    """Retrieve relevant PDF chunks for a given question"""
    relevant = []
    q_words = set(question.lower().split())
    for chunk in chunks:
        c_words = set(chunk.lower().split())
        if not q_words.isdisjoint(c_words):
            relevant.append(chunk)
    return "\n\n".join(relevant[:top_k])
