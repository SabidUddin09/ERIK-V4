import streamlit as st
from googlesearch import search
import requests
from bs4 import BeautifulSoup
import fitz  # PyMuPDF
import docx
import sympy as sp
import matplotlib.pyplot as plt
import numpy as np
from textwrap import shorten
import plotly.graph_objects as go
from io import BytesIO
from PyPDF2 import PdfReader

# ------------------ ERIK v4.4 ------------------
st.set_page_config(page_title="ERIK v4.4 - Advanced Academic AI", layout="wide")
st.title("🧠 ERIK v4.4 - Exceptional Resources & Intelligence Kernel (AI Academic Assistant)")

# ------------------ Sidebar ------------------
st.sidebar.header("Features")
mode = st.sidebar.radio("Choose a feature:", [
    "Ask Question (AI-style)", 
    "Math Solver", 
    "Quiz Generator", 
    "PDF/Text Analyzer", 
    "Graph Generator",
    "3D Diagram Generator",
    "Google Scholar Paper Search & Summary"
])

# ------------------ Ask Question (AI-style) ------------------
if mode == "Ask Question (AI-style)":
    query = st.text_input("Ask anything:")
    if st.button("Search & Answer"):
        st.info("Searching Google & generating concise answer...")
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
                for p in paragraphs[:2]:
                    answer += p.get_text() + " "
            except:
                continue
        if answer:
            concise = shorten(answer, width=600, placeholder="...")
            st.markdown("**AI-style Answer (Concise Summary):**")
            st.write(concise)
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
            reader = PdfReader(uploaded_file)
            for page in reader.pages:
                text += page.extract_text() + "\n"
        elif uploaded_file.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
            doc = docx.Document(uploaded_file)
            for para in doc.paragraphs:
                text += para.text + "\n"
        else:
            text = str(uploaded_file.read(), "utf-8")
        st.text_area("Extracted Text", text, height=300)

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

# ------------------ 3D Diagram Generator ------------------
elif mode == "3D Diagram Generator":
    st.subheader("Interactive 3D Surface Plot")
    func_input = st.text_input("Enter function in x and y (e.g., x**2 + y**2):")
    if st.button("Plot 3D Diagram"):
        x = sp.symbols('x')
        y = sp.symbols('y')
        func = sp.sympify(func_input)
        X = np.linspace(-10, 10, 50)
        Y = np.linspace(-10, 10, 50)
        X, Y = np.meshgrid(X, Y)
        Z = np.array([[func.subs({x: xi, y: yi}) for xi, yi in zip(X_row, Y_row)] for X_row, Y_row in zip(X, Y)])
        fig = go.Figure(data=[go.Surface(z=Z, x=X, y=Y)])
        fig.update_layout(scene=dict(zaxis_title='Z', xaxis_title='X', yaxis_title='Y'))
        st.plotly_chart(fig)

# ------------------ Google Scholar Paper Search & Summary ------------------
elif mode == "Google Scholar Paper Search & Summary":
    st.subheader("Search, Download (if open-access) & Summarize Research Papers")
    topic = st.text_input("Enter research topic or keywords:")
    if st.button("Search Papers"):
        query = f"{topic} site:scholar.google.com"
        papers = []
        try:
            for url in search(query, num_results=5):
                papers.append(url)
        except:
            st.error("Error searching Google Scholar.")

        if papers:
            st.write("Top Research Papers:")
            for p in papers:
                st.write(f"- {p}")
                try:
                    r = requests.get(p, timeout=5)
                    soup = BeautifulSoup(r.text, 'html.parser')
                    abstract = ""
                    paragraphs = soup.find_all('p')
                    for par in paragraphs[:5]:
                        abstract += par.get_text() + " "
                    st.write("**Summary:**")
                    st.write(shorten(abstract, width=400, placeholder="..."))

                    # Optional: Attempt PDF download
                    pdf_link = soup.find('a', href=True, text=lambda t: t and 'PDF' in t)
                    if pdf_link:
                        pdf_url = pdf_link['href']
                        st.write(f"[Download PDF]({pdf_url})")
                except:
                    st.write("Summary/PDF not available.")
        else:
            st.warning("No papers found.")
