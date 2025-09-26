# LNA (Learning Need Analysis) Test Data Files

This repository contains comprehensive test data files for developing and testing an AI bot that extracts information from Learning Need Analysis reports and determines optimal training delivery methods.

## File Structure

### Main Test Data Files
- `lna_report_2024_q1.csv` - Q1 2024 LNA entries (20 records)
- `lna_report_2024_q2.csv` - Q2 2024 LNA entries (20 records) 
- `lna_report_2024_q3.csv` - Q3 2024 LNA entries (20 records)
- `lna_report_2024_q4_2025_preview.csv` - Q4 2024 + 2025 preview entries (20 records)

### Supporting Files
- `skills_mapping.md` - Comprehensive mapping of competencies to specific skills
- `competency_classification.md` - Classification of competencies as "niche" or "common"
- `business_rules_config.md` - Business logic configuration for the AI bot

## Data Schema

Each CSV file contains the following columns in order:
1. **ID** - Unique identifier for each LNA entry
2. **Submission** - Date when the request was submitted
3. **Priority** - High/Medium/Low priority level
4. **Competency type** - Category of competency (Technical, Leadership, Soft Skills, Compliance)
5. **Job families** - Relevant job families/departments
6. **Targeted competencies** - Specific competency to be developed
7. **Request type** - New Training/Upskilling/Refresher
8. **Targeted audience** - Who will receive the training
9. **Estimated trainees** - Number of people requiring training
10. **Comment** - Additional context and justification
11. **Year** - Training year
12. **Division** - Organizational division
13. **Department** - Specific department
14. **Section** - Team or section within department

## Business Logic for Training Type Recommendation

### Primary Rules
1. **Employee Count Based:**
   - \> 50 trainees → **In-house** training
   - 11-50 trainees → **SDP** (Special Development Program)
   - ≤ 10 trainees → **External** training

2. **Competency Type Override:**
   - **Niche** competencies → **SDP** (regardless of trainee count)
   - **Common** competencies with >50 trainees → **In-house**

### Expected AI Bot Outputs
The AI bot should analyze each LNA entry and provide:
1. **Training Type Recommendation** (In-house/SDP/External)
2. **Priority Level** from the data
3. **Associated Skills** for each competency (from skills_mapping.md)
4. **Competencies Ranked by Demand** (highest to lowest)

## Test Data Coverage

### Training Type Distribution
- **In-house candidates:** Entries with >50 trainees or common competencies with high trainee counts
- **SDP candidates:** Entries with 11-50 trainees or niche competencies
- **External candidates:** Entries with ≤10 trainees and common competencies

### Competency Types Covered
- **Technical:** Cloud computing, AI/ML, cybersecurity, blockchain, etc.
- **Leadership:** Strategic planning, change management, innovation, etc.
- **Soft Skills:** Communication, cultural intelligence, time management, etc.
- **Compliance:** GDPR, safety, AML, environmental regulations, etc.

### Priority Levels
- **High Priority:** Critical business needs, regulatory requirements
- **Medium Priority:** Important capabilities, skill enhancement
- **Low Priority:** General improvement, awareness training

### Trainee Count Scenarios
- **Small groups (1-10):** Specialized, niche skills
- **Medium groups (11-50):** Department-specific training
- **Large groups (51-320):** Company-wide initiatives

## Sample Test Cases

### In-house Training Examples
- LNA004: Communication Skills, 150 trainees (common competency, large group)
- LNA021: Lean Manufacturing, 65 trainees (process improvement, large group)
- LNA041: Cloud Security, 52 trainees (technical competency, large group)

### SDP (Special Development Program) Examples
- LNA003: Advanced Data Analytics, 8 trainees (niche competency)
- LNA010: Blockchain Technology, 4 trainees (niche competency)
- LNA012: IoT & Embedded Systems, 12 trainees (medium group, niche)

### External Training Examples
- LNA005: Financial Risk Assessment, 6 trainees (small group, specialized)
- LNA016: Database Administration, 9 trainees (small group, technical)
- LNA026: Cryptocurrency, 5 trainees (small group, niche but external due to size)

## Usage Instructions

1. **Load the CSV files** into your AI bot testing environment
2. **Reference the skills mapping** to associate competencies with specific skills
3. **Use the competency classification** to determine niche vs. common categorization
4. **Apply the business rules** to generate training type recommendations
5. **Validate outputs** against expected results based on the logic provided

## Data Quality Features

- **Realistic business scenarios** across multiple industries
- **Varied trainee counts** to test all business logic paths  
- **Diverse competency types** covering technical, leadership, and soft skills
- **Temporal progression** showing quarterly training needs evolution
- **Comprehensive skill mappings** for detailed analysis
- **Clear classification rules** for consistent categorization

This test data provides a robust foundation for developing and validating an AI bot that can accurately analyze LNA reports and provide intelligent training delivery recommendations.