"""
Main LNA Bot Application Module.

This module provides the main application interface for the LNA
(Learning Need Analysis) Bot. It orchestrates the various components
to provide a complete analysis pipeline.
"""

import logging
from pathlib import Path
from typing import List, Dict, Any, Optional, Tuple, Union
import json

from .models import LNARecord, LNAAnalysisResult, DatasetSummary, BusinessRules, SkillsMapping
from .core.decision_engine import LNADecisionEngine
from .utils.config_loader import ConfigurationLoader, DataLoader
from .utils.data_processor import DataProcessor

logger = logging.getLogger(__name__)


class LNABotError(Exception):
    """Base exception for LNA Bot errors."""
    pass


class LNABot:
    """
    Main LNA Bot application class.
    
    This class provides the high-level interface for analyzing LNA reports
    and generating training recommendations.
    """
    
    def __init__(self, config_dir: Optional[Path] = None):
        """
        Initialize the LNA Bot.
        
        Args:
            config_dir: Directory containing configuration files
        """
        self.config_dir = config_dir or Path("config")
        
        # Initialize components
        self.config_loader = ConfigurationLoader(self.config_dir)
        self.data_loader = DataLoader()
        self.data_processor = DataProcessor()
        
        # Load configuration
        self.business_rules: Optional[BusinessRules] = None
        self.skills_mapping: Optional[SkillsMapping] = None
        self.decision_engine: Optional[LNADecisionEngine] = None
        
        self._initialize_components()
        
        logger.info("LNA Bot initialized successfully")
    
    def _initialize_components(self):
        """Initialize the bot components with configuration."""
        try:
            # Load configuration
            self.business_rules = self.config_loader.load_business_rules()
            self.skills_mapping = self.config_loader.load_skills_mapping()
            
            # Initialize decision engine
            self.decision_engine = LNADecisionEngine(
                business_rules=self.business_rules,
                skills_mapping=self.skills_mapping
            )
            
            logger.info("All components initialized successfully")
            
        except Exception as e:
            logger.error(f"Failed to initialize components: {str(e)}")
            raise LNABotError(f"Initialization failed: {str(e)}")
    
    def analyze_csv_file(self, csv_file_path: Path) -> Tuple[List[LNAAnalysisResult], DatasetSummary]:
        """
        Analyze an LNA CSV file and generate recommendations.
        
        Args:
            csv_file_path: Path to the CSV file containing LNA data
            
        Returns:
            Tuple of (analysis_results, dataset_summary)
            
        Raises:
            LNABotError: If analysis fails
        """
        logger.info(f"Starting analysis of CSV file: {csv_file_path}")
        
        try:
            # Load CSV data
            df = self.data_loader.load_csv_file(csv_file_path)
            
            # Validate data
            validation_errors = self.data_loader.validate_dataframe(df)
            if validation_errors:
                logger.warning(f"Data validation warnings: {validation_errors}")
            
            # Convert to LNARecord objects
            records = self.data_processor.dataframe_to_records(df)
            
            # Analyze records
            assert self.decision_engine is not None, "Decision engine not initialized"
            analysis_results, summary = self.decision_engine.analyze_dataset(records)
            
            logger.info(f"Analysis complete: {len(analysis_results)} records processed")
            
            return analysis_results, summary
            
        except Exception as e:
            logger.error(f"Analysis failed: {str(e)}")
            raise LNABotError(f"Analysis failed: {str(e)}")
    
    def analyze_excel_file(self, file_path: Path, sheet_name: Union[str, int, None] = None) -> Tuple[List[LNAAnalysisResult], DatasetSummary]:
        """
        Analyze an LNA Excel file and generate recommendations.
        
        Args:
            excel_file_path: Path to the Excel file containing LNA data
            sheet_name: Name or index of the sheet to analyze (default: first sheet)
            
        Returns:
            Tuple of (analysis_results, dataset_summary)
            
        Raises:
            LNABotError: If analysis fails
        """
        logger.info(f"Starting analysis of Excel file: {file_path} (sheet: {sheet_name or 'first'})")
        
        try:
            # Load Excel data
            df = self.data_loader.load_excel_file(file_path, sheet_name)
            
            # Validate data
            validation_errors = self.data_loader.validate_dataframe(df)
            if validation_errors:
                logger.warning(f"Data validation warnings: {validation_errors}")
            
            # Convert to LNARecord objects
            records = self.data_processor.dataframe_to_records(df)
            
            # Analyze records
            assert self.decision_engine is not None, "Decision engine not initialized"
            analysis_results, summary = self.decision_engine.analyze_dataset(records)
            
            logger.info(f"Analysis complete: {len(analysis_results)} records processed")
            
            return analysis_results, summary
            
        except Exception as e:
            logger.error(f"Excel analysis failed: {str(e)}")
            raise LNABotError(f"Excel analysis failed: {str(e)}")
    
    def analyze_file(self, file_path: Path) -> Tuple[List[LNAAnalysisResult], DatasetSummary]:
        """
        Analyze an LNA file (CSV or Excel) with automatic format detection.
        
        Args:
            file_path: Path to the file containing LNA data
            
        Returns:
            Tuple of (analysis_results, dataset_summary)
            
        Raises:
            LNABotError: If analysis fails
        """
        logger.info(f"Starting analysis of file: {file_path}")
        
        try:
            # Load file data with auto-detection (uses first sheet for Excel files)
            df = self.data_loader.load_file(file_path)
            
            # Validate data
            validation_errors = self.data_loader.validate_dataframe(df)
            if validation_errors:
                logger.warning(f"Data validation warnings: {validation_errors}")
            
            # Convert to LNARecord objects
            records = self.data_processor.dataframe_to_records(df)
            
            # Analyze records
            assert self.decision_engine is not None, "Decision engine not initialized"
            analysis_results, summary = self.decision_engine.analyze_dataset(records)
            
            logger.info(f"Analysis complete: {len(analysis_results)} records processed")
            
            return analysis_results, summary
            
        except Exception as e:
            logger.error(f"File analysis failed: {str(e)}")
            raise LNABotError(f"File analysis failed: {str(e)}")
    
    def analyze_file_with_stats(self, file_path: Path) -> Tuple[List[LNAAnalysisResult], DatasetSummary, Any]:
        """
        Analyze an LNA file with detailed processing statistics.
        
        Args:
            file_path: Path to the file containing LNA data
            
        Returns:
            Tuple of (analysis_results, dataset_summary, processing_statistics)
            
        Raises:
            LNABotError: If analysis fails
        """
        from .models import ProcessingStatistics
        
        logger.info(f"Starting analysis of file: {file_path}")
        
        try:
            # Load file data with auto-detection (uses first sheet for Excel files)
            df = self.data_loader.load_file(file_path)
            
            # Validate data
            validation_errors = self.data_loader.validate_dataframe(df)
            validation_warnings = validation_errors if validation_errors else []
            
            # Convert to LNARecord objects with statistics
            records, processing_stats = self.data_processor.dataframe_to_records_with_stats(df)
            
            # Add validation warnings to processing stats
            processing_stats.validation_warnings = validation_warnings
            
            # Analyze records
            assert self.decision_engine is not None, "Decision engine not initialized"
            analysis_results, summary = self.decision_engine.analyze_dataset(records)
            
            logger.info(f"Analysis complete: {len(analysis_results)} records processed with {processing_stats.success_rate:.1f}% success rate")
            
            return analysis_results, summary, processing_stats
            
        except Exception as e:
            logger.error(f"File analysis failed: {str(e)}")
            raise LNABotError(f"File analysis failed: {str(e)}")
    
    def analyze_single_record(self, record: LNARecord) -> LNAAnalysisResult:
        """
        Analyze a single LNA record.
        
        Args:
            record: LNA record to analyze
            
        Returns:
            Analysis result with recommendation
            
        Raises:
            LNABotError: If analysis fails
        """
        logger.info(f"Analyzing single record: {record.id}")
        
        try:
            assert self.decision_engine is not None, "Decision engine not initialized"
            result = self.decision_engine.analyze_record(record)
            logger.info(f"Single record analysis complete: {record.id}")
            return result
            
        except Exception as e:
            logger.error(f"Single record analysis failed: {str(e)}")
            raise LNABotError(f"Single record analysis failed: {str(e)}")
    
    def get_competency_skills(self, competency: str) -> List[str]:
        """
        Get the skills associated with a competency.
        
        Args:
            competency: Name of the competency
            
        Returns:
            List of associated skills
        """
        assert self.skills_mapping is not None, "Skills mapping not initialized"
        return self.skills_mapping.get_skills_for_competency(competency)
    
    def get_training_recommendation(self, estimated_trainees: int, competency: str) -> Dict[str, Any]:
        """
        Get a training recommendation for given parameters.
        
        Args:
            estimated_trainees: Number of trainees
            competency: Competency name
            
        Returns:
            Dictionary with recommendation details
        """
        try:
            # Ensure all components are initialized
            assert self.business_rules is not None, "Business rules not initialized"
            assert self.decision_engine is not None, "Decision engine not initialized"
            assert self.skills_mapping is not None, "Skills mapping not initialized"
            
            # Get competency classification
            competency_classification = self.business_rules.get_competency_classification(competency)
            
            # Determine training type
            training_type, reasoning = self.decision_engine._determine_training_type(
                estimated_trainees,
                competency_classification,
                competency
            )
            
            # Get associated skills
            associated_skills = self.skills_mapping.get_skills_for_competency(competency)
            
            return {
                'training_type': training_type,
                'reasoning': reasoning,
                'competency_classification': competency_classification,
                'associated_skills': associated_skills,
                'estimated_trainees': estimated_trainees,
                'competency': competency
            }
            
        except Exception as e:
            logger.error(f"Failed to get training recommendation: {str(e)}")
            raise LNABotError(f"Failed to get training recommendation: {str(e)}")
    
    def export_results_to_json(self, 
                              analysis_results: List[LNAAnalysisResult], 
                              summary: DatasetSummary,
                              output_file: Path) -> None:
        """
        Export analysis results to a JSON file.
        
        Args:
            analysis_results: List of analysis results
            summary: Dataset summary
            output_file: Path for the output JSON file
        """
        try:
            # Convert to dictionaries
            results_dict = self.data_processor.analysis_results_to_dict(analysis_results)
            summary_dict = self.data_processor.summary_to_dict(summary)
            
            # Create output structure
            output_data = {
                'metadata': {
                    'total_records': len(analysis_results),
                    'analysis_timestamp': summary.analysis_date.isoformat(),
                    'bot_version': '1.0.0'
                },
                'summary': summary_dict,
                'results': results_dict
            }
            
            # Write to file
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(output_data, f, indent=2, ensure_ascii=False)
            
            logger.info(f"Results exported to: {output_file}")
            
        except Exception as e:
            logger.error(f"Failed to export results: {str(e)}")
            raise LNABotError(f"Failed to export results: {str(e)}")
    
    def export_results_to_csv(self, 
                              analysis_results: List[LNAAnalysisResult], 
                              summary: DatasetSummary,
                              output_file: Path) -> None:
        """
        Export analysis results to a CSV file.
        
        Args:
            analysis_results: List of analysis results
            summary: Dataset summary
            output_file: Path for the output CSV file
        """
        try:
            import pandas as pd
            
            # Convert to dictionaries and then to DataFrame
            results_dict = self.data_processor.analysis_results_to_dict(analysis_results)
            df = pd.DataFrame(results_dict)
            
            # Reorder columns for better readability
            column_order = [
                'id', 'submission', 'priority', 'competency', 'estimated_trainees',
                'expected_training_type', 'reasoning', 'demand_score',
                'competency_classification', 'associated_skills',
                'job_families', 'targeted_audience', 'division', 'department', 'section',
                'analysis_timestamp'
            ]
            
            # Ensure all expected columns exist, add missing ones with default values
            for col in column_order:
                if col not in df.columns:
                    df[col] = None
            
            # Reorder DataFrame columns
            df = df[column_order]
            
            # Convert list columns to string representation for CSV
            if 'associated_skills' in df.columns:
                df['associated_skills'] = df['associated_skills'].apply(
                    lambda x: '; '.join(x) if isinstance(x, list) else str(x) if x else ''
                )
            
            # Export to CSV
            df.to_csv(output_file, index=False, encoding='utf-8')
            
            logger.info(f"Results exported to CSV: {output_file}")
            
        except Exception as e:
            logger.error(f"Failed to export CSV results: {str(e)}")
            raise LNABotError(f"Failed to export CSV results: {str(e)}")
    
    def export_results_to_excel(self, 
                                analysis_results: List[LNAAnalysisResult], 
                                summary: DatasetSummary,
                                output_file: Path) -> None:
        """
        Export analysis results to an Excel file with multiple sheets.
        
        Args:
            analysis_results: List of analysis results
            summary: Dataset summary
            output_file: Path for the output Excel file
        """
        try:
            import pandas as pd
            
            # Check if openpyxl is available for Excel export
            try:
                import openpyxl
            except ImportError:
                raise ImportError(
                    "openpyxl is required for Excel export. "
                    "Install it with: pip install openpyxl>=3.0.0"
                )
            
            # Convert to dictionaries and then to DataFrame
            results_dict = self.data_processor.analysis_results_to_dict(analysis_results)
            df = pd.DataFrame(results_dict)
            
            # Reorder columns for better readability
            column_order = [
                'id', 'submission', 'priority', 'competency', 'estimated_trainees',
                'expected_training_type', 'reasoning', 'demand_score',
                'competency_classification', 'associated_skills',
                'job_families', 'targeted_audience', 'division', 'department', 'section',
                'analysis_timestamp'
            ]
            
            # Ensure all expected columns exist
            for col in column_order:
                if col not in df.columns:
                    df[col] = None
            
            # Reorder DataFrame columns
            df = df[column_order]
            
            # Convert list columns to string representation for Excel
            if 'associated_skills' in df.columns:
                df['associated_skills'] = df['associated_skills'].apply(
                    lambda x: '; '.join(x) if isinstance(x, list) else str(x) if x else ''
                )
            
            # Create summary DataFrame
            summary_dict = self.data_processor.summary_to_dict(summary)
            summary_data = []
            for key, value in summary_dict.items():
                if key == 'training_type_distribution' and isinstance(value, dict):
                    for training_type, count in value.items():
                        summary_data.append({'Metric': f'Training Type - {training_type}', 'Value': count})
                elif key == 'priority_distribution' and isinstance(value, dict):
                    for priority, count in value.items():
                        summary_data.append({'Metric': f'Priority - {priority}', 'Value': count})
                elif key == 'competency_classification_distribution' and isinstance(value, dict):
                    for classification, count in value.items():
                        summary_data.append({'Metric': f'Competency - {classification}', 'Value': count})
                else:
                    summary_data.append({'Metric': key.replace('_', ' ').title(), 'Value': value})
            
            summary_df = pd.DataFrame(summary_data)
            
            # Export to Excel with multiple sheets
            with pd.ExcelWriter(output_file, engine='openpyxl') as writer:
                # Main results sheet
                df.to_excel(writer, sheet_name='Analysis Results', index=False)
                
                # Summary sheet
                summary_df.to_excel(writer, sheet_name='Summary', index=False)
                
                # Training type breakdown sheet
                if 'expected_training_type' in df.columns:
                    training_breakdown = df.groupby('expected_training_type').agg({
                        'id': 'count',
                        'estimated_trainees': 'sum',
                        'demand_score': 'mean'
                    }).round(2)
                    training_breakdown.columns = ['Record Count', 'Total Trainees', 'Avg Demand Score']
                    training_breakdown.to_excel(writer, sheet_name='Training Type Breakdown')
                
                # Competency analysis sheet
                if 'competency' in df.columns:
                    competency_stats = df.groupby('competency').agg({
                        'id': 'count',
                        'estimated_trainees': 'sum',
                        'demand_score': 'mean',
                        'expected_training_type': lambda x: x.mode().iloc[0] if not x.empty else 'N/A'
                    }).round(2)
                    competency_stats.columns = ['Record Count', 'Total Trainees', 'Avg Demand Score', 'Most Common Training Type']
                    competency_stats.to_excel(writer, sheet_name='Competency Analysis')
            
            logger.info(f"Results exported to Excel: {output_file}")
            
        except Exception as e:
            logger.error(f"Failed to export Excel results: {str(e)}")
            raise LNABotError(f"Failed to export Excel results: {str(e)}")
    
    def export_results(self, 
                      analysis_results: List[LNAAnalysisResult], 
                      summary: DatasetSummary,
                      output_file: Path,
                      format_type: str = 'json') -> None:
        """
        Export analysis results to specified format (json, csv, or excel).
        
        Args:
            analysis_results: List of analysis results
            summary: Dataset summary
            output_file: Path for the output file
            format_type: Export format ('json', 'csv', or 'excel')
        """
        format_type = format_type.lower()
        
        if format_type == 'json':
            self.export_results_to_json(analysis_results, summary, output_file)
        elif format_type == 'csv':
            self.export_results_to_csv(analysis_results, summary, output_file)
        elif format_type == 'excel':
            self.export_results_to_excel(analysis_results, summary, output_file)
        else:
            raise LNABotError(f"Unsupported export format: {format_type}. Supported formats: json, csv, excel")
    
    def get_summary_report(self, summary: DatasetSummary) -> str:
        """
        Generate a formatted summary report.
        
        Args:
            summary: Dataset summary
            
        Returns:
            Formatted summary report as string
        """
        return self.data_processor.create_summary_table(summary)
    
    def get_business_rules_info(self) -> Dict[str, Any]:
        """
        Get information about the current business rules configuration.
        
        Returns:
            Dictionary with business rules information
        """
        assert self.business_rules is not None, "Business rules not initialized"
        assert self.skills_mapping is not None, "Skills mapping not initialized"
        
        return {
            'external_threshold': self.business_rules.external_threshold,
            'in_house_threshold': self.business_rules.in_house_threshold,
            'priority_weights': self.business_rules.priority_weights,
            'niche_competencies_count': len(self.business_rules.niche_competencies),
            'common_competencies_count': len(self.business_rules.common_competencies),
            'total_skills_mapped': len(self.skills_mapping.competency_skills)
        }
    
    def validate_configuration(self) -> List[str]:
        """
        Validate the current configuration and return any issues.
        
        Returns:
            List of validation issues (empty if all valid)
        """
        issues = []
        
        # Check business rules
        if not self.business_rules:
            issues.append("Business rules not loaded")
        else:
            if self.business_rules.external_threshold >= self.business_rules.in_house_threshold:
                issues.append("External threshold should be less than in-house threshold")
        
        # Check skills mapping
        if not self.skills_mapping:
            issues.append("Skills mapping not loaded")
        else:
            if not self.skills_mapping.competency_skills:
                issues.append("No skills mapping data found")
        
        # Check competency classifications
        if self.business_rules:
            total_competencies = (len(self.business_rules.niche_competencies) + 
                                len(self.business_rules.common_competencies))
            if total_competencies == 0:
                issues.append("No competency classifications found")
        
        return issues