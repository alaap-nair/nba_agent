#!/usr/bin/env python3
"""
Input validation and sanitization for NBA Agent
Provides robust validation for user inputs, API responses, and data integrity
"""

import re
import html
from typing import Optional, Dict, Any, List
from dataclasses import dataclass
from enum import Enum

class ValidationError(Exception):
    """Custom exception for validation errors"""
    pass

class SeasonFormat(Enum):
    """Valid NBA season formats"""
    CURRENT = "2024-25"
    PREVIOUS = "2023-24"
    OLDER = r"^\d{4}-\d{2}$"

@dataclass
class ValidationResult:
    """Result of a validation check"""
    is_valid: bool
    cleaned_value: Any = None
    error_message: Optional[str] = None
    warnings: List[str] = None
    
    def __post_init__(self):
        if self.warnings is None:
            self.warnings = []

class InputValidator:
    """Comprehensive input validation for NBA Agent"""
    
    # Valid NBA team abbreviations
    VALID_TEAM_ABBREVS = {
        'ATL', 'BOS', 'BKN', 'CHA', 'CHI', 'CLE', 'DAL', 'DEN', 'DET', 'GSW',
        'HOU', 'IND', 'LAC', 'LAL', 'MEM', 'MIA', 'MIL', 'MIN', 'NOP', 'NYK',
        'OKC', 'ORL', 'PHI', 'PHX', 'POR', 'SAC', 'SAS', 'TOR', 'UTA', 'WAS'
    }
    
    # Common player name patterns to watch for
    SUSPICIOUS_PATTERNS = [
        r'<script.*?>',     # XSS attempts
        r'javascript:',     # JavaScript injection
        r'[<>"\']',         # HTML/SQL injection characters
        # Match SQL injection patterns like ';', '|', or '--' without blocking
        # legitimate hyphenated inputs (e.g., seasons like 2024-25)
        r';',
        r'\|',
        r'--',
        r'union\s+select',  # SQL injection
        r'drop\s+table',    # SQL injection
    ]
    
    @staticmethod
    def sanitize_string(value: str, max_length: int = 100) -> ValidationResult:
        """
        Sanitize and validate string input
        
        Args:
            value: Input string to sanitize
            max_length: Maximum allowed length
            
        Returns:
            ValidationResult with cleaned string
        """
        if not isinstance(value, str):
            return ValidationResult(
                is_valid=False,
                error_message="Input must be a string"
            )
        
        # Basic sanitization
        cleaned = value.strip()
        
        # Check length
        if len(cleaned) == 0:
            return ValidationResult(
                is_valid=False,
                error_message="Input cannot be empty"
            )
        
        if len(cleaned) > max_length:
            return ValidationResult(
                is_valid=False,
                error_message=f"Input too long (max {max_length} characters)"
            )
        
        # Check for suspicious patterns
        for pattern in InputValidator.SUSPICIOUS_PATTERNS:
            if re.search(pattern, cleaned, re.IGNORECASE):
                return ValidationResult(
                    is_valid=False,
                    error_message="Input contains invalid characters"
                )
        
        # HTML escape for safety
        cleaned = html.escape(cleaned)
        
        return ValidationResult(
            is_valid=True,
            cleaned_value=cleaned
        )
    
    @staticmethod
    def validate_player_name(name: str) -> ValidationResult:
        """
        Validate NBA player name input
        
        Args:
            name: Player name to validate
            
        Returns:
            ValidationResult with cleaned player name
        """
        result = InputValidator.sanitize_string(name, max_length=50)
        if not result.is_valid:
            return result
        
        cleaned_name = result.cleaned_value
        
        # Check for valid name pattern (letters, spaces, hyphens, apostrophes)
        if not re.match(r"^[A-Za-z\s\-'\.]+$", cleaned_name):
            return ValidationResult(
                is_valid=False,
                error_message="Player name contains invalid characters"
            )
        
        # Check for reasonable name length
        if len(cleaned_name.split()) > 4:
            return ValidationResult(
                is_valid=False,
                error_message="Player name has too many parts"
            )
        
        # Normalize capitalization
        cleaned_name = ' '.join(word.capitalize() for word in cleaned_name.split())
        
        return ValidationResult(
            is_valid=True,
            cleaned_value=cleaned_name
        )
    
    @staticmethod
    def validate_team_name(name: str) -> ValidationResult:
        """
        Validate NBA team name input
        
        Args:
            name: Team name to validate
            
        Returns:
            ValidationResult with cleaned team name
        """
        result = InputValidator.sanitize_string(name, max_length=50)
        if not result.is_valid:
            return result
        
        cleaned_name = result.cleaned_value
        
        # Check if it's a valid abbreviation
        if cleaned_name.upper() in InputValidator.VALID_TEAM_ABBREVS:
            return ValidationResult(
                is_valid=True,
                cleaned_value=cleaned_name.upper()
            )
        
        # Check for valid team name pattern
        if not re.match(r"^[A-Za-z\s\-]+$", cleaned_name):
            return ValidationResult(
                is_valid=False,
                error_message="Team name contains invalid characters"
            )
        
        # Normalize capitalization
        cleaned_name = ' '.join(word.capitalize() for word in cleaned_name.split())
        
        return ValidationResult(
            is_valid=True,
            cleaned_value=cleaned_name
        )
    
    @staticmethod
    def validate_season(season: str) -> ValidationResult:
        """
        Validate NBA season format
        
        Args:
            season: Season string (e.g., "2024-25")
            
        Returns:
            ValidationResult with validated season
        """
        result = InputValidator.sanitize_string(season, max_length=10)
        if not result.is_valid:
            return result
        
        cleaned_season = result.cleaned_value.replace("&hyphen;", "-")  # Unescape hyphen
        
        # Check season format
        if not re.match(r"^\d{4}-\d{2}$", cleaned_season):
            return ValidationResult(
                is_valid=False,
                error_message="Season must be in format YYYY-YY (e.g., 2024-25)"
            )
        
        # Validate year range (NBA started in 1946)
        start_year = int(cleaned_season[:4])
        end_year = int(f"20{cleaned_season[-2:]}")
        
        if start_year < 1946:
            return ValidationResult(
                is_valid=False,
                error_message="NBA seasons start from 1946"
            )
        
        if start_year > 2030:  # Reasonable future limit
            return ValidationResult(
                is_valid=False,
                error_message="Season year is too far in the future"
            )
        
        if end_year != start_year + 1:
            return ValidationResult(
                is_valid=False,
                error_message="Season format is invalid (must be consecutive years)"
            )
        
        return ValidationResult(
            is_valid=True,
            cleaned_value=cleaned_season
        )
    
    @staticmethod
    def validate_stat_type(stat_type: str) -> ValidationResult:
        """
        Validate NBA statistic type
        
        Args:
            stat_type: Statistic type to validate
            
        Returns:
            ValidationResult with validated stat type
        """
        valid_stats = {
            'points', 'ppg', 'assists', 'apg', 'rebounds', 'rpg',
            'steals', 'spg', 'blocks', 'bpg', 'fg%', 'fg_pct',
            '3p%', 'fg3_pct', 'ft%', 'ft_pct', 'all', 'everything'
        }
        
        result = InputValidator.sanitize_string(stat_type, max_length=20)
        if not result.is_valid:
            return result
        
        cleaned_stat = result.cleaned_value.lower()
        
        if cleaned_stat not in valid_stats:
            return ValidationResult(
                is_valid=False,
                error_message=f"Invalid stat type. Valid options: {', '.join(sorted(valid_stats))}"
            )
        
        return ValidationResult(
            is_valid=True,
            cleaned_value=cleaned_stat
        )
    
    @staticmethod
    def validate_query(query: str) -> ValidationResult:
        """
        Validate general user query
        
        Args:
            query: User query to validate
            
        Returns:
            ValidationResult with cleaned query
        """
        result = InputValidator.sanitize_string(query, max_length=500)
        if not result.is_valid:
            return result
        
        cleaned_query = result.cleaned_value
        
        # Check for minimum meaningful length
        if len(cleaned_query.split()) < 2:
            return ValidationResult(
                is_valid=False,
                error_message="Query too short - please provide more details"
            )
        
        return ValidationResult(
            is_valid=True,
            cleaned_value=cleaned_query
        )

class ResponseValidator:
    """Validate API responses and data integrity"""
    
    @staticmethod
    def validate_player_stats(data: Dict[str, Any]) -> ValidationResult:
        """
        Validate player statistics response
        
        Args:
            data: Player statistics dictionary
            
        Returns:
            ValidationResult indicating if stats are valid
        """
        required_fields = ['player', 'season', 'stats']
        
        for field in required_fields:
            if field not in data:
                return ValidationResult(
                    is_valid=False,
                    error_message=f"Missing required field: {field}"
                )
        
        # Validate stats are numeric and reasonable
        if 'stats' in data and isinstance(data['stats'], dict):
            for stat_name, stat_value in data['stats'].items():
                if isinstance(stat_value, (int, float)):
                    # Check for reasonable ranges
                    if stat_name in ['ppg', 'apg', 'rpg'] and stat_value < 0:
                        return ValidationResult(
                            is_valid=False,
                            error_message=f"Invalid {stat_name}: cannot be negative"
                        )
                    
                    if stat_name in ['ppg'] and stat_value > 100:
                        return ValidationResult(
                            is_valid=False,
                            error_message="PPG seems unreasonably high",
                            warnings=["PPG over 100 is extremely unusual"]
                        )
        
        return ValidationResult(is_valid=True, cleaned_value=data)
    
    @staticmethod
    def validate_team_data(data: Dict[str, Any]) -> ValidationResult:
        """
        Validate team-related response data
        
        Args:
            data: Team data dictionary
            
        Returns:
            ValidationResult indicating if team data is valid
        """
        if 'team' not in data:
            return ValidationResult(
                is_valid=False,
                error_message="Missing team information"
            )
        
        # Validate team name
        team_result = InputValidator.validate_team_name(data['team'])
        if not team_result.is_valid:
            return ValidationResult(
                is_valid=False,
                error_message=f"Invalid team name: {team_result.error_message}"
            )
        
        return ValidationResult(is_valid=True, cleaned_value=data)

# Convenience functions for common validations
def safe_validate_input(validator_func, value: Any, default_error: str = "Invalid input") -> Any:
    """
    Safely validate input with error handling
    
    Args:
        validator_func: Validation function to call
        value: Value to validate
        default_error: Default error message if validation fails
        
    Returns:
        Cleaned value if valid, raises ValidationError if invalid
    """
    try:
        result = validator_func(value)
        if result.is_valid:
            return result.cleaned_value
        else:
            raise ValidationError(result.error_message or default_error)
    except Exception as e:
        raise ValidationError(f"{default_error}: {str(e)}")

# Export main classes and functions
__all__ = [
    'ValidationError',
    'ValidationResult',
    'InputValidator',
    'ResponseValidator',
    'safe_validate_input'
] 