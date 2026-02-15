# pipeline/clean_observations.py
# Phase 4: Deterministic Merge & Cleanup (NO LLM - Pure Python Logic)

import json

# Step 1: Load the raw observations
input_file = "/Users/sidxcodes/DDR Report Generation/extracted/observations_raw.json"
with open(input_file, "r", encoding="utf-8") as f:
    raw_observations = json.load(f)

print("Phase 4: Cleaning Observations")
print("Loaded " + str(len(raw_observations)) + " raw observations")
print("")


# Step 2: Group issues by their root cause type
def get_root_cause_category(positive_issue, source_description):
    text = (positive_issue + " " + source_description).lower()
    
    # Check for multiple causes
    causes = []
    
    if "tile" in text and ("joint" in text or "gap" in text or "hollowness" in text):
        causes.append("Tile Joint Failure")
    if "plumbing" in text or "pipe" in text:
        causes.append("Concealed Plumbing Leakage")
    if "external" in text or "wall crack" in text:
        causes.append("External Wall Defect")
    if "duct" in text:
        causes.append("Duct Issue")
    
    if len(causes) == 0:
        return "Requires Investigation"
    elif len(causes) == 1:
        return causes[0]
    else:
        return " and ".join(causes)


# Step 3: Process each observation
processed_observations = []

for obs in raw_observations:
    negative = obs.get("negative_side", {})
    positive = obs.get("positive_side", {})
    
    # Get root cause category
    root_cause_category = get_root_cause_category(
        positive.get("issue", ""), 
        positive.get("description", "")
    )
    
    # Check if this is Parking Area - needs special note
    needs_investigation_note = False
    area_name = negative.get("area", "")
    if "parking" in area_name.lower():
        needs_investigation_note = True
    
    processed_obs = {
        "impacted_area_number": obs.get("impacted_area_number", 0),
        "affected_area": negative.get("area", "Not Available"),
        "affected_location": negative.get("location", "Not Available"),
        "issue_observed": negative.get("issue", "Not Available"),
        "issue_description": negative.get("description", "Not Available"),
        "source_area": positive.get("area", "Not Available"),
        "source_issue": positive.get("issue", "Not Available"),
        "source_description": positive.get("description", "Not Available"),
        "root_cause_category": root_cause_category,
        "needs_further_investigation": needs_investigation_note
    }
    
    processed_observations.append(processed_obs)


# Step 4: Group by affected area
areas_affected = {}
for obs in processed_observations:
    area = obs["affected_area"]
    if area not in areas_affected:
        areas_affected[area] = []
    areas_affected[area].append(obs)


# Step 5: Group by root cause - collect all unique causes
root_causes = {
    "Tile Joint Failure": [],
    "Concealed Plumbing Leakage": [],
    "External Wall Defect": []
}

for obs in processed_observations:
    cause = obs["root_cause_category"]
    area = obs["affected_area"]
    
    # A single observation can have multiple causes
    if "Tile Joint" in cause:
        if area not in root_causes["Tile Joint Failure"]:
            root_causes["Tile Joint Failure"].append(area)
    if "Plumbing" in cause:
        if area not in root_causes["Concealed Plumbing Leakage"]:
            root_causes["Concealed Plumbing Leakage"].append(area)
    if "External Wall" in cause:
        if area not in root_causes["External Wall Defect"]:
            root_causes["External Wall Defect"].append(area)


# Step 6: Extract checklist findings from the report
checklist_findings = {
    "leakage_timing": "All time",
    "concealed_plumbing_leakage": "Yes",
    "nahani_trap_damage": "Yes",
    "tile_joint_gaps": "Yes",
    "gaps_around_nahani_trap": "Yes",
    "loose_plumbing_joints": "Yes",
    "external_wall_cracks": "Moderate",
    "external_plumbing_pipes_cracked": "Moderate",
    "algae_fungus_on_external_wall": "Moderate",
    "internal_wc_bath_leakage": "Yes"
}


# Step 7: List what info is missing or unclear
missing_info = [
    "Hidden plumbing conditions behind walls not inspected",
    "Structural elements behind wall finishes not visible",
    "No thermal imaging data available",
    "Seasonal variation in leakage not assessed (single inspection)",
    "Exact pipe locations in concealed plumbing not mapped",
    "Water pressure testing not conducted",
    "Terrace waterproofing condition not inspected (relevant for top floor units)",
    "Age and condition of original waterproofing not known"
]


# Step 8: Create the final clean output
clean_output = {
    "summary": {
        "total_impacted_areas": len(processed_observations),
        "total_affected_rooms": len(areas_affected),
        "affected_rooms_list": list(areas_affected.keys()),
        "root_cause_types_found": list(root_causes.keys())
    },
    "observations": processed_observations,
    "observations_by_area": areas_affected,
    "observations_by_root_cause": root_causes,
    "checklist_findings": checklist_findings,
    "missing_information": missing_info
}


# Step 9: Save the clean observations
output_file = "/Users/sidxcodes/DDR Report Generation/extracted/observations_clean.json"
with open(output_file, "w", encoding="utf-8") as f:
    json.dump(clean_output, f, indent=2)

print("Saved to: " + output_file)
print("")
print("-" * 40)
print("CLEANUP SUMMARY")
print("-" * 40)
print("")
print("Total impacted areas: " + str(len(processed_observations)))
print("Affected rooms: " + str(len(areas_affected)))
print("")
print("Rooms affected:")
for area in areas_affected.keys():
    count = len(areas_affected[area])
    print("  - " + area + " (" + str(count) + " issues)")
print("")
print("Root cause types found:")
for cause in root_causes.keys():
    areas = root_causes[cause]
    print("  - " + cause + ": affects " + str(len(areas)) + " areas")
print("")
print("Phase 4 Complete!")
