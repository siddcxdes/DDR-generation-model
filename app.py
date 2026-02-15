import streamlit as st
import subprocess
import sys
import os

st.set_page_config(page_title="DDR Report Generator", layout="wide")

st.title("DDR Report Generator")
st.write("Upload a property inspection PDF to generate a Due Diligence Report")

uploaded_file = st.file_uploader("Upload PDF", type=["pdf"])

if uploaded_file is not None:
    input_path = "/Users/sidxcodes/DDR Report Generation/input/Sample Report.pdf"
    with open(input_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    st.success("File uploaded: " + uploaded_file.name)

if st.button("Generate DDR Report"):
    
    if uploaded_file is None:
        st.error("Please upload a PDF file first")
    else:
        progress = st.progress(0)
        status = st.empty()
        
        # Phase 1
        status.text("Running Phase 1: Extracting text from PDF...")
        progress.progress(10)
        result = subprocess.run(
            [sys.executable, "/Users/sidxcodes/DDR Report Generation/pipeline/extract_text.py"],
            capture_output=True,
            text=True
        )
        if result.returncode != 0:
            st.error("Phase 1 failed: " + result.stderr)
            st.stop()
        
        # Phase 3
        status.text("Running Phase 3: Extracting observations using LLM...")
        progress.progress(30)
        result = subprocess.run(
            [sys.executable, "/Users/sidxcodes/DDR Report Generation/pipeline/extract_observation.py"],
            capture_output=True,
            text=True
        )
        if result.returncode != 0:
            st.error("Phase 3 failed: " + result.stderr)
            st.stop()
        
        # Phase 4
        status.text("Running Phase 4: Cleaning and merging observations...")
        progress.progress(50)
        result = subprocess.run(
            [sys.executable, "/Users/sidxcodes/DDR Report Generation/pipeline/clean_observations.py"],
            capture_output=True,
            text=True
        )
        if result.returncode != 0:
            st.error("Phase 4 failed: " + result.stderr)
            st.stop()
        
        # Phase 5
        status.text("Running Phase 5: Adding reasoning and severity...")
        progress.progress(70)
        result = subprocess.run(
            [sys.executable, "/Users/sidxcodes/DDR Report Generation/pipeline/add_reasoning.py"],
            capture_output=True,
            text=True
        )
        if result.returncode != 0:
            st.error("Phase 5 failed: " + result.stderr)
            st.stop()
        
        # Phase 6
        status.text("Running Phase 6: Generating DDR report...")
        progress.progress(90)
        result = subprocess.run(
            [sys.executable, "/Users/sidxcodes/DDR Report Generation/pipeline/generate_ddr.py"],
            capture_output=True,
            text=True
        )
        if result.returncode != 0:
            st.error("Phase 6 failed: " + result.stderr)
            st.stop()
        
        progress.progress(100)
        status.text("Done!")
        
        st.success("DDR Report generated successfully")

# Show the report if it exists
output_path = "/Users/sidxcodes/DDR Report Generation/output/final_ddr.txt"
if os.path.exists(output_path):
    st.subheader("Generated Report")
    
    with open(output_path, "r") as f:
        report_text = f.read()
    
    st.text_area("DDR Report", report_text, height=500)
    
    st.download_button(
        label="Download Report",
        data=report_text,
        file_name="final_ddr.txt",
        mime="text/plain"
    )
