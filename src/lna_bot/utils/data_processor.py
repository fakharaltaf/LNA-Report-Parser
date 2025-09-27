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
    
    def dataframe_to_records_with_stats(self, df: pd.DataFrame) -> tuple[List[LNARecord], Any]:
        """
        Convert a pandas DataFrame to a list of LNARecord objects with detailed statistics.
        
        Args:
            df: DataFrame containing LNA data
            
        Returns:
            Tuple of (List of validated LNARecord objects, ProcessingStatistics)
            
        Raises:
            DataProcessingError: If no records could be processed
        """
        from ..models import ProcessingStatistics
        
        logger.info(f"Converting DataFrame to LNARecord objects ({len(df)} rows)")
        
        records = []
        errors = []
        
        for idx, row in df.iterrows():
            try:
                record = self._row_to_record(row)
                records.append(record)
            except Exception as e:
                row_num = int(idx) + 1 if isinstance(idx, (int, float)) else idx
                error_msg = f"Row {row_num}: {str(e)}"
                errors.append(error_msg)
                logger.warning(f"Failed to convert row {row_num}: {str(e)}")
        
        # Create processing statistics
        stats = ProcessingStatistics(
            total_rows=len(df),
            successful_records=len(records),
            failed_records=len(errors),
            processing_errors=errors
        )
        
        if len(errors) == len(df):
            raise DataProcessingError("Failed to convert any rows from DataFrame")
        
        logger.info(f"Successfully converted {len(records)} out of {len(df)} records ({stats.success_rate:.1f}% success rate)")
        return records, stats
    
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
            
            # Handle string fields with fallbacks for missing values
            def safe_str(value, field_name, default="Unknown"):
                if pd.isna(value) or str(value).strip() == '' or str(value).strip().lower() == 'nan':
                    if field_name in ['ID', 'Targeted competencies']:
                        raise ValueError(f"{field_name} is null or empty - this is a critical field")
                    logger.warning(f"Missing {field_name} - using default '{default}'")
                    return default
                return str(value).strip()

            # Create LNARecord
            record = LNARecord(
                id=safe_str(row['ID'], 'ID'),
                submission=submission_date,
                priority=priority,
                competency_type=competency_type,
                job_families=safe_str(row['Job families'], 'Job families', 'General'),
                targeted_competencies=safe_str(row['Targeted competencies'], 'Targeted competencies'),
                request_type=request_type,
                targeted_audience=safe_str(row['Targeted audience'], 'Targeted audience', 'General Staff'),
                estimated_trainees=estimated_trainees,
                comment=safe_str(row['Comment'], 'Comment', 'No comment provided'),
                year=year,
                division=safe_str(row['Division'], 'Division', 'General'),
                department=safe_str(row['Department'], 'Department', 'General'),
                section=safe_str(row['Section'], 'Section', 'General')
            )
            
            return record
            
        except Exception as e:
            raise ValueError(f"Invalid row data: {str(e)}")
    
    def _parse_date(self, date_value: Any) -> datetime:
        """Parse a date value from various formats."""
        if pd.isna(date_value) or str(date_value).strip() == '':
            # Use current date as fallback for missing submission dates
            logger.warning("Missing submission date - using current date as fallback")
            return datetime.now()
        
        if isinstance(date_value, datetime):
            return date_value
        
        try:
            # Try parsing as string
            return date_parser.parse(str(date_value))
        except Exception:
            # Use current date as fallback for invalid dates
            logger.warning(f"Cannot parse date '{date_value}' - using current date as fallback")
            return datetime.now()
    
    def _parse_priority(self, priority_value: Any) -> PriorityLevel:
        """Parse priority level from string value."""
        if pd.isna(priority_value) or str(priority_value).strip() == '':
            raise ValueError("Priority value is null or empty - this is a critical field")
        
        priority_str = str(priority_value).strip()
        
        # Handle common alternative priority values
        priority_mapping = {
            'Very High': 'High',
            'Critical': 'High', 
            'Urgent': 'High',
            'Normal': 'Medium',
            'Standard': 'Medium',
            'Minor': 'Low',
            'Minimal': 'Low'
        }
        
        if priority_str in priority_mapping:
            priority_str = priority_mapping[priority_str]
            logger.warning(f"Mapped priority '{priority_value}' to '{priority_str}'")
        
        try:
            return PriorityLevel(priority_str)
        except ValueError:
            # Default to Medium priority for invalid values
            logger.warning(f"Invalid priority level '{priority_str}' - defaulting to Medium")
            return PriorityLevel.MEDIUM
    
    def _parse_competency_type(self, competency_type_value: Any) -> CompetencyType:
        """Parse competency type from string value."""
        if pd.isna(competency_type_value) or str(competency_type_value).strip() == '':
            logger.warning("Missing competency type - defaulting to Technical")
            return CompetencyType.TECHNICAL
        
        competency_type_str = str(competency_type_value).strip()
        
        try:
            return CompetencyType(competency_type_str)
        except ValueError:
            # Default to Technical for invalid competency types
            logger.warning(f"Invalid competency type '{competency_type_str}' - defaulting to Technical")
            return CompetencyType.TECHNICAL
    
    def _parse_request_type(self, request_type_value: Any) -> RequestType:
        """Parse request type from string value."""
        if pd.isna(request_type_value) or str(request_type_value).strip() == '':
            logger.warning("Missing request type - defaulting to New Training")
            return RequestType.NEW_TRAINING
        
        request_type_str = str(request_type_value).strip()
        
        # Handle common alternative request type values
        request_mapping = {
            'New': 'New Training',
            'Training': 'New Training',
            'Update': 'Upskilling',
            'Skill Development': 'Upskilling',
            'Refresh': 'Refresher',
            'Review': 'Refresher'
        }
        
        if request_type_str in request_mapping:
            request_type_str = request_mapping[request_type_str]
            logger.warning(f"Mapped request type '{request_type_value}' to '{request_type_str}'")
        
        try:
            return RequestType(request_type_str)
        except ValueError:
            # Default to New Training for invalid request types
            logger.warning(f"Invalid request type '{request_type_str}' - defaulting to New Training")
            return RequestType.NEW_TRAINING
    
    def _parse_trainees(self, trainees_value: Any) -> int:
        """Parse estimated trainees from numeric value."""
        if pd.isna(trainees_value) or str(trainees_value).strip() == '':
            raise ValueError("Estimated trainees value is null or empty - this is a critical field")
        
        try:
            trainees = int(float(trainees_value))  # Handle both int and float
            if trainees <= 0:
                raise ValueError("Estimated trainees must be greater than 0")
            if trainees > 100000:  # Cap extremely large values
                logger.warning(f"Very large trainee count ({trainees}) - capping at 10000")
                return 10000
            return trainees
        except (ValueError, TypeError):
            raise ValueError(f"Invalid estimated trainees value: {trainees_value}")
    
    def _parse_year(self, year_value: Any) -> int:
        """Parse year from numeric value."""
        if pd.isna(year_value) or str(year_value).strip() == '':
            # Use current year as fallback
            current_year = datetime.now().year
            logger.warning(f"Missing year - using current year {current_year}")
            return current_year
        
        try:
            year = int(float(year_value))  # Handle both int and float
            if year < 2020 or year > 2030:
                # Use current year for out-of-range values
                current_year = datetime.now().year
                logger.warning(f"Year {year} out of range (2020-2030) - using current year {current_year}")
                return current_year
            return year
        except (ValueError, TypeError):
            # Use current year as fallback for invalid years
            current_year = datetime.now().year
            logger.warning(f"Invalid year value '{year_value}' - using current year {current_year}")
            return current_year
    
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