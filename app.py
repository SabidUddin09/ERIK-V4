import streamlit as st
from googlesearch import search
import requests
from bs4 import BeautifulSoup
import fitz  # PyMuPDF
import docx
import sympy as sp
import matplotlib.pyplot as plt
import io
import random
from pytube import YouTube

# ------------------ ERIK v4 ------------------
st.set_page_config(page_title="ERIK v4 - AI Academic Assistant", layout="wide")

st.title("🧠 ERIK v4 - Exceptional Resources & Intelligence Kernel")

# ------------------ Sidebar ------------------
st.sidebar.header("Features")
mode = st.sidebar.radio("Choose a feature:", ["Ask Question", "Math Solver", "Quiz Generator", "PDF/Text Analyzer", "YouTube Class Search", "Graph Generator"])

# ------------------ Ask Question ------------------
if mode == "Ask Question":
    query = st.text_input("Ask anything:")
    if st.button("Search & Answer"):
        st.info("Searching Google and generating answer...")
        results = []
        try:
            for url in search(query, num_results=5):
                results.append(url)
        except:
            st.error("Error searching Google.")
        
        answer = ""
        for link in results:
            try:
                r = requests.get(link, timeout=3)
                soup = BeautifulSoup(r.text, 'html.parser')
                paragraphs = soup.find_all('p')
                for p in paragraphs[:3]:
                    answer += p.get_text() + "\n"
            except:
                continue
        
        if answer:
            st.markdown("**Answer from web sources:**")
            st.write(answer)
            st.markdown("**Top sources:**")
            for r in results:
                st.write(f"- {r}")
        else:
            st.warning("No answer found. Try rephrasing the question.")

# ------------------ Math Solver ------------------
elif mode == "Math Solver":
    st.subheader("Math Problem Solver")
    problem = st.text_area("Enter a math problem (symbolic or numeric):")
    if st.button("Solve"):
        try:
            x = sp.symbols('x')
            solution = sp.solve(problem, x)
            st.success(f"Solution: {solution}")
        except Exception as e:
            st.error(f"Error: {e}")

# ------------------ Quiz Generator ------------------
elif mode == "Quiz Generator":
    st.subheader("Generate Multiple Choice Questions")
    topic = st.text_input("Enter topic:")
    num_q = st.number_input("Number of questions:", min_value=1, max_value=20, value=5)
    if st.button("Generate Quiz"):
        for i in range(num_q):
            st.write(f"Q{i+1}: This is a placeholder question about {topic}?")
            st.write("a) Option A  b) Option B  c) Option C  d) Option D")

# ------------------ PDF/Text Analyzer ------------------
elif mode == "PDF/Text Analyzer":
    st.subheader("Upload PDF or DOCX")
    uploaded_file = st.file_uploader("Choose a file", type=['pdf','docx','txt'])
    if uploaded_file:
        text = ""
        if uploaded_file.type == "application/pdf":
            doc = fitz.open(stream=uploaded_file.read(), filetype="pdf")
            for page in doc:
                text += page.get_text()
        elif uploaded_file.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
            doc = docx.Document(uploaded_file)
            for para in doc.paragraphs:
                text += para.text + "\n"
        else:
            text = str(uploaded_file.read(), "utf-8")
        st.text_area("Extracted Text", text, height=300)

# ------------------ YouTube Class Search ------------------
elif mode == "YouTube Class Search":
    st.subheader("Search YouTube Classes")
    keyword = st.text_input("Enter topic or class:")
    if st.button("Search YouTube"):
        st.info("Fetching top videos...")
        query = f"{keyword} site:youtube.com"
        links = []
        try:
            for url in search(query, num_results=5):
                links.append(url)
        except:
            st.error("Error searching YouTube.")
        st.write("Top Results:")
        for l in links:
            st.write(l)

# ------------------ Graph Generator ------------------
elif mode == "Graph Generator":
    st.subheader("Generate 2D Graphs")
    func_input = st.text_input("Enter function in x (e.g., x**2 + 2*x - 3):")
    if st.button("Plot Graph"):
        x = sp.symbols('x')
        func = sp.sympify(func_input)
        x_vals = [i for i in range(-10,11)]
        y_vals = [func.subs(x,i) for i in x_vals]
        plt.plot(x_vals, y_vals)
        plt.xlabel("x")
        plt.ylabel("y")
        plt.title(f"Graph of {func_input}")
        st.pyplot(plt)
