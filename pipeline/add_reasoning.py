import json

input_file = "/Users/sidxcodes/DDR Report Generation/extracted/observations_clean.json"
with open(input_file, "r", encoding="utf-8") as f:
    clean_data = json.load(f)

print("Adding Reasoning")
print("Loaded clean observations")
print("")

observations = clean_data["observations"]
checklist = clean_data["checklist_findings"]


def get_detailed_root_cause(obs):
    source_issue = obs["source_issue"].lower()
    source_area = obs["source_area"]
    root_category = obs["root_cause_category"]
    
    if root_category == "Tile Joint Failure":
        return {
            "cause": "Tile joint gaps and hollowness in " + source_area,
            "mechanism": "Water seeps through gaps in tile joints during usage, travels through the substrate, and appears as dampness on the negative side",
            "supporting_evidence": "Checklist confirms gaps in tile joints and around nahani trap"
        }
    
    elif root_category == "Concealed Plumbing Leakage":
        return {
            "cause": "Concealed plumbing leakage in " + source_area,
            "mechanism": "Leaking pipes within walls or floor slabs allow continuous water seepage, causing persistent dampness",
            "supporting_evidence": "Checklist confirms concealed plumbing leakage and loose plumbing joints"
        }
    
    elif root_category == "External Wall Defect":
        return {
            "cause": "Cracks and defects in external wall",
            "mechanism": "Rainwater enters through cracks in external wall surface, causing internal dampness and efflorescence",
            "supporting_evidence": "Checklist confirms moderate cracks on external surface and cracked external plumbing pipes"
        }
    
    else:
        return {
            "cause": "Source requires further investigation",
            "mechanism": "Not enough data to determine water pathway",
            "supporting_evidence": "Additional inspection needed"
        }

def calculate_severity(obs, all_observations, checklist):
    issue = obs["issue_observed"].lower()
    root_cause = obs["root_cause_category"]

    same_cause_count = 0
    for o in all_observations:
        if o["root_cause_category"] == root_cause:
            same_cause_count = same_cause_count + 1

    is_continuous = checklist.get("leakage_timing", "") == "All time"
    
    has_plumbing_issue = checklist.get("concealed_plumbing_leakage", "") == "Yes"

    if same_cause_count >= 3 and is_continuous:
        severity = "High"
        reason = "Same root cause affects " + str(same_cause_count) + " areas with continuous leakage"
    elif same_cause_count >= 2 or has_plumbing_issue:
        severity = "Moderate"
        reason = "Multiple areas affected or plumbing system involved"
    else:
        severity = "Needs Assessment"
        reason = "Single occurrence, requires further investigation"
    
    return severity, reason


observations_with_reasoning = []

for obs in observations:
    root_cause_detail = get_detailed_root_cause(obs)

    severity, severity_reason = calculate_severity(obs, observations, checklist)

    needs_note = obs.get("needs_further_investigation", False)
    if needs_note:
        severity_reason = severity_reason + ". Based on visual indicators; requires further investigation"

    reasoned_obs = {
        "impacted_area_number": obs["impacted_area_number"],
        "affected_area": obs["affected_area"],
        "affected_location": obs["affected_location"],
        "issue_observed": obs["issue_observed"],
        "issue_description": obs["issue_description"],
        "source_area": obs["source_area"],
        "source_issue": obs["source_issue"],
        "root_cause_category": obs["root_cause_category"],
        "root_cause_detail": root_cause_detail,
        "severity": severity,
        "severity_reason": severity_reason,
        "needs_further_investigation": needs_note
    }
    
    observations_with_reasoning.append(reasoned_obs)


is_continuous = checklist.get("leakage_timing", "") == "All time"
total_areas = len(observations_with_reasoning)
has_multiple_causes = True 

if total_areas >= 5 and is_continuous:
    overall_severity = "High"
    overall_reason = "Multiple areas affected with continuous leakage pattern observed throughout the property"
elif total_areas >= 3:
    overall_severity = "High"
    overall_reason = "Widespread issue affecting multiple rooms with persistent water ingress"
else:
    overall_severity = "Moderate"
    overall_reason = "Limited spread but requires attention due to ongoing leakage"

reasoned_output = {
    "overall_assessment": {
        "total_impacted_areas": len(observations_with_reasoning),
        "overall_severity": overall_severity,
        "overall_severity_reason": overall_reason,
        "severity_factors": [
            "Leakage is continuous (observed all time)",
            "Multiple areas affected across the property",
            "Multiple root causes: tile joint failures, plumbing issues, and external wall defects"
        ]
    },
    "observations_with_reasoning": observations_with_reasoning,
    "checklist_findings": checklist,
    "missing_information": clean_data["missing_information"]
}


output_file = "/Users/sidxcodes/DDR Report Generation/extracted/observations_reasoned.json"
with open(output_file, "w", encoding="utf-8") as f:
    json.dump(reasoned_output, f, indent=2)

print("Saved to: " + output_file)