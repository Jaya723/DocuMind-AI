import streamlit as st
import requests
import mimetypes

API_BASE = "http://localhost:8000"


st.set_page_config(
    page_title = "DocuMind AI",
    page_icon  = "📄",
    layout     = "centered"
)

if "token"    not in st.session_state: st.session_state.token    = None
if "username" not in st.session_state: st.session_state.username = None
if "messages" not in st.session_state: st.session_state.messages = []
if "file_name" not in st.session_state: st.session_state.file_name = None


def auth_headers() -> dict:
    return {"Authorization": f"Bearer {st.session_state.token}"}


def get_mime_type(filename: str) -> str:
    """
    Detect correct MIME type from file extension.
    So a CSV isn't sent as application/pdf.

    Examples:
    resume.pdf  → application/pdf
    notes.txt   → text/plain
    data.csv    → text/csv
    report.docx → application/vnd.openxmlformats-officedocument...
    """
    mime_type, _ = mimetypes.guess_type(filename)
    if mime_type is None:
        mime_type = "application/octet-stream"  
    return mime_type


def signup(username: str, email: str, password: str) -> bool:
    res = requests.post(f"{API_BASE}/auth/signup", json={
        "username": username,
        "email"   : email,
        "password": password
    })
    if res.status_code == 201:
        data = res.json()
        st.session_state.token    = data["access_token"]
        st.session_state.username = data["username"]  
        return True
    st.error(res.json().get("detail", "Signup failed."))
    return False


def login(email: str, password: str) -> bool:
    res = requests.post(f"{API_BASE}/auth/login", json={
        "email"   : email,
        "password": password
    })
    if res.status_code == 200:
        data = res.json()
        st.session_state.token    = data["access_token"]
        st.session_state.username = data["username"]   
        return True                                     
    st.error(res.json().get("detail", "Login failed."))
    return False


def upload_file(file) -> bool:
    """
    Upload any supported file type with correct MIME type.
    Detects MIME type from filename automatically.
    """
    mime_type = get_mime_type(file.name)   

    res = requests.post(
        f"{API_BASE}/upload/",
        files   = {"file": (file.name, file.getvalue(), mime_type)},
        headers = auth_headers()
    )
    if res.status_code == 200:
        data = res.json()
        st.session_state.file_name = data["filename"]
        st.success(
            f"'{data['filename']}' uploaded — "
            f"{data['chunks_count']} chunks indexed."
        )
        return True
    st.error(res.json().get("detail", "Upload failed."))
    return False


def ask_question(question: str) -> str:
    res = requests.post(
        f"{API_BASE}/rag/query",
        json    = {"question": question, "top_k": 5},
        headers = auth_headers()
    )
    if res.status_code == 200:
        return res.json()["answer"]
    return f"Error: {res.json().get('detail', 'Query failed.')}"


def load_history() -> list:
    res = requests.get(
        f"{API_BASE}/rag/history",
        headers = auth_headers()
    )
    if res.status_code == 200:
        return res.json()
    return []


def clear_history():
    requests.delete(
        f"{API_BASE}/rag/history",
        headers = auth_headers()
    )
    st.session_state.messages = []


def logout():
    st.session_state.token    = None
    st.session_state.username = None
    st.session_state.messages = []
    st.session_state.file_name = None


def page_auth():
    st.title("📄 DocuMind AI")
    st.caption("Upload a document. Ask questions. Get answers.")
    st.divider()

    tab_login, tab_signup = st.tabs(["Login", "Sign Up"])

    with tab_login:
        email    = st.text_input("Email",    key="login_email")
        password = st.text_input("Password", type="password", key="login_pass")
        if st.button("Login", use_container_width=True):
            if email and password:
                if login(email, password):
                    st.rerun()
            else:
                st.warning("Please fill in all fields.")

    with tab_signup:
        username = st.text_input("Username", key="signup_user")
        email    = st.text_input("Email",    key="signup_email")
        password = st.text_input("Password", type="password", key="signup_pass")
        if st.button("Create Account", use_container_width=True):
            if username and email and password:
                if signup(username, email, password):
                    st.rerun()
            else:
                st.warning("Please fill in all fields.")


def page_main():
    with st.sidebar:
        st.title("📄 DocuMind AI")
        st.write(f"👤 **{st.session_state.username}**")  
        st.divider()

        # File upload — all supported types
        st.subheader("Upload Document")
        uploaded_file = st.file_uploader(
            "Choose a file",
            type = ["pdf", "txt", "csv", "docx"]  
        )
        if uploaded_file:
            if st.button("Upload & Index", use_container_width=True):
                with st.spinner("Indexing document..."):
                    upload_file(uploaded_file)

        if st.session_state.file_name:
            st.success(f"📑 Active: {st.session_state.file_name}")

        st.divider()

        st.subheader("Chat History")
        if st.button("Load History", use_container_width=True):
            history = load_history()
            st.session_state.messages = []
            for h in reversed(history):
                st.session_state.messages.append(
                    {"role": "user",      "content": h["question"]}
                )
                st.session_state.messages.append(
                    {"role": "assistant", "content": h["answer"]}
                )
            st.rerun()

        if st.button("Clear History", use_container_width=True):
            clear_history()
            st.rerun()

        st.divider()
        if st.button("Logout", use_container_width=True):
            logout()
            st.rerun()

    st.title("💬 Ask your Document")

    if not st.session_state.file_name:
        st.info("👈 Upload a document from the sidebar to get started.")

    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.write(msg["content"])

    question = st.chat_input(
        "Ask a question about your document...",
        disabled = not st.session_state.file_name
    )

    if question:
        st.session_state.messages.append({"role": "user", "content": question})
        with st.chat_message("user"):
            st.write(question)

        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                answer = ask_question(question)
            st.write(answer)
            st.session_state.messages.append(
                {"role": "assistant", "content": answer}
            )


if st.session_state.token:
    page_main()
else:
    page_auth()