# LNA Training Recommendation Business Rules Configuration

## Training Type Decision Logic

### Employee Count Rules
```
IF estimated_trainees > 50 THEN training_type = "In-house"
ELSE IF estimated_trainees > 10 THEN training_type = "SDP" (Special Development Program)
ELSE training_type = "External"
```

### Competency Type Override Rules
```
IF competency_type = "niche" THEN training_type = "SDP"
IF competency_type = "common" AND estimated_trainees > 50 THEN training_type = "In-house"
```

### Priority Level Weights
```
High Priority = 3 points
Medium Priority = 2 points  
Low Priority = 1 point
```

### Competency Classification
```
NICHE COMPETENCIES:
- Quantum Computing Fundamentals
- Blockchain Technology
- Artificial Intelligence Ethics
- Advanced Data Analytics
- Machine Learning & AI
- IoT & Embedded Systems
- 3D Printing & Additive Manufacturing
- Renewable Energy Systems
- Robotics & Automation
- Telemedicine & Digital Health
- Precision Medicine & Genomics
- Advanced Materials Science
- Cryptocurrency & Digital Assets
- Algorithmic Trading Systems
- ESG Reporting & Sustainability Metrics
- Virtual Reality & Augmented Reality
- Sustainable Engineering Practices
- Advanced Manufacturing Automation
- Computer Vision & Image Recognition
- Natural Language Processing
- Extended Reality (XR) Development
- Autonomous Vehicle Systems
- Space Technology & Satellite Systems
- Sustainable Energy Storage Systems
- Edge Computing & 5G Networks
- Serverless Architecture & Functions
- Advanced Cybersecurity Threat Hunting
- Decentralized Finance (DeFi) Systems
- AI-Powered Diagnostics
- Industry 4.0 Integration
- Climate Risk Assessment

COMMON COMPETENCIES:
- Strategic Planning & Decision Making
- Change Management
- Emotional Intelligence & Team Dynamics
- Project Management Certification
- Crisis Management & Business Continuity
- Innovation Management
- Communication & Presentation Skills
- Cross-Cultural Communication
- Customer Relationship Management
- Time Management & Productivity
- Mental Health & Wellness
- Data Privacy & GDPR
- Workplace Safety & Health
- Anti-Money Laundering (AML)
- Environmental Regulations
- Financial Risk Assessment
- Advanced Excel & Financial Modeling
- Lean Manufacturing & Six Sigma
- Database Administration & Optimization
- Mobile App Development
- Cybersecurity & Information Security
- Cloud Computing & DevOps
- Microservices Architecture
- DevSecOps & Security Integration
- Containerization & Kubernetes
- API Design & Management
- Agile Leadership & Scrum Mastery
- Digital Marketing & Social Media
- Transformational Leadership
- Digital Transformation Leadership
- Strategic Thinking & Planning
- Data-Driven Decision Making
- Diversity & Inclusion Awareness
- Remote Work & Virtual Collaboration
- Ethical Decision Making
- Cultural Intelligence & Global Mindset
- Effective Communication in Digital Age
- Consultative Selling Techniques
- Neuromarketing & Consumer Psychology
- Future of Work Adaptation
- ISO Quality Standards
- Updated Privacy Regulations
- Medical Device Cybersecurity
```

### Expected Output Format
```json
{
  "recommendation": {
    "training_type": "In-house|SDP|External",
    "priority_level": "High|Medium|Low",
    "competencies": [
      {
        "name": "competency_name",
        "demand_score": "calculated_score",
        "skills": ["skill1", "skill2", "skill3"],
        "estimated_trainees": "number"
      }
    ],
    "competencies_ranked_by_demand": [
      "competency1", "competency2", "competency3"
    ]
  }
}
```

### Demand Score Calculation
```
demand_score = (priority_weight * urgency_multiplier * trainee_count) / 100
where:
- priority_weight: High=3, Medium=2, Low=1
- urgency_multiplier: Based on submission date and current date
- trainee_count: Number of estimated trainees
```

### Urgency Multiplier Calculation
```
days_since_submission = current_date - submission_date
IF days_since_submission > 180 THEN urgency_multiplier = 0.5
ELSE IF days_since_submission > 90 THEN urgency_multiplier = 0.7
ELSE IF days_since_submission > 30 THEN urgency_multiplier = 1.0
ELSE urgency_multiplier = 1.5
```