# LNA Bot Test Datasets Documentation

This document provides comprehensive information about the test datasets created for the LNA Bot project. Each dataset is designed to test specific aspects of the system and provides realistic scenarios for development and validation.

## Dataset Overview

| Dataset | Records | Purpose | Key Features |
|---------|---------|---------|--------------|
| **Original Datasets** |
| lna_report_2024_q1.csv | 20 | Baseline mixed scenarios | Standard quarterly training requests |
| lna_report_2024_q2.csv | 20 | Continuation scenarios | Follow-up training initiatives |
| lna_report_2024_q3.csv | 20 | Advanced scenarios | Complex competency requirements |
| lna_report_2024_q4_2025_preview.csv | 20 | Future planning | Emerging technology trends |
| **New Comprehensive Datasets** |
| lna_report_specialized_competencies.csv | 20 | Niche competencies | Highly specialized, low-volume training |
| lna_report_medium_scale_training.csv | 20 | Mid-scale programs | 11-50 participants, mixed competencies |
| lna_report_large_scale_training.csv | 20 | Enterprise-wide programs | 50+ participants, company-wide initiatives |
| lna_report_emerging_technologies.csv | 20 | Cutting-edge tech | Bleeding-edge, experimental technologies |
| lna_report_edge_cases_errors.csv | 20 | Error handling | Invalid data, edge cases, error scenarios |
| lna_report_pharmaceutical_industry.csv | 20 | Industry-specific | Pharmaceutical & biotech specializations |
| lna_report_fintech_banking.csv | 20 | Financial services | Banking, fintech, and financial technologies |
| lna_report_green_technology.csv | 20 | Sustainability focus | Environmental and green technology training |

## Detailed Dataset Descriptions

### 1. lna_report_specialized_competencies.csv
**Purpose**: Test the system's handling of highly specialized, niche competencies with very small participant counts.

**Key Characteristics**:
- **Participant Range**: 1-8 people (External training scenarios)
- **Competency Types**: Highly specialized technical skills
- **Priority Distribution**: Mix of High/Medium priorities
- **Industries**: Healthcare, Research, Advanced Technology

**Examples**:
- Advanced Clinical Research (3 participants)
- Specialized Surgery Techniques (2 participants)
- Quantum Computing Fundamentals (4 participants)
- Nuclear Medicine (5 participants)

**Testing Focus**:
- External training recommendations
- Niche competency classification
- Small group cost-effectiveness
- Specialized skill requirements

### 2. lna_report_medium_scale_training.csv
**Purpose**: Test the Sweet Spot for Special Development Program (SDP) recommendations.

**Key Characteristics**:
- **Participant Range**: 11-52 people (SDP target range)
- **Competency Types**: Mix of technical, leadership, and soft skills
- **Request Types**: Balanced mix of new training, upskilling, and certification
- **Industries**: Manufacturing, IT, Finance, HR

**Examples**:
- Lean Manufacturing & Six Sigma (45 participants)
- Project Management Certification (38 participants)
- Cloud Computing & DevOps (52 participants)
- Cybersecurity Certification (31 participants)

**Testing Focus**:
- SDP recommendation logic
- Medium-scale training efficiency
- Cost-benefit analysis for mid-size groups
- Professional certification programs

### 3. lna_report_large_scale_training.csv
**Purpose**: Test in-house training recommendations for enterprise-wide programs.

**Key Characteristics**:
- **Participant Range**: 50+ people (In-house training threshold)
- **Competency Types**: Common skills applicable to large groups
- **Request Types**: Mandatory, company-wide initiatives
- **Scope**: Enterprise-wide, department-wide, all-staff programs

**Examples**:
- Communication & Presentation Skills (1,250 participants)
- Data Privacy & GDPR (890 participants)
- Workplace Safety & Health (1,150 participants)
- Cybersecurity Awareness (1,180 participants)

**Testing Focus**:
- In-house training recommendations
- Large-scale program logistics
- Mandatory training compliance
- Cost efficiency for large groups

### 4. lna_report_emerging_technologies.csv
**Purpose**: Test the system with cutting-edge, experimental technologies that may not have established classifications.

**Key Characteristics**:
- **Participant Range**: 1-6 people (Ultra-specialized)
- **Competency Types**: Bleeding-edge technologies
- **Priority**: High priority due to competitive advantage
- **Innovation Level**: Experimental, research-focused

**Examples**:
- 3D Printing & Additive Manufacturing
- Virtual Reality Development
- Neuromorphic Computing
- Fusion Energy Technology
- Photonic Computing Systems

**Testing Focus**:
- New technology classification
- Research and development training
- Innovation capability building
- Future-proofing skill development

### 5. lna_report_edge_cases_errors.csv
**Purpose**: Test error handling, data validation, and system robustness with intentionally problematic data.

**Key Characteristics**:
- **Data Quality**: Invalid, incomplete, or nonsensical data
- **Error Types**: Missing fields, negative values, impossible scenarios
- **Edge Cases**: Boundary conditions, extreme values
- **Invalid Combinations**: Mismatched competency-audience pairs

**Examples**:
- Legacy System Modernization (0 participants) - No developers available
- Strategic Planning (500 executives) - Unrealistic count
- Brain Surgery for Nurses - Skill mismatch
- Time Travel Programming - Fictional technology

**Testing Focus**:
- Data validation robustness
- Error message clarity
- Graceful failure handling
- Edge case boundary testing

### 6. lna_report_pharmaceutical_industry.csv
**Purpose**: Test industry-specific competencies and regulatory requirements in pharmaceutical sector.

**Key Characteristics**:
- **Industry Focus**: Pharmaceutical, biotech, medical devices
- **Regulatory Requirements**: FDA, GMP, ICH guidelines
- **Specialization Level**: High technical complexity
- **Compliance Focus**: Quality, safety, regulatory affairs

**Examples**:
- Clinical Research Methodology
- Pharmaceutical Manufacturing (GMP)
- Pharmacovigilance & Drug Safety
- Cell & Gene Therapy Manufacturing

**Testing Focus**:
- Industry-specific competency classification
- Regulatory compliance training
- Technical specialization requirements
- Quality system training needs

### 7. lna_report_fintech_banking.csv
**Purpose**: Test financial services and technology competencies with regulatory and innovation focus.

**Key Characteristics**:
- **Industry Focus**: Banking, fintech, financial services
- **Technology Integration**: Digital transformation, blockchain, AI
- **Regulatory Environment**: Basel III, PSD2, AML/KYC
- **Innovation Level**: High-tech financial solutions

**Examples**:
- Sustainable Finance & ESG Investing
- Cryptocurrency & Digital Assets
- Decentralized Finance (DeFi) Protocols
- Central Bank Digital Currency (CBDC)

**Testing Focus**:
- Financial technology competencies
- Regulatory compliance in finance
- Innovation in financial services
- Digital transformation training

### 8. lna_report_green_technology.csv
**Purpose**: Test environmental and sustainability-focused competencies across various green technology sectors.

**Key Characteristics**:
- **Sustainability Focus**: Environmental protection, clean energy
- **Technology Areas**: Renewable energy, waste management, water treatment
- **Industry Range**: Energy, manufacturing, engineering
- **Impact Level**: Environmental and social benefits

**Examples**:
- Renewable Energy Systems
- Carbon Capture & Storage
- Hydrogen Fuel Technology
- Circular Economy & Resource Recovery

**Testing Focus**:
- Environmental competency classification
- Sustainability training requirements
- Green technology specializations
- Corporate social responsibility training

## Testing Scenarios by Dataset

### Business Rules Testing

**External Training (≤10 participants)**:
- Primary Dataset: `lna_report_specialized_competencies.csv`
- Secondary: `lna_report_emerging_technologies.csv`

**SDP Training (11-50 participants)**:
- Primary Dataset: `lna_report_medium_scale_training.csv`
- Secondary: `lna_report_pharmaceutical_industry.csv`, `lna_report_fintech_banking.csv`

**In-house Training (>50 participants)**:
- Primary Dataset: `lna_report_large_scale_training.csv`

### Error Handling Testing

**Data Validation**:
- Primary Dataset: `lna_report_edge_cases_errors.csv`
- Tests: Missing fields, invalid values, boundary conditions

**System Robustness**:
- Mixed datasets with intentional data quality issues
- Tests: Graceful degradation, error recovery

### Industry-Specific Testing

**Healthcare & Life Sciences**:
- Datasets: `lna_report_pharmaceutical_industry.csv`, `lna_report_specialized_competencies.csv`

**Financial Services**:
- Dataset: `lna_report_fintech_banking.csv`

**Technology & Innovation**:
- Dataset: `lna_report_emerging_technologies.csv`

**Environmental & Sustainability**:
- Dataset: `lna_report_green_technology.csv`

## Data Quality Metrics

### Valid Records Distribution
- **High Quality**: ~85% of records across all datasets
- **Edge Cases**: ~10% intentionally problematic (edge_cases_errors.csv)
- **Industry Specific**: ~5% highly specialized scenarios

### Competency Classification Coverage
- **Niche Competencies**: 40% of total competencies
- **Common Competencies**: 60% of total competencies
- **Emerging/Unclassified**: Handled through flexible classification system

### Priority Distribution
- **High Priority**: 40% (urgent/strategic initiatives)
- **Medium Priority**: 45% (planned development)
- **Low Priority**: 15% (compliance/maintenance)

## Usage Recommendations

### For Development Testing
1. Start with original datasets (Q1-Q4) for baseline functionality
2. Progress to specialized datasets for specific feature testing
3. Use edge cases dataset for robustness validation

### For Performance Testing
1. Use large-scale dataset for volume testing
2. Combine multiple datasets for stress testing
3. Test with real-world data volumes

### For User Acceptance Testing
1. Industry-specific datasets for domain validation
2. Mixed scenarios for comprehensive workflow testing
3. Error scenarios for user experience validation

### For Integration Testing
1. Full dataset suite for end-to-end testing
2. Combined analysis across multiple datasets
3. Cross-dataset consistency validation

## Maintenance and Updates

### Adding New Datasets
1. Follow the established CSV structure
2. Include realistic industry-specific scenarios
3. Maintain balanced priority and size distributions
4. Document testing objectives and expected outcomes

### Data Refresh Guidelines
1. Update dates to maintain relevance
2. Add new emerging technologies as they develop
3. Refresh industry-specific regulations and requirements
4. Maintain data quality standards

This comprehensive test suite ensures thorough validation of the LNA Bot system across various scenarios, industries, and edge cases while providing realistic data for development and testing purposes.