"""
Data models for the LNA (Learning Need Analysis) Bot.

This module defines the core data structures used throughout the application,
providing type safety, validation, and clear interfaces for data handling.
"""

from datetime import datetime
from enum import Enum
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field, validator


class PriorityLevel(str, Enum):
    """Enumeration for priority levels in LNA requests."""
    HIGH = "High"
    MEDIUM = "Medium"
    LOW = "Low"


class TrainingType(str, Enum):
    """Enumeration for training delivery types."""
    IN_HOUSE = "In-house"
    SDP = "SDP"  # Special Development Program
    EXTERNAL = "External"


class CompetencyType(str, Enum):
    """Enumeration for competency classifications."""
    TECHNICAL = "Technical"
    LEADERSHIP = "Leadership"
    SOFT_SKILLS = "Soft Skills"
    COMPLIANCE = "Compliance"


class CompetencyClassification(str, Enum):
    """Enumeration for competency complexity classification."""
    NICHE = "niche"
    COMMON = "common"


class RequestType(str, Enum):
    """Enumeration for training request types."""
    NEW_TRAINING = "New Training"
    UPSKILLING = "Upskilling"
    REFRESHER = "Refresher"


class LNARecord(BaseModel):
    """
    Represents a single Learning Need Analysis record.
    
    This model validates and structures the input data from LNA reports,
    ensuring data integrity and providing a clean interface for processing.
    """
    
    id: str = Field(..., description="Unique identifier for the LNA record")
    submission: datetime = Field(..., description="Date when the request was submitted")
    priority: PriorityLevel = Field(..., description="Priority level of the training need")
    competency_type: CompetencyType = Field(..., description="Category of competency")
    job_families: str = Field(..., description="Relevant job families/departments")
    targeted_competencies: str = Field(..., description="Specific competency to be developed")
    request_type: RequestType = Field(..., description="Type of training request")
    targeted_audience: str = Field(..., description="Who will receive the training")
    estimated_trainees: int = Field(..., gt=0, description="Number of people requiring training")
    comment: str = Field(..., description="Additional context and justification")
    year: int = Field(..., ge=2020, le=2030, description="Training year")
    division: str = Field(..., description="Organizational division")
    department: str = Field(..., description="Specific department")
    section: str = Field(..., description="Team or section within department")

    @validator('estimated_trainees')
    def validate_estimated_trainees(cls, v):
        """Ensure estimated trainees is a positive integer."""
        if v <= 0:
            raise ValueError('Estimated trainees must be greater than 0')
        return v

    @validator('submission')
    def validate_submission_date(cls, v):
        """Ensure submission date is not in the future beyond reasonable limits."""
        if v > datetime.now().replace(year=datetime.now().year + 1):
            raise ValueError('Submission date cannot be more than 1 year in the future')
        return v


class TrainingRecommendation(BaseModel):
    """
    Represents the AI bot's training recommendation for an LNA record.
    
    This model encapsulates the decision logic output, including the recommended
    training type, reasoning, and associated metadata.
    """
    
    training_type: TrainingType = Field(..., description="Recommended training delivery method")
    reasoning: str = Field(..., description="Explanation for the recommendation")
    priority_level: PriorityLevel = Field(..., description="Priority level from the original request")
    demand_score: float = Field(..., ge=0, description="Calculated demand score")
    competency: str = Field(..., description="The competency being addressed")
    competency_classification: CompetencyClassification = Field(..., description="Niche or common classification")
    associated_skills: List[str] = Field(default_factory=list, description="Skills associated with the competency")
    
    class Config:
        """Pydantic configuration for the model."""
        pass


class LNAAnalysisResult(BaseModel):
    """
    Represents the complete analysis result for an LNA record.
    
    This model combines the original record data with the AI bot's
    recommendation and analysis.
    """
    
    record: LNARecord = Field(..., description="Original LNA record")
    recommendation: TrainingRecommendation = Field(..., description="AI bot recommendation")
    analysis_timestamp: datetime = Field(default_factory=datetime.now, description="When the analysis was performed")
    
    class Config:
        """Pydantic configuration for the model."""
        pass


class DatasetSummary(BaseModel):
    """
    Represents summary statistics for a dataset of LNA records.
    
    This model provides aggregated insights across multiple LNA records,
    useful for reporting and high-level analysis.
    """
    
    total_entries: int = Field(..., ge=0, description="Total number of LNA entries")
    total_trainees: int = Field(..., ge=0, description="Sum of all estimated trainees")
    average_trainees_per_entry: float = Field(..., ge=0, description="Average trainees per entry")
    
    training_type_distribution: Dict[str, int] = Field(
        default_factory=dict, 
        description="Count of each training type recommendation"
    )
    
    priority_distribution: Dict[str, int] = Field(
        default_factory=dict,
        description="Count of each priority level"
    )
    
    competency_type_distribution: Dict[str, int] = Field(
        default_factory=dict,
        description="Count of each competency type"
    )
    
    competencies_ranked_by_demand: List[Dict[str, Any]] = Field(
        default_factory=list,
        description="Competencies sorted by demand score (highest to lowest)"
    )
    
    analysis_date: datetime = Field(default_factory=datetime.now, description="When the summary was generated")
    
    class Config:
        """Pydantic configuration for the model."""
        use_enum_values = True


class BusinessRules(BaseModel):
    """
    Represents the business rules configuration for training type decisions.
    
    This model encapsulates the decision logic parameters, making them
    easily configurable and testable.
    """
    
    # Trainee count thresholds
    external_threshold: int = Field(default=10, description="Max trainees for external training")
    in_house_threshold: int = Field(default=50, description="Min trainees for in-house training")
    
    # Priority weights for demand calculation
    priority_weights: Dict[str, int] = Field(
        default={
            PriorityLevel.HIGH: 3,
            PriorityLevel.MEDIUM: 2,
            PriorityLevel.LOW: 1
        },
        description="Weight multipliers for priority levels"
    )
    
    # Competency classifications
    niche_competencies: List[str] = Field(default_factory=list, description="List of niche competencies")
    common_competencies: List[str] = Field(default_factory=list, description="List of common competencies")
    
    def is_niche_competency(self, competency: str) -> bool:
        """Check if a competency is classified as niche."""
        return competency in self.niche_competencies
    
    def is_common_competency(self, competency: str) -> bool:
        """Check if a competency is classified as common."""
        return competency in self.common_competencies
    
    def get_competency_classification(self, competency: str) -> CompetencyClassification:
        """Get the classification of a competency."""
        if self.is_niche_competency(competency):
            return CompetencyClassification.NICHE
        elif self.is_common_competency(competency):
            return CompetencyClassification.COMMON
        else:
            # Default to common if not explicitly classified
            return CompetencyClassification.COMMON
    
    class Config:
        """Pydantic configuration for the model."""
        use_enum_values = True


class SkillsMapping(BaseModel):
    """
    Represents the mapping between competencies and their associated skills.
    
    This model provides a structured way to store and retrieve the skills
    associated with each competency.
    """
    
    competency_skills: Dict[str, List[str]] = Field(
        default_factory=dict,
        description="Mapping of competency names to their associated skills"
    )
    
    def get_skills_for_competency(self, competency: str) -> List[str]:
        """Get the list of skills associated with a competency."""
        return self.competency_skills.get(competency, [])
    
    def add_competency_skills(self, competency: str, skills: List[str]) -> None:
        """Add or update skills for a competency."""
        self.competency_skills[competency] = skills
    
    def has_competency(self, competency: str) -> bool:
        """Check if a competency has associated skills defined."""
        return competency in self.competency_skills


class ProcessingStatistics(BaseModel):
    """
    Statistics about data processing operations.
    
    This model captures important metrics about file processing,
    including success rates, error counts, and validation warnings.
    """
    
    total_rows: int = Field(description="Total number of rows in the input data")
    successful_records: int = Field(description="Number of records successfully processed")
    failed_records: int = Field(description="Number of records that failed processing")
    validation_warnings: List[str] = Field(default_factory=list, description="List of validation warning messages")
    processing_errors: List[str] = Field(default_factory=list, description="List of processing error messages")
    
    @property
    def success_rate(self) -> float:
        """Calculate the success rate as a percentage."""
        if self.total_rows == 0:
            return 0.0
        return (self.successful_records / self.total_rows) * 100
    
    @property
    def has_warnings(self) -> bool:
        """Check if there are any validation warnings."""
        return len(self.validation_warnings) > 0
    
    @property
    def has_errors(self) -> bool:
        """Check if there are any processing errors."""
        return len(self.processing_errors) > 0