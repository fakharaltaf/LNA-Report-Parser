"""
Business Logic Engine for LNA Training Recommendations.

This module implements the core decision-making logic for determining
training delivery methods based on the specified business rules.

The engine follows a clear decision tree:
1. Check competency classification (niche vs common)
2. Apply trainee count thresholds
3. Handle special cases and overrides
4. Calculate demand scores
5. Generate comprehensive recommendations
"""

import logging
from typing import List, Dict, Any, Optional
from datetime import datetime

from ..models import (
    LNARecord,
    TrainingRecommendation,
    LNAAnalysisResult,
    DatasetSummary,
    BusinessRules,
    SkillsMapping,
    TrainingType,
    PriorityLevel,
    CompetencyClassification
)

# Set up logging
logger = logging.getLogger(__name__)


class LNADecisionEngine:
    """
    Core decision engine for LNA training recommendations.
    
    This class encapsulates the business logic for determining optimal
    training delivery methods based on competency type, trainee count,
    and priority levels.
    """
    
    def __init__(self, business_rules: BusinessRules, skills_mapping: SkillsMapping):
        """
        Initialize the decision engine with business rules and skills mapping.
        
        Args:
            business_rules: Configuration containing decision thresholds and classifications
            skills_mapping: Mapping of competencies to associated skills
        """
        self.business_rules = business_rules
        self.skills_mapping = skills_mapping
        
        logger.info("LNA Decision Engine initialized")
        logger.debug(f"Business rules: {business_rules}")
    
    def analyze_record(self, record: LNARecord) -> LNAAnalysisResult:
        """
        Analyze a single LNA record and generate a training recommendation.
        
        Args:
            record: The LNA record to analyze
            
        Returns:
            Complete analysis result with recommendation
            
        Raises:
            ValueError: If the record contains invalid data
        """
        logger.info(f"Analyzing LNA record: {record.id}")
        
        try:
            # Step 1: Determine competency classification
            competency_classification = self.business_rules.get_competency_classification(
                record.targeted_competencies
            )
            
            # Step 2: Apply business logic to determine training type
            training_type, reasoning = self._determine_training_type(
                record.estimated_trainees,
                competency_classification,
                record.targeted_competencies
            )
            
            # Step 3: Calculate demand score
            demand_score = self._calculate_demand_score(
                record.priority,
                record.estimated_trainees
            )
            
            # Step 4: Get associated skills
            associated_skills = self.skills_mapping.get_skills_for_competency(
                record.targeted_competencies
            )
            
            # Step 5: Create recommendation
            recommendation = TrainingRecommendation(
                training_type=training_type,
                reasoning=reasoning,
                priority_level=record.priority,
                demand_score=demand_score,
                competency=record.targeted_competencies,
                competency_classification=competency_classification,
                associated_skills=associated_skills
            )
            
            # Step 6: Create complete analysis result
            analysis_result = LNAAnalysisResult(
                record=record,
                recommendation=recommendation
            )
            
            logger.info(f"Analysis complete for {record.id}: {training_type}")
            return analysis_result
            
        except Exception as e:
            logger.error(f"Error analyzing record {record.id}: {str(e)}")
            raise ValueError(f"Failed to analyze record {record.id}: {str(e)}")
    
    def _determine_training_type(
        self, 
        estimated_trainees: int, 
        competency_classification: CompetencyClassification,
        competency: str
    ) -> tuple[TrainingType, str]:
        """
        Determine the appropriate training type based on business rules.
        
        Business Logic:
        1. If competency is niche → SDP (unless >50 trainees, then In-house)
        2. If trainees > 50 → In-house
        3. If trainees 11-50 → SDP
        4. If trainees ≤ 10 → External
        
        Args:
            estimated_trainees: Number of trainees requiring training
            competency_classification: Whether the competency is niche or common
            competency: The specific competency name for logging
            
        Returns:
            Tuple of (training_type, reasoning)
        """
        logger.debug(f"Determining training type for {competency}: "
                    f"{estimated_trainees} trainees, {competency_classification}")
        
        # Rule 1: Niche competencies
        if competency_classification == CompetencyClassification.NICHE:
            if estimated_trainees > self.business_rules.in_house_threshold:
                return (
                    TrainingType.IN_HOUSE,
                    f"{estimated_trainees} trainees exceeds {self.business_rules.in_house_threshold}, "
                    f"overrides niche classification for in-house delivery"
                )
            else:
                return (
                    TrainingType.SDP,
                    f"Niche competency requires specialized development program "
                    f"regardless of trainee count ({estimated_trainees})"
                )
        
        # Rule 2: Large groups (>50 trainees) → In-house
        if estimated_trainees > self.business_rules.in_house_threshold:
            return (
                TrainingType.IN_HOUSE,
                f"{estimated_trainees} trainees exceeds {self.business_rules.in_house_threshold}, "
                f"common competency suitable for in-house delivery"
            )
        
        # Rule 3: Medium groups (11-50 trainees) → SDP
        if estimated_trainees > self.business_rules.external_threshold:
            return (
                TrainingType.SDP,
                f"{estimated_trainees} trainees falls in SDP range "
                f"({self.business_rules.external_threshold + 1}-{self.business_rules.in_house_threshold})"
            )
        
        # Rule 4: Small groups (≤10 trainees) → External
        return (
            TrainingType.EXTERNAL,
            f"{estimated_trainees} trainees is at or below {self.business_rules.external_threshold}, "
            f"common competency suitable for external training"
        )
    
    def _calculate_demand_score(self, priority: PriorityLevel, estimated_trainees: int) -> float:
        """
        Calculate demand score based on priority and trainee count.
        
        Formula: demand_score = priority_weight × trainee_count
        
        Args:
            priority: Priority level of the training need
            estimated_trainees: Number of trainees requiring training
            
        Returns:
            Calculated demand score
        """
        priority_weight = self.business_rules.priority_weights.get(priority, 1)
        demand_score = priority_weight * estimated_trainees
        
        logger.debug(f"Demand score calculation: {priority} (weight={priority_weight}) × "
                    f"{estimated_trainees} = {demand_score}")
        
        return float(demand_score)
    
    def analyze_dataset(self, records: List[LNARecord]) -> tuple[List[LNAAnalysisResult], DatasetSummary]:
        """
        Analyze a complete dataset of LNA records.
        
        Args:
            records: List of LNA records to analyze
            
        Returns:
            Tuple of (analysis_results, dataset_summary)
        """
        logger.info(f"Analyzing dataset with {len(records)} records")
        
        analysis_results = []
        
        # Analyze each record
        for record in records:
            try:
                result = self.analyze_record(record)
                analysis_results.append(result)
            except Exception as e:
                logger.error(f"Failed to analyze record {record.id}: {str(e)}")
                # Continue with other records
                continue
        
        # Generate summary statistics
        summary = self._generate_dataset_summary(analysis_results)
        
        logger.info(f"Dataset analysis complete: {len(analysis_results)} successful analyses")
        return analysis_results, summary
    
    def _generate_dataset_summary(self, analysis_results: List[LNAAnalysisResult]) -> DatasetSummary:
        """
        Generate summary statistics for a dataset of analysis results.
        
        Args:
            analysis_results: List of completed analysis results
            
        Returns:
            Dataset summary with aggregated statistics
        """
        if not analysis_results:
            return DatasetSummary(
                total_entries=0,
                total_trainees=0,
                average_trainees_per_entry=0.0
            )
        
        # Basic statistics
        total_entries = len(analysis_results)
        total_trainees = sum(result.record.estimated_trainees for result in analysis_results)
        average_trainees = total_trainees / total_entries if total_entries > 0 else 0.0
        
        # Training type distribution
        training_type_counts = {}
        for result in analysis_results:
            training_type = result.recommendation.training_type
            training_type_counts[training_type] = training_type_counts.get(training_type, 0) + 1
        
        # Priority distribution
        priority_counts = {}
        for result in analysis_results:
            priority = result.record.priority
            priority_counts[priority] = priority_counts.get(priority, 0) + 1
        
        # Competency type distribution
        competency_type_counts = {}
        for result in analysis_results:
            comp_classification = result.recommendation.competency_classification
            competency_type_counts[comp_classification] = competency_type_counts.get(comp_classification, 0) + 1
        
        # Rank competencies by demand score
        competency_demands = {}
        for result in analysis_results:
            competency = result.recommendation.competency
            demand_score = result.recommendation.demand_score
            training_type = result.recommendation.training_type
            
            if competency not in competency_demands:
                competency_demands[competency] = {
                    'competency': competency,
                    'demand_score': demand_score,
                    'training_type': training_type,
                    'total_trainees': result.record.estimated_trainees
                }
            else:
                # If duplicate competency, take the one with higher demand
                if demand_score > competency_demands[competency]['demand_score']:
                    competency_demands[competency].update({
                        'demand_score': demand_score,
                        'training_type': training_type,
                        'total_trainees': result.record.estimated_trainees
                    })
        
        # Sort by demand score (highest first)
        ranked_competencies = sorted(
            competency_demands.values(),
            key=lambda x: x['demand_score'],
            reverse=True
        )
        
        # Add rank information
        for i, comp in enumerate(ranked_competencies, 1):
            comp['rank'] = i
        
        return DatasetSummary(
            total_entries=total_entries,
            total_trainees=total_trainees,
            average_trainees_per_entry=round(average_trainees, 2),
            training_type_distribution=training_type_counts,
            priority_distribution=priority_counts,
            competency_type_distribution=competency_type_counts,
            competencies_ranked_by_demand=ranked_competencies
        )