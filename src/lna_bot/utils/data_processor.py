"""
Data processing utilities for LNA Bot.

This module provides utilities for converting between different data formats,
processing CSV data, and preparing data for analysis.
"""

import logging
from datetime import datetime
from typing import List, Dict, Any, Optional
import pandas as pd
from dateutil import parser as date_parser

from ..models import (
    LNARecord, 
    PriorityLevel, 
    CompetencyType, 
    RequestType,
    LNAAnalysisResult,
    DatasetSummary
)

logger = logging.getLogger(__name__)


class DataProcessingError(Exception):
    """Raised when there's an error in data processing."""
    pass


class DataProcessor:
    """
    Handles conversion and processing of LNA data.
    
    This class provides methods to convert between different data formats
    and prepare data for analysis by the decision engine.
    """
    
    def __init__(self):
        """Initialize the data processor."""
        logger.info("Data processor initialized")
    
    def dataframe_to_records(self, df: pd.DataFrame) -> List[LNARecord]:
        """
        Convert a pandas DataFrame to a list of LNARecord objects.
        
        Args:
            df: DataFrame containing LNA data
            
        Returns:
            List of validated LNARecord objects
            
        Raises:
            DataProcessingError: If data conversion fails
        """
        logger.info(f"Converting DataFrame to LNARecord objects ({len(df)} rows)")
        
        records = []
        errors = []
        
        for index, row in df.iterrows():
            try:
                record = self._row_to_record(row)
                records.append(record)
            except Exception as e:
                error_msg = f"Row {index}: {str(e)}"
                errors.append(error_msg)
                logger.warning(f"Failed to convert row {index}: {str(e)}")
        
        if errors:
            logger.error(f"Failed to convert {len(errors)} rows out of {len(df)}")
            if len(errors) == len(df):
                raise DataProcessingError("Failed to convert any rows from DataFrame")
            logger.warning(f"Proceeding with {len(records)} valid records")
        
        logger.info(f"Successfully converted {len(records)} records")
        return records
    
    def _row_to_record(self, row: pd.Series) -> LNARecord:
        """
        Convert a pandas Series (DataFrame row) to an LNARecord.
        
        Args:
            row: Pandas Series containing row data
            
        Returns:
            Validated LNARecord object
            
        Raises:
            ValueError: If row data is invalid
        """
        try:
            # Parse submission date
            submission_date = self._parse_date(row['Submission'])
            
            # Parse priority level
            priority = self._parse_priority(row['Priority'])
            
            # Parse competency type
            competency_type = self._parse_competency_type(row['Competency type'])
            
            # Parse request type
            request_type = self._parse_request_type(row['Request type'])
            
            # Parse estimated trainees
            estimated_trainees = self._parse_trainees(row['Estimated trainees'])
            
            # Parse year
            year = self._parse_year(row['Year'])
            
            # Create LNARecord
            record = LNARecord(
                id=str(row['ID']).strip(),
                submission=submission_date,
                priority=priority,
                competency_type=competency_type,
                job_families=str(row['Job families']).strip(),
                targeted_competencies=str(row['Targeted competencies']).strip(),
                request_type=request_type,
                targeted_audience=str(row['Targeted audience']).strip(),
                estimated_trainees=estimated_trainees,
                comment=str(row['Comment']).strip(),
                year=year,
                division=str(row['Division']).strip(),
                department=str(row['Department']).strip(),
                section=str(row['Section']).strip()
            )
            
            return record
            
        except Exception as e:
            raise ValueError(f"Invalid row data: {str(e)}")
    
    def _parse_date(self, date_value: Any) -> datetime:
        """Parse a date value from various formats."""
        if pd.isna(date_value):
            raise ValueError("Date value is null or empty")
        
        if isinstance(date_value, datetime):
            return date_value
        
        try:
            # Try parsing as string
            return date_parser.parse(str(date_value))
        except Exception:
            raise ValueError(f"Cannot parse date: {date_value}")
    
    def _parse_priority(self, priority_value: Any) -> PriorityLevel:
        """Parse priority level from string value."""
        if pd.isna(priority_value):
            raise ValueError("Priority value is null or empty")
        
        priority_str = str(priority_value).strip()
        
        try:
            return PriorityLevel(priority_str)
        except ValueError:
            raise ValueError(f"Invalid priority level: {priority_str}")
    
    def _parse_competency_type(self, competency_type_value: Any) -> CompetencyType:
        """Parse competency type from string value."""
        if pd.isna(competency_type_value):
            raise ValueError("Competency type value is null or empty")
        
        competency_type_str = str(competency_type_value).strip()
        
        try:
            return CompetencyType(competency_type_str)
        except ValueError:
            raise ValueError(f"Invalid competency type: {competency_type_str}")
    
    def _parse_request_type(self, request_type_value: Any) -> RequestType:
        """Parse request type from string value."""
        if pd.isna(request_type_value):
            raise ValueError("Request type value is null or empty")
        
        request_type_str = str(request_type_value).strip()
        
        try:
            return RequestType(request_type_str)
        except ValueError:
            raise ValueError(f"Invalid request type: {request_type_str}")
    
    def _parse_trainees(self, trainees_value: Any) -> int:
        """Parse estimated trainees from numeric value."""
        if pd.isna(trainees_value):
            raise ValueError("Estimated trainees value is null or empty")
        
        try:
            trainees = int(float(trainees_value))  # Handle both int and float
            if trainees <= 0:
                raise ValueError("Estimated trainees must be greater than 0")
            return trainees
        except (ValueError, TypeError):
            raise ValueError(f"Invalid estimated trainees value: {trainees_value}")
    
    def _parse_year(self, year_value: Any) -> int:
        """Parse year from numeric value."""
        if pd.isna(year_value):
            raise ValueError("Year value is null or empty")
        
        try:
            year = int(float(year_value))  # Handle both int and float
            if year < 2020 or year > 2030:
                raise ValueError("Year must be between 2020 and 2030")
            return year
        except (ValueError, TypeError):
            raise ValueError(f"Invalid year value: {year_value}")
    
    def analysis_results_to_dict(self, results: List[LNAAnalysisResult]) -> List[Dict[str, Any]]:
        """
        Convert analysis results to a list of dictionaries for easy serialization.
        
        Args:
            results: List of analysis results
            
        Returns:
            List of dictionaries containing the analysis data
        """
        logger.info(f"Converting {len(results)} analysis results to dictionaries")
        
        output = []
        
        for result in results:
            result_dict = {
                'id': result.record.id,
                'submission': result.record.submission.isoformat(),
                'priority': result.record.priority.value if hasattr(result.record.priority, 'value') else result.record.priority,
                'competency': result.recommendation.competency,
                'estimated_trainees': result.record.estimated_trainees,
                'competency_classification': result.recommendation.competency_classification.value if hasattr(result.recommendation.competency_classification, 'value') else result.recommendation.competency_classification,
                'expected_training_type': result.recommendation.training_type.value if hasattr(result.recommendation.training_type, 'value') else result.recommendation.training_type,
                'reasoning': result.recommendation.reasoning,
                'demand_score': result.recommendation.demand_score,
                'associated_skills': result.recommendation.associated_skills,
                'job_families': result.record.job_families,
                'targeted_audience': result.record.targeted_audience,
                'division': result.record.division,
                'department': result.record.department,
                'section': result.record.section,
                'analysis_timestamp': result.analysis_timestamp.isoformat()
            }
            output.append(result_dict)
        
        return output
    
    def summary_to_dict(self, summary: DatasetSummary) -> Dict[str, Any]:
        """
        Convert dataset summary to dictionary for easy serialization.
        
        Args:
            summary: Dataset summary object
            
        Returns:
            Dictionary containing the summary data
        """
        return {
            'total_entries': summary.total_entries,
            'total_trainees': summary.total_trainees,
            'average_trainees_per_entry': summary.average_trainees_per_entry,
            'training_type_distribution': summary.training_type_distribution,
            'priority_distribution': summary.priority_distribution,
            'competency_type_distribution': summary.competency_type_distribution,
            'competencies_ranked_by_demand': summary.competencies_ranked_by_demand,
            'analysis_date': summary.analysis_date.isoformat()
        }
    
    def create_summary_table(self, summary: DatasetSummary) -> str:
        """
        Create a formatted text table of the dataset summary.
        
        Args:
            summary: Dataset summary object
            
        Returns:
            Formatted string table
        """
        lines = []
        lines.append("=" * 60)
        lines.append("LNA DATASET ANALYSIS SUMMARY")
        lines.append("=" * 60)
        lines.append("")
        
        # Basic statistics
        lines.append("BASIC STATISTICS:")
        lines.append(f"  Total Entries: {summary.total_entries}")
        lines.append(f"  Total Trainees: {summary.total_trainees}")
        lines.append(f"  Average Trainees per Entry: {summary.average_trainees_per_entry:.2f}")
        lines.append("")
        
        # Training type distribution
        lines.append("TRAINING TYPE DISTRIBUTION:")
        for training_type, count in summary.training_type_distribution.items():
            percentage = (count / summary.total_entries * 100) if summary.total_entries > 0 else 0
            lines.append(f"  {training_type}: {count} ({percentage:.1f}%)")
        lines.append("")
        
        # Priority distribution
        lines.append("PRIORITY LEVEL DISTRIBUTION:")
        for priority, count in summary.priority_distribution.items():
            percentage = (count / summary.total_entries * 100) if summary.total_entries > 0 else 0
            lines.append(f"  {priority}: {count} ({percentage:.1f}%)")
        lines.append("")
        
        # Top competencies by demand
        lines.append("TOP COMPETENCIES BY DEMAND:")
        for i, comp in enumerate(summary.competencies_ranked_by_demand[:10], 1):
            lines.append(f"  {i:2d}. {comp['competency']}")
            lines.append(f"      Demand Score: {comp['demand_score']}")
            lines.append(f"      Training Type: {comp['training_type']}")
            lines.append(f"      Trainees: {comp['total_trainees']}")
            lines.append("")
        
        lines.append("=" * 60)
        lines.append(f"Analysis generated on: {summary.analysis_date.strftime('%Y-%m-%d %H:%M:%S')}")
        lines.append("=" * 60)
        
        return "\n".join(lines)
    
    def summary_to_dict(self, summary: DatasetSummary) -> Dict[str, Any]:
        """
        Convert DatasetSummary to dictionary format.
        
        Args:
            summary: DatasetSummary object to convert
            
        Returns:
            Dictionary representation of the summary
        """
        try:
            return {
                'total_entries': summary.total_entries,
                'total_trainees': summary.total_trainees,
                'average_trainees_per_entry': summary.average_trainees_per_entry,
                'training_type_distribution': summary.training_type_distribution,
                'priority_distribution': summary.priority_distribution,
                'competency_type_distribution': summary.competency_type_distribution,
                'competencies_ranked_by_demand': summary.competencies_ranked_by_demand,
                'analysis_date': summary.analysis_date.isoformat()
            }
        except Exception as e:
            logger.error(f"Failed to convert summary to dict: {str(e)}")
            raise DataProcessingError(f"Summary conversion failed: {str(e)}")