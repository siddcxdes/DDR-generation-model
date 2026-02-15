import subprocess
import sys

print("DDR REPORT GENERATION PIPELINE")
print("=" * 60)
print("")

phases = [
    {
        "name": "Text Extraction",
        "script": "/Users/sidxcodes/DDR Report Generation/pipeline/extract_text.py"
    },
    {
        "name": "Structured Extraction (LLM)",
        "script": "/Users/sidxcodes/DDR Report Generation/pipeline/extract_observation.py"
    },
    {
        "name": "Merge and Cleanup",
        "script": "/Users/sidxcodes/DDR Report Generation/pipeline/clean_observations.py"
    },
    {
        "name": "Reasoning Layer",
        "script": "/Users/sidxcodes/DDR Report Generation/pipeline/add_reasoning.py"
    },
    {
        "name": "DDR Generation (LLM)",
        "script": "/Users/sidxcodes/DDR Report Generation/pipeline/generate_ddr.py"
    }
]

for phase in phases:
    print("")
    print(phase["name"])
    print("-" * 60)
    print("")
    
    result = subprocess.run(
        [sys.executable, phase["script"]],
        capture_output=False
    )
    
    if result.returncode != 0:
        print("")
        print("ERROR: " + phase["name"] + " failed!")
        print("Stopping pipeline.")
        sys.exit(1)
    
    print("")

print("")
print("PIPELINE COMPLETE!")
print("=" * 60)
print("")
print("Output files:")
print("  - extracted/report_text.txt (raw text from PDF)")
print("  - extracted/observations_raw.json (LLM extracted observations)")
print("  - extracted/observations_clean.json (merged and cleaned)")
print("  - extracted/observations_reasoned.json (with root causes and severity)")
print("  - output/final_ddr.txt (final DDR report)")

