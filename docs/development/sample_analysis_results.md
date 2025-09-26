# Sample LNA Analysis Results
# Expected outputs from the AI bot for selected test cases

## Test Case 1: LNA004 - Communication & Presentation Skills
**Input Data:**
- ID: LNA004
- Priority: Low
- Competency: Communication & Presentation Skills
- Estimated Trainees: 150
- Competency Type: Common

**Expected AI Bot Output:**
```json
{
  "id": "LNA004",
  "recommendation": {
    "training_type": "In-house",
    "reasoning": "150 trainees exceeds threshold of 50 for in-house training. Common competency supports in-house delivery.",
    "priority_level": "Low",
    "demand_score": 150,
    "competency": "Communication & Presentation Skills",
    "associated_skills": [
      "Public Speaking",
      "Written Communication", 
      "Active Listening",
      "Visual Communication",
      "Storytelling",
      "Audience Analysis",
      "Persuasion Techniques"
    ]
  }
}
```

## Test Case 2: LNA010 - Blockchain Technology
**Input Data:**
- ID: LNA010
- Priority: High
- Competency: Blockchain Technology
- Estimated Trainees: 4
- Competency Type: Niche

**Expected AI Bot Output:**
```json
{
  "id": "LNA010", 
  "recommendation": {
    "training_type": "SDP",
    "reasoning": "Niche competency requires specialized development program regardless of trainee count (4).",
    "priority_level": "High",
    "demand_score": 12,
    "competency": "Blockchain Technology",
    "associated_skills": [
      "Distributed Ledger Technology",
      "Smart Contract Development",
      "Cryptocurrency Fundamentals",
      "Consensus Mechanisms",
      "DeFi Protocol Understanding",
      "Security Auditing",
      "Tokenomics Design"
    ]
  }
}
```

## Test Case 3: LNA005 - Financial Risk Assessment
**Input Data:**
- ID: LNA005
- Priority: High
- Competency: Financial Risk Assessment
- Estimated Trainees: 6
- Competency Type: Common

**Expected AI Bot Output:**
```json
{
  "id": "LNA005",
  "recommendation": {
    "training_type": "External",
    "reasoning": "6 trainees is below threshold of 10 for SDP. Common competency with small group suitable for external training.",
    "priority_level": "High", 
    "demand_score": 18,
    "competency": "Financial Risk Assessment",
    "associated_skills": [
      "Credit Risk Analysis",
      "Market Risk Modeling", 
      "Operational Risk Management",
      "Regulatory Capital",
      "Stress Testing",
      "Portfolio Management",
      "Risk Reporting"
    ]
  }
}
```

## Test Case 4: LNA021 - Lean Manufacturing & Six Sigma
**Input Data:**
- ID: LNA021
- Priority: High
- Competency: Lean Manufacturing & Six Sigma
- Estimated Trainees: 65
- Competency Type: Common

**Expected AI Bot Output:**
```json
{
  "id": "LNA021",
  "recommendation": {
    "training_type": "In-house",
    "reasoning": "65 trainees exceeds threshold of 50 for in-house training. Common competency suitable for internal delivery.",
    "priority_level": "High",
    "demand_score": 195,
    "competency": "Lean Manufacturing & Six Sigma", 
    "associated_skills": [
      "Process Mapping",
      "Statistical Process Control",
      "Root Cause Analysis",
      "Waste Elimination",
      "Continuous Improvement",
      "Quality Tools",
      "Project Management"
    ]
  }
}
```

## Test Case 5: LNA025 - 3D Printing & Additive Manufacturing
**Input Data:**
- ID: LNA025
- Priority: High
- Competency: 3D Printing & Additive Manufacturing
- Estimated Trainees: 7
- Competency Type: Niche

**Expected AI Bot Output:**
```json
{
  "id": "LNA025",
  "recommendation": {
    "training_type": "SDP",
    "reasoning": "Niche competency requires specialized development program. 7 trainees is small but niche classification overrides.",
    "priority_level": "High",
    "demand_score": 21,
    "competency": "3D Printing & Additive Manufacturing",
    "associated_skills": [
      "CAD Design",
      "Material Selection",
      "Printing Technologies", 
      "Post-processing Techniques",
      "Quality Control",
      "Design for Manufacturing",
      "Cost Optimization"
    ]
  }
}
```

## Aggregated Analysis Example
**For all Q1 2024 entries, expected ranked competencies by demand:**

```json
{
  "competencies_ranked_by_demand": [
    {
      "rank": 1,
      "competency": "Communication & Presentation Skills",
      "total_trainees": 150,
      "demand_score": 150,
      "training_type": "In-house"
    },
    {
      "rank": 2, 
      "competency": "Cloud Computing & DevOps",
      "total_trainees": 45,
      "demand_score": 135,
      "training_type": "SDP"
    },
    {
      "rank": 3,
      "competency": "Machine Learning & AI", 
      "total_trainees": 35,
      "demand_score": 70,
      "training_type": "SDP"
    },
    {
      "rank": 4,
      "competency": "Cybersecurity & Information Security",
      "total_trainees": 25, 
      "demand_score": 50,
      "training_type": "SDP"
    },
    {
      "rank": 5,
      "competency": "Change Management",
      "total_trainees": 18,
      "demand_score": 54,
      "training_type": "SDP"
    }
  ]
}
```

## Validation Criteria

### Training Type Accuracy
- All entries with >50 trainees should be "In-house" (unless overridden by niche classification)
- All niche competencies should be "SDP" regardless of trainee count
- All entries with ≤10 trainees and common competencies should be "External"

### Skills Mapping Accuracy  
- Each competency should return the correct associated skills from the skills_mapping.md file
- Skills should be comprehensive and relevant to the competency

### Demand Ranking Accuracy
- Should consider priority level, trainee count, and urgency
- Higher priority items should generally rank higher
- Larger trainee counts should contribute to higher demand scores

This sample analysis provides clear expectations for validating the AI bot's performance against the test data.