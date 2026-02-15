
import json
from langchain_ollama import ChatOllama
from pydantic import BaseModel
from typing import List

class Observation(BaseModel):
    impacted_area_number: int
    negative_side_area: str
    negative_side_location: str
    negative_side_issue: str
    negative_side_description: str
    positive_side_area: str
    positive_side_issue: str
    positive_side_description: str


class ObservationList(BaseModel):
    observations: List[Observation]

input_file = "/Users/sidxcodes/DDR Report Generation/extracted/report_text.txt"
with open(input_file, "r", encoding="utf-8") as f:
    extracted_text = f.read()


llm = ChatOllama(model="llama3.2", base_url="http://localhost:11434")
structured_llm = llm.with_structured_output(ObservationList)

extraction_prompt = f"""
You are extracting data from a property inspection report. Extract ALL 7 impacted areas.

For each impacted area, extract:
- impacted_area_number: The area number (1 to 7)
- negative_side_area: The affected area name. Use these exact names:
  - "Hall" for Hall
  - "Bedroom" for Common Bedroom  
  - "Master Bedroom" for Master Bedroom skirting issues
  - "Kitchen" for Kitchen
  - "Master Bedroom-2" for Master Bedroom wall/efflorescence issues (this is a different location)
  - "Parking Area" for Parking Area
  - "Common Bathroom" for Common Bathroom ceiling
- negative_side_location: Where in the area (skirting level, ceiling, wall surface)
- negative_side_issue: The problem (Dampness, Seepage, Efflorescence)
- negative_side_description: Full description of the problem from the report
- positive_side_area: The source area causing the issue
- positive_side_issue: The cause - be specific:
  - "tile joint gaps" for tile joint issues
  - "tile hollowness" for hollow tiles
  - "plumbing issue" for plumbing problems
  - "external wall crack" for external wall issues
  - "duct issue" for duct problems
- positive_side_description: Full description of the cause

IMPORTANT: There are exactly 7 impacted areas. Extract all of them with accurate descriptions.

Summary table from the report:
1. Hall skirting dampness - caused by Common Bathroom tile joint gaps
2. Common Bedroom skirting dampness - caused by Common Bathroom tile joint gaps  
3. Master Bedroom skirting dampness - caused by Master Bedroom Bathroom tile joint gaps
4. Kitchen skirting dampness - caused by Master Bedroom Bathroom tile joint gaps
5. Master Bedroom wall dampness and efflorescence - caused by External wall cracks and duct issue
6. Parking Area ceiling seepage - caused by Common Bathroom plumbing issue and tile joint gaps
7. Common Bathroom ceiling dampness - caused by tile joint gaps in Flat No. 203 bathrooms

INSPECTION REPORT:
{extracted_text}
"""

print("Extracting observations from report...")
response = structured_llm.invoke(extraction_prompt)

observations_list = []
for obs in response.observations:
    observations_list.append({
        "impacted_area_number": obs.impacted_area_number,
        "negative_side": {
            "area": obs.negative_side_area,
            "location": obs.negative_side_location,
            "issue": obs.negative_side_issue,
            "description": obs.negative_side_description
        },
        "positive_side": {
            "area": obs.positive_side_area,
            "issue": obs.positive_side_issue,
            "description": obs.positive_side_description
        }
    })

output_file = "/Users/sidxcodes/DDR Report Generation/extracted/observations_raw.json"
with open(output_file, "w", encoding="utf-8") as f:
    json.dump(observations_list, f, indent=2)

print("Extracted " + str(len(observations_list)) + " observations")
print("Saved to " + output_file)