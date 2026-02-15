# DDR Report Generation

## Purpose
This project turns a property inspection PDF into a Due Diligence Report (DDR). It extracts the text, pulls the water ingress observations, cleans the data, adds simple reasoning, and then writes a final DDR. Everything is kept in plain Python scripts so a beginner can read and edit the steps.

## What is inside
- `pipeline/` holds the step-by-step scripts for every phase.
- `input/` stores the inspection PDF. A sample file is already there.
- `extracted/` stores text, JSON, and reasoning files that are created after each phase.
- `output/` stores the final DDR text.
- `app.py` is a very simple Streamlit user interface.
- `validation_checklist.txt` explains how to review the final DDR by hand.

## Simple architecture (plain words)
```
PDF report
  |
Phase 1: extract_text.py reads every PDF page with pdfplumber and saves plain text.
  |
Phase 2: extract_observation.py uses the local LLM (llama3.2 on Ollama) to pull 7 impacted areas into JSON.
  |
Phase 3: clean_observations.py cleans the JSON, adds root cause tags, and stores helper lists.
  |
Phase 4: add_reasoning.py adds simple rules for severity and explains each root cause.
  |
Phase 5: generate_ddr.py asks the LLM to write the final DDR and then appends checklist and missing info sections.
  |
Streamlit UI or run_all.py show the results and save the text file.
```

## Prerequisites
1. Python 3.10 or newer.
2. pip (Python package manager).
3. [Ollama](https://ollama.com) installed locally.
4. The `llama3.2` model pulled inside Ollama and the Ollama server running (`ollama serve`).

## Install Python packages
```bash
pip install -r requirements.txt
```
This installs pdfplumber, langchain-ollama, pydantic, and streamlit.

## Running the full pipeline from the terminal
1. Put your inspection PDF inside `input/` and rename it to `Sample Report.pdf` (or edit the paths inside the scripts).
2. Open a terminal at the project folder.
3. Run the entire pipeline:
```bash
python pipeline/run_all.py
```
4. The final DDR will appear at `output/final_ddr.txt`.

### Run each phase by hand (optional)
- `python pipeline/extract_text.py`
- `python pipeline/extract_observation.py`
- `python pipeline/clean_observations.py`
- `python pipeline/add_reasoning.py`
- `python pipeline/generate_ddr.py`

Running them in order gives you the same result as `run_all.py`, and it helps with debugging.

## Using the Streamlit UI
1. Make sure the packages are installed and Ollama is running.
2. Start the app:
```bash
streamlit run app.py
```
3. Open the browser link that Streamlit prints (usually http://localhost:8501).
4. Upload the inspection PDF, click **Generate DDR Report**, and read or download the result inside the page.

## Files produced during a run
- `extracted/report_text.txt`: raw text from every PDF page.
- `extracted/observations_raw.json`: structured observations from the LLM.
- `extracted/observations_clean.json`: cleaned observations with root cause tags.
- `extracted/observations_reasoned.json`: adds severity and reasoning.
- `output/final_ddr.txt`: final Due Diligence Report with all sections.

## Validation checklist
Open `pipeline/validation_checklist.txt` to see how to manually check the DDR. It lists common mistakes (missing sections, wrong area names, etc.) so you can catch issues before sharing the report.

## Troubleshooting tips
- **Ollama errors**: make sure `ollama serve` is running in another terminal and that the `llama3.2` model is downloaded.
- **No PDF text**: confirm the PDF has selectable text. Scanned images need OCR, which this project does not include.
- **Streamlit upload stuck**: check terminal output for Python errors. Fix the issue, restart Streamlit, and try again.
- **Wrong file paths**: every script uses absolute paths that point to this folder. If you move the repo, update the paths at the top of each script.

## Next steps (optional ideas)
- Add OCR for scanned PDFs.
- Store outputs in a database.
- Add tests for the keyword rules in `clean_observations.py` and `add_reasoning.py`.
