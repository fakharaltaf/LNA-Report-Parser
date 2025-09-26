"""
Configuration loader for LNA Bot.

This module handles loading business rules, skills mappings, and competency
classifications from various sources (files, databases, etc.).
"""

import json
import logging
from pathlib import Path
from typing import Dict, List, Any, Optional, Union
import pandas as pd

from ..models import BusinessRules, SkillsMapping, PriorityLevel

logger = logging.getLogger(__name__)


class ConfigurationError(Exception):
    """Raised when there's an error in configuration loading or validation."""
    pass


class ConfigurationLoader:
    """
    Loads and manages configuration data for the LNA Bot.
    
    This class provides methods to load business rules, skills mappings,
    and competency classifications from various sources.
    """
    
    def __init__(self, config_dir: Optional[Path] = None):
        """
        Initialize the configuration loader.
        
        Args:
            config_dir: Directory containing configuration files
        """
        self.config_dir = config_dir or Path("Testing/Configuration")
        logger.info(f"Configuration loader initialized with directory: {self.config_dir}")
    
    def load_business_rules(self) -> BusinessRules:
        """
        Load business rules from configuration files.
        
        Returns:
            BusinessRules object with loaded configuration
            
        Raises:
            ConfigurationError: If configuration cannot be loaded or is invalid
        """
        try:
            # Load competency classifications
            niche_competencies, common_competencies = self._load_competency_classifications()
            
            # Create business rules with default thresholds and loaded classifications
            business_rules = BusinessRules(
                external_threshold=10,
                in_house_threshold=50,
                priority_weights={
                    PriorityLevel.HIGH: 3,
                    PriorityLevel.MEDIUM: 2,
                    PriorityLevel.LOW: 1
                },
                niche_competencies=niche_competencies,
                common_competencies=common_competencies
            )
            
            logger.info(f"Business rules loaded: {len(niche_competencies)} niche, "
                       f"{len(common_competencies)} common competencies")
            
            return business_rules
            
        except Exception as e:
            logger.error(f"Failed to load business rules: {str(e)}")
            raise ConfigurationError(f"Failed to load business rules: {str(e)}")
    
    def load_skills_mapping(self) -> SkillsMapping:
        """
        Load skills mapping from configuration files.
        
        Returns:
            SkillsMapping object with competency-to-skills mappings
            
        Raises:
            ConfigurationError: If skills mapping cannot be loaded
        """
        try:
            skills_file = self.config_dir / "skills_mapping.md"
            
            if not skills_file.exists():
                logger.warning(f"Skills mapping file not found: {skills_file}")
                return SkillsMapping()
            
            # Parse the Markdown skills mapping file
            competency_skills = self._parse_skills_mapping_file(skills_file)
            
            skills_mapping = SkillsMapping(competency_skills=competency_skills)
            
            logger.info(f"Skills mapping loaded: {len(competency_skills)} competencies")
            
            return skills_mapping
            
        except Exception as e:
            logger.error(f"Failed to load skills mapping: {str(e)}")
            raise ConfigurationError(f"Failed to load skills mapping: {str(e)}")
    
    def _load_competency_classifications(self) -> tuple[List[str], List[str]]:
        """
        Load competency classifications from the classification file.
        
        Returns:
            Tuple of (niche_competencies, common_competencies)
        """
        classification_file = self.config_dir / "competency_classification.md"
        
        if not classification_file.exists():
            logger.warning(f"Competency classification file not found: {classification_file}")
            return [], []
        
        niche_competencies = []
        common_competencies = []
        
        with open(classification_file, 'r', encoding='utf-8') as f:
            content = f.read()
            
            # Parse niche competencies
            niche_section = self._extract_section(content, "## Niche Competencies")
            niche_competencies = self._extract_competency_names(niche_section)
            
            # Parse common competencies
            common_section = self._extract_section(content, "## Common Competencies")
            common_competencies = self._extract_competency_names(common_section)
        
        return niche_competencies, common_competencies
    
    def _parse_skills_mapping_file(self, file_path: Path) -> Dict[str, List[str]]:
        """
        Parse the skills mapping Markdown file.
        
        Args:
            file_path: Path to the skills mapping file
            
        Returns:
            Dictionary mapping competency names to skill lists
        """
        competency_skills = {}
        
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Split content into sections by ### headers (competency names)
        sections = content.split('### ')
        
        for section in sections[1:]:  # Skip the first empty section
            lines = section.strip().split('\n')
            if not lines:
                continue
                
            # First line is the competency name
            competency_name = lines[0].strip()
            
            # Extract skills (lines starting with -)
            skills = []
            for line in lines[1:]:
                line = line.strip()
                if line.startswith('- '):
                    skill = line[2:].strip()  # Remove '- ' prefix
                    if skill:
                        skills.append(skill)
            
            if skills:
                competency_skills[competency_name] = skills
        
        return competency_skills
    
    def _extract_section(self, content: str, section_header: str) -> str:
        """
        Extract a section from markdown content.
        
        Args:
            content: Full markdown content
            section_header: Header to look for (e.g., "## Niche Competencies")
            
        Returns:
            Content of the section
        """
        lines = content.split('\n')
        section_lines = []
        in_section = False
        
        for line in lines:
            if line.strip() == section_header:
                in_section = True
                continue
            elif line.startswith('## ') and in_section:
                # Start of next section
                break
            elif in_section:
                section_lines.append(line)
        
        return '\n'.join(section_lines)
    
    def _extract_competency_names(self, section_content: str) -> List[str]:
        """
        Extract competency names from a section.
        
        Args:
            section_content: Content of a classification section
            
        Returns:
            List of competency names
        """
        competencies = []
        lines = section_content.split('\n')
        
        for line in lines:
            line = line.strip()
            if line.startswith('- '):
                competency = line[2:].strip()  # Remove '- ' prefix
                if competency and not competency.startswith('#'):  # Skip comments
                    competencies.append(competency)
        
        return competencies


class DataLoader:
    """
    Handles loading and parsing of LNA data from various sources.
    
    This class provides methods to load LNA records from CSV files,
    databases, or other data sources.
    """
    
    def __init__(self):
        """Initialize the data loader."""
        logger.info("Data loader initialized")
    
    def load_csv_file(self, file_path: Path) -> pd.DataFrame:
        """
        Load LNA data from a CSV file.
        
        Args:
            file_path: Path to the CSV file
            
        Returns:
            DataFrame containing the LNA data
            
        Raises:
            FileNotFoundError: If the CSV file doesn't exist
            ValueError: If the CSV file has invalid format
        """
        if not file_path.exists():
            raise FileNotFoundError(f"CSV file not found: {file_path}")
        
        try:
            # Load CSV with proper column names
            df = pd.read_csv(file_path)
            
            # Validate required columns
            required_columns = [
                'ID', 'Submission', 'Priority', 'Competency type', 'Job families',
                'Targeted competencies', 'Request type', 'Targeted audience',
                'Estimated trainees', 'Comment', 'Year', 'Division', 'Department', 'Section'
            ]
            
            missing_columns = [col for col in required_columns if col not in df.columns]
            if missing_columns:
                raise ValueError(f"Missing required columns: {missing_columns}")
            
            # Basic data validation
            if df.empty:
                raise ValueError("CSV file is empty")
            
            # Check for required non-null columns
            critical_columns = ['ID', 'Priority', 'Targeted competencies', 'Estimated trainees']
            for col in critical_columns:
                if df[col].isnull().any():
                    raise ValueError(f"Column '{col}' contains null values")
            
            logger.info(f"Successfully loaded CSV file: {file_path} ({len(df)} records)")
            
            return df
            
        except pd.errors.EmptyDataError:
            raise ValueError(f"CSV file is empty: {file_path}")
        except pd.errors.ParserError as e:
            raise ValueError(f"Error parsing CSV file: {str(e)}")
        except Exception as e:
            logger.error(f"Failed to load CSV file {file_path}: {str(e)}")
            raise ValueError(f"Failed to load CSV file: {str(e)}")
    
    def load_excel_file(self, file_path: Path, sheet_name: Union[str, int, None] = None) -> pd.DataFrame:
        """
        Load LNA data from an Excel file.
        
        Args:
            file_path: Path to the Excel file
            sheet_name: Name or index of the sheet to load (default: first sheet)
            
        Returns:
            DataFrame containing the LNA data
            
        Raises:
            FileNotFoundError: If the Excel file doesn't exist
            ValueError: If the Excel file has invalid format
            ImportError: If openpyxl is not installed
        """
        if not file_path.exists():
            raise FileNotFoundError(f"Excel file not found: {file_path}")
        
        try:
            # Check if openpyxl is available
            try:
                import openpyxl
            except ImportError:
                raise ImportError(
                    "openpyxl is required for Excel file support. "
                    "Install it with: pip install openpyxl>=3.0.0"
                )
            
            # Load Excel file with proper handling
            df = pd.read_excel(file_path, sheet_name=sheet_name or 0)
            
            # Apply same validation as CSV files
            required_columns = [
                'ID', 'Submission', 'Priority', 'Competency type', 'Job families',
                'Targeted competencies', 'Request type', 'Targeted audience',
                'Estimated trainees', 'Comment', 'Year', 'Division', 'Department', 'Section'
            ]
            
            missing_columns = [col for col in required_columns if col not in df.columns]
            if missing_columns:
                raise ValueError(f"Missing required columns: {missing_columns}")
            
            # Basic data validation
            if df.empty:
                raise ValueError("Excel file is empty")
            
            # Check for required non-null columns
            critical_columns = ['ID', 'Priority', 'Targeted competencies', 'Estimated trainees']
            for col in critical_columns:
                if df[col].isnull().any():
                    raise ValueError(f"Column '{col}' contains null values")
            
            logger.info(f"Successfully loaded Excel file: {file_path} ({len(df)} records)")
            
            return df
            
        except pd.errors.EmptyDataError:
            raise ValueError(f"Excel file is empty: {file_path}")
        except Exception as e:
            logger.error(f"Failed to load Excel file {file_path}: {str(e)}")
            raise ValueError(f"Failed to load Excel file: {str(e)}")
    
    def _detect_file_type(self, file_path: Path) -> str:
        """
        Detect file type based on file extension.
        
        Args:
            file_path: Path to the file
            
        Returns:
            File type string ('csv', 'excel')
            
        Raises:
            ValueError: If file type is not supported
        """
        suffix = file_path.suffix.lower()
        if suffix == '.csv':
            return 'csv'
        elif suffix in ['.xlsx', '.xls', '.xlsm']:
            return 'excel'
        else:
            raise ValueError(f"Unsupported file format: {suffix}. Supported formats: .csv, .xlsx, .xls, .xlsm")
    
    def load_file(self, file_path: Path, sheet_name: str = None) -> pd.DataFrame:
        """
        Universal file loader with automatic format detection.
        
        Args:
            file_path: Path to the file (CSV or Excel)
            sheet_name: Name or index of Excel sheet (ignored for CSV files)
            
        Returns:
            DataFrame containing the LNA data
            
        Raises:
            FileNotFoundError: If the file doesn't exist
            ValueError: If the file format is unsupported or invalid
        """
        file_type = self._detect_file_type(file_path)
        
        if file_type == 'csv':
            return self.load_csv_file(file_path)
        elif file_type == 'excel':
            return self.load_excel_file(file_path, sheet_name)
        else:
            raise ValueError(f"Unsupported file type: {file_type}")
    
    def validate_dataframe(self, df: pd.DataFrame) -> List[str]:
        """
        Validate a DataFrame containing LNA data.
        
        Args:
            df: DataFrame to validate
            
        Returns:
            List of validation error messages (empty if valid)
        """
        errors = []
        
        # Check estimated trainees are positive integers
        if 'Estimated trainees' in df.columns:
            invalid_trainees = df[df['Estimated trainees'] <= 0]
            if not invalid_trainees.empty:
                errors.append(f"Found {len(invalid_trainees)} records with invalid trainee counts")
        
        # Check priority values
        if 'Priority' in df.columns:
            valid_priorities = ['High', 'Medium', 'Low']
            invalid_priorities = df[~df['Priority'].isin(valid_priorities)]
            if not invalid_priorities.empty:
                errors.append(f"Found {len(invalid_priorities)} records with invalid priority levels")
        
        # Check for duplicate IDs
        if 'ID' in df.columns:
            duplicate_ids = df[df['ID'].duplicated()]
            if not duplicate_ids.empty:
                errors.append(f"Found {len(duplicate_ids)} records with duplicate IDs")
        
        return errors