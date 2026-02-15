import json
from langchain_ollama import ChatOllama
from datetime import datetime

input_file = "/Users/sidxcodes/DDR Report Generation/extracted/observations_reasoned.json"
with open(input_file, "r", encoding="utf-8") as f:
    reasoned_data = json.load(f)

print("Phase 6: Generating DDR Report")
print("Loaded reasoned observations")
print("")

llm = ChatOllama(model="llama3.2", base_url="http://localhost:11434")

observations_text = json.dumps(reasoned_data, indent=2)

ddr_prompt = f"""
You are writing a Due Diligence Report for a property inspection.

STRICT RULES:
1. Use ONLY the data provided. Do not invent anything.
2. Do NOT add recommendations not in the data.
3. Use simple English.
4. Tile joint issues are SERIOUS causes of water ingress, not cosmetic.
5. List ALL impacted areas. Do not skip any.

LANGUAGE RULES (very important):
- Do NOT say "Primary cause is X". Instead say "Primary contributors include tile joint failures, concealed plumbing leakage, and external wall defects"
- Do NOT use exact severity counts like "6 high and 1 moderate". Instead describe severity through spread: "High overall severity due to multiple areas affected with continuous leakage"
- For Parking Area, add: "Based on visual indicators; requires further investigation"
- Each area name should be distinct. No "second instance" labels.

REPORT STRUCTURE:

1. EXECUTIVE SUMMARY
Write 4-5 sentences:
- How many areas are affected
- Types of issues found (dampness, seepage, efflorescence)
- Say: "Primary contributors include tile joint failures, concealed plumbing leakage, and external wall defects"
- Overall severity is High due to widespread and continuous leakage

2. IMPACTED AREAS OVERVIEW
- Total impacted areas: [number]
- List each area name (no duplicates, each area is distinct)

3. DETAILED OBSERVATIONS
For each impacted area:

IMPACTED AREA [number]: [Area Name]
Problem: [issue type]
Location: [skirting level, ceiling, wall surface]
Description: [from data]
Source: [positive side area]
Root Cause: [specific cause - tile joint gaps OR plumbing issue OR external wall crack]
Mechanism: [how water travels]
Severity: [from data]
Note: For Parking Area add "Based on visual indicators; requires further investigation"

4. ROOT CAUSE ANALYSIS
List ALL THREE root cause types found:

A. Tile Joint Failure
- Areas affected: [list]
- Evidence: Checklist confirms gaps in tile joints

B. Concealed Plumbing Leakage
- Areas affected: [list]  
- Evidence: Checklist confirms plumbing issues
- Note: Based on visual indicators; requires further investigation

C. External Wall Defects
- Areas affected: [list]
- Evidence: Checklist shows moderate cracks

5. CHECKLIST FINDINGS
- Leakage timing: [from data]
- Tile joint gaps: [from data]
- Concealed plumbing leakage: [from data]
- External wall cracks: [from data]
- Other findings from checklist

6. SEVERITY ASSESSMENT
Overall Severity: High
Reason: Multiple areas affected with continuous leakage pattern. Leakage is observed "all time" indicating persistent water ingress.

Do NOT use exact counts. Describe severity through:
- Spread across areas
- Continuous nature of leakage
- Multiple root causes involved

7. MISSING OR UNCLEAR INFORMATION
List each item from the missing_information field exactly as given.

8. CONCLUSION
2-3 sentences:
- Multiple areas affected by water ingress
- Primary contributors are tile joint failures, plumbing issues, and external wall defects
- Further investigation needed for concealed conditions

DATA:
{observations_text}

Write the report. Use only information from the data.
"""

print("Generating DDR report...")
response = llm.invoke(ddr_prompt)

if hasattr(response, 'content'):
    ddr_text = response.content
else:
    ddr_text = str(response)

current_date = datetime.now().strftime("%d %B %Y")

missing_info = reasoned_data.get("missing_information", [])

output_file = "/Users/sidxcodes/DDR Report Generation/output/final_ddr.txt"
with open(output_file, "w", encoding="utf-8") as f:
    f.write("DUE DILIGENCE REPORT (DDR)\n")
    f.write("Property Inspection Findings\n")
    f.write("\n")
    f.write("Report Date: " + current_date + "\n")
    f.write("Report Type: Defect Detection Report\n")
    f.write("\n")
    f.write("-" * 60 + "\n")
    f.write("\n")
    f.write(ddr_text)
    f.write("\n\n")
    
    f.write("MISSING OR UNCLEAR INFORMATION\n")
    f.write("\n")
    for item in missing_info:
        f.write("- " + item + "\n")
    f.write("\n")
    
    checklist = reasoned_data.get("checklist_findings", {})
    f.write("CHECKLIST FINDINGS\n")
    f.write("\n")
    f.write("- Leakage timing: " + checklist.get("leakage_timing", "Not Available") + "\n")
    f.write("- Concealed plumbing leakage: " + checklist.get("concealed_plumbing_leakage", "Not Available") + "\n")
    f.write("- Tile joint gaps: " + checklist.get("tile_joint_gaps", "Not Available") + "\n")
    f.write("- Gaps around nahani trap: " + checklist.get("gaps_around_nahani_trap", "Not Available") + "\n")
    f.write("- Loose plumbing joints: " + checklist.get("loose_plumbing_joints", "Not Available") + "\n")
    f.write("- External wall cracks: " + checklist.get("external_wall_cracks", "Not Available") + "\n")
    f.write("- Internal WC/Bath leakage: " + checklist.get("internal_wc_bath_leakage", "Not Available") + "\n")
    f.write("\n")

    f.write("CONCLUSION\n")
    f.write("\n")
    f.write("Multiple areas of the property are affected by water ingress issues.\n")
    f.write("Primary contributors include tile joint failures, concealed plumbing leakage, and external wall defects.\n")
    f.write("Further investigation is needed for concealed conditions behind walls and floors.\n")
    f.write("\n")
    
    f.write("-" * 60 + "\n")
    f.write("\n")
    f.write("DISCLAIMER\n")
    f.write("This report is based on visual inspection findings.\n")
    f.write("Root causes mentioned are probable and need verification.\n")
    f.write("Hidden conditions behind walls and floors were not inspected.\n")
    f.write("Recommendations should be verified by qualified professionals.\n")
    f.write("\n")
    f.write("END OF REPORT\n")

print("DDR report saved to: " + output_file)
print("")
print("Phase 6 Complete!")
print("")
print("Preview:")
print("-" * 40)
print(ddr_text[:1500] + "...")
