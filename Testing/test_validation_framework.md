# LNA AI Bot Test Validation Framework

This document provides a comprehensive testing framework to validate the AI bot's performance against expected outcomes for Learning Need Analysis (LNA) report processing.

## Test Structure Overview

The testing framework is organized into the following structure:

```
Testing/
├── TestData/                    # CSV files with LNA report data
├── ExpectedResults/             # JSON files with expected outcomes
├── Configuration/               # Business rules and mappings
└── Documentation/               # Test documentation and guides
```

## Validation Categories

### 1. Business Logic Validation

#### Training Type Decision Accuracy
**Primary Rules:**
- **> 50 trainees** → **In-house** (unless overridden by niche classification)
- **11-50 trainees** → **SDP** (Special Development Program)
- **≤ 10 trainees** → **External**

**Override Rules:**
- **Niche competencies** → **SDP** (regardless of trainee count)
- **Exception:** If niche competency has >50 trainees, it becomes **In-house**

#### Test Case Examples:
```json
{
  "rule": "Large group, common competency",
  "example": "LNA004 - Communication Skills (150 trainees) → In-house",
  "validation": "training_type === 'In-house'"
}
```

### 2. Competency Classification Validation

#### Skills Mapping Accuracy
Each competency must return the correct associated skills from the skills mapping configuration.

**Test Method:**
```javascript
function validateSkills(competency, returnedSkills, expectedSkills) {
  return expectedSkills.every(skill => returnedSkills.includes(skill));
}
```

#### Niche vs Common Classification
**Niche Examples:**
- Quantum Computing Fundamentals
- Blockchain Technology
- Artificial Intelligence Ethics
- Advanced Data Analytics
- Machine Learning & AI

**Common Examples:**
- Communication & Presentation Skills
- Strategic Planning & Decision Making
- Project Management Certification
- Data Privacy & GDPR
- Time Management & Productivity

### 3. Demand Score Calculation Validation

#### Formula:
```
demand_score = priority_weight × trainee_count
where:
- High Priority = 3 points
- Medium Priority = 2 points
- Low Priority = 1 point
```

#### Test Cases:
```json
{
  "LNA001": {
    "priority": "High",
    "trainees": 45,
    "expected_demand_score": 135
  },
  "LNA002": {
    "priority": "Medium", 
    "trainees": 12,
    "expected_demand_score": 24
  }
}
```

### 4. Ranking Validation

#### Competencies by Demand
The AI bot should rank competencies from highest to lowest demand score.

**Expected Top 5 Across All Datasets:**
1. Effective Communication in Digital Age (310 demand score)
2. Workplace Safety & Health (320 demand score) 
3. Updated Privacy Regulations (285 demand score)
4. Data Privacy & GDPR (280 demand score)
5. Diversity & Inclusion Awareness (275 demand score)

## Test Execution Framework

### 1. Individual Record Validation

For each LNA entry, validate:
- **Training Type Recommendation** matches expected outcome
- **Priority Level** is correctly extracted
- **Associated Skills** are complete and accurate
- **Demand Score** calculation is correct
- **Competency Classification** (niche/common) is accurate

### 2. Dataset Summary Validation

For each quarterly dataset, validate:
- **Training Type Distribution** matches expected counts
- **Priority Distribution** is correctly summarized
- **Total Trainees** sum is accurate
- **Average Trainees** calculation is correct
- **Top 5 Rankings** by demand score are accurate

### 3. Cross-Dataset Consistency

Validate that:
- Same competencies receive same classification across datasets
- Skills mapping is consistent for identical competencies
- Business logic is applied uniformly

## Automated Test Cases

### Test Case 1: Training Type Logic
```json
{
  "test_name": "training_type_logic",
  "test_cases": [
    {
      "input": {"trainees": 150, "competency_type": "common"},
      "expected_output": "In-house",
      "reasoning": "150 > 50, common competency"
    },
    {
      "input": {"trainees": 4, "competency_type": "niche"},
      "expected_output": "SDP", 
      "reasoning": "Niche competency overrides trainee count"
    },
    {
      "input": {"trainees": 6, "competency_type": "common"},
      "expected_output": "External",
      "reasoning": "6 ≤ 10, common competency"
    }
  ]
}
```

### Test Case 2: Skills Mapping
```json
{
  "test_name": "skills_mapping_accuracy",
  "test_cases": [
    {
      "competency": "Cloud Computing & DevOps",
      "expected_skills": [
        "AWS/Azure/GCP Platform Management",
        "Container Orchestration (Docker, Kubernetes)",
        "Infrastructure as Code (Terraform, CloudFormation)",
        "CI/CD Pipeline Design",
        "Monitoring and Logging",
        "Auto-scaling and Load Balancing",
        "Cloud Security Best Practices"
      ]
    }
  ]
}
```

### Test Case 3: Demand Score Calculation
```json
{
  "test_name": "demand_score_calculation", 
  "test_cases": [
    {
      "priority": "High",
      "trainees": 45,
      "expected_score": 135,
      "calculation": "3 × 45 = 135"
    },
    {
      "priority": "Medium",
      "trainees": 12, 
      "expected_score": 24,
      "calculation": "2 × 12 = 24"
    },
    {
      "priority": "Low",
      "trainees": 150,
      "expected_score": 150,
      "calculation": "1 × 150 = 150"
    }
  ]
}
```

## Performance Benchmarks

### Accuracy Targets
- **Training Type Accuracy**: 100% (all cases must be correct)
- **Skills Mapping Accuracy**: 100% (all skills must be present)
- **Demand Score Accuracy**: 100% (calculations must be exact)
- **Ranking Accuracy**: 95% (minor variations acceptable for ties)

### Response Time Targets
- **Single Record Processing**: < 2 seconds
- **Full Dataset Processing**: < 30 seconds
- **Skills Lookup**: < 1 second

## Error Handling Tests

### Invalid Data Tests
- Missing required fields
- Invalid priority levels
- Negative trainee counts
- Unknown competency types

### Edge Cases
- Exact threshold values (10, 50 trainees)
- Tied demand scores
- Empty skills mappings
- Future dates in submissions

## Regression Testing

### Dataset Updates
When adding new test data:
1. Verify new competencies are classified (niche/common)
2. Add skills mappings for new competencies
3. Update expected results files
4. Run full validation suite

### Business Rule Changes
When modifying business logic:
1. Update configuration files
2. Regenerate all expected results
3. Update validation framework
4. Re-run all test cases

## Test Reporting

### Success Criteria
- All individual record validations pass
- All summary statistics match expected values
- All ranking validations pass
- No critical errors in error handling tests

### Failure Analysis
- Categorize failures by type (logic, mapping, calculation)
- Identify patterns in failures
- Provide detailed error descriptions
- Suggest corrective actions

This comprehensive validation framework ensures the AI bot performs accurately and consistently across all test scenarios.