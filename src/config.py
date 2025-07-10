#!/usr/bin/env python3
"""
Configuration management for NBA Agent
Centralized configuration with environment variables and sensible defaults
"""

import os
from typing import Optional, Dict, Any
from dataclasses import dataclass, field
from pathlib import Path

@dataclass
class APIConfig:
    """API-related configuration"""
    openai_api_key: str = ""
    judgment_api_key: Optional[str] = None
    judgment_org_id: Optional[str] = None
    request_timeout: int = 30
    max_retries: int = 3
    rate_limit_per_minute: int = 100
    max_concurrent_requests: int = 10

@dataclass
class CacheConfig:
    """Cache-related configuration"""
    ttl_seconds: int = 3600  # 1 hour default
    cache_dir: str = "cache"
    max_cache_size_mb: int = 100
    enable_memory_cache: bool = True
    enable_disk_cache: bool = True

@dataclass
class LoggingConfig:
    """Logging configuration"""
    level: str = "INFO"
    format: str = "colored"  # "colored" or "json"
    log_file: Optional[str] = None
    max_log_file_size_mb: int = 10
    log_rotation_count: int = 5

@dataclass
class SecurityConfig:
    """Security-related configuration"""
    enable_input_validation: bool = True
    enable_rate_limiting: bool = True
    max_query_length: int = 500
    max_player_name_length: int = 50
    max_team_name_length: int = 50
    enable_request_sanitization: bool = True

@dataclass
class PerformanceConfig:
    """Performance tuning configuration"""
    enable_async: bool = False
    connection_pool_size: int = 10
    enable_compression: bool = True
    query_timeout_seconds: int = 30
    enable_performance_monitoring: bool = True

@dataclass
class StreamlitConfig:
    """Streamlit-specific configuration"""
    server_port: int = 8501
    server_address: str = "localhost"
    max_upload_size_mb: int = 200
    enable_cors: bool = False
    theme: str = "dark"

@dataclass
class NBAAgentConfig:
    """Main configuration class for NBA Agent"""
    # Sub-configurations
    api: APIConfig = field(default_factory=APIConfig)
    cache: CacheConfig = field(default_factory=CacheConfig)
    logging: LoggingConfig = field(default_factory=LoggingConfig)
    security: SecurityConfig = field(default_factory=SecurityConfig)
    performance: PerformanceConfig = field(default_factory=PerformanceConfig)
    streamlit: StreamlitConfig = field(default_factory=StreamlitConfig)
    
    # General settings
    debug: bool = False
    development_mode: bool = False
    testing: bool = False
    environment: str = "production"

def load_config() -> NBAAgentConfig:
    """
    Load configuration from environment variables with fallback to defaults
    
    Returns:
        NBAAgentConfig instance with loaded configuration
    """
    config = NBAAgentConfig()
    
    # API Configuration
    config.api.openai_api_key = os.getenv("OPENAI_API_KEY", "")
    config.api.judgment_api_key = os.getenv("JUDGMENT_API_KEY")
    config.api.judgment_org_id = os.getenv("JUDGMENT_ORG_ID")
    config.api.request_timeout = int(os.getenv("NBA_AGENT_REQUEST_TIMEOUT", "30"))
    config.api.max_retries = int(os.getenv("NBA_AGENT_MAX_RETRIES", "3"))
    config.api.rate_limit_per_minute = int(os.getenv("NBA_AGENT_RATE_LIMIT", "100"))
    config.api.max_concurrent_requests = int(os.getenv("NBA_AGENT_MAX_CONCURRENT", "10"))
    
    # Cache Configuration
    config.cache.ttl_seconds = int(os.getenv("NBA_AGENT_CACHE_TTL", "3600"))
    config.cache.cache_dir = os.getenv("NBA_AGENT_CACHE_DIR", "cache")
    config.cache.max_cache_size_mb = int(os.getenv("NBA_AGENT_MAX_CACHE_SIZE_MB", "100"))
    config.cache.enable_memory_cache = os.getenv("NBA_AGENT_ENABLE_MEMORY_CACHE", "true").lower() == "true"
    config.cache.enable_disk_cache = os.getenv("NBA_AGENT_ENABLE_DISK_CACHE", "true").lower() == "true"
    
    # Logging Configuration
    config.logging.level = os.getenv("NBA_AGENT_LOG_LEVEL", "INFO").upper()
    config.logging.format = os.getenv("LOG_FORMAT", "colored")
    config.logging.log_file = os.getenv("NBA_AGENT_LOG_FILE")
    config.logging.max_log_file_size_mb = int(os.getenv("NBA_AGENT_MAX_LOG_SIZE_MB", "10"))
    config.logging.log_rotation_count = int(os.getenv("NBA_AGENT_LOG_ROTATION_COUNT", "5"))
    
    # Security Configuration
    config.security.enable_input_validation = os.getenv("NBA_AGENT_ENABLE_VALIDATION", "true").lower() == "true"
    config.security.enable_rate_limiting = os.getenv("API_RATE_LIMIT_ENABLED", "true").lower() == "true"
    config.security.max_query_length = int(os.getenv("NBA_AGENT_MAX_QUERY_LENGTH", "500"))
    config.security.max_player_name_length = int(os.getenv("NBA_AGENT_MAX_PLAYER_NAME_LENGTH", "50"))
    config.security.max_team_name_length = int(os.getenv("NBA_AGENT_MAX_TEAM_NAME_LENGTH", "50"))
    config.security.enable_request_sanitization = os.getenv("NBA_AGENT_ENABLE_SANITIZATION", "true").lower() == "true"
    
    # Performance Configuration
    config.performance.enable_async = os.getenv("NBA_AGENT_ENABLE_ASYNC", "false").lower() == "true"
    config.performance.connection_pool_size = int(os.getenv("NBA_AGENT_POOL_SIZE", "10"))
    config.performance.enable_compression = os.getenv("NBA_AGENT_ENABLE_COMPRESSION", "true").lower() == "true"
    config.performance.query_timeout_seconds = int(os.getenv("NBA_AGENT_QUERY_TIMEOUT", "30"))
    config.performance.enable_performance_monitoring = os.getenv("NBA_AGENT_ENABLE_MONITORING", "true").lower() == "true"
    
    # Streamlit Configuration
    config.streamlit.server_port = int(os.getenv("STREAMLIT_SERVER_PORT", "8501"))
    config.streamlit.server_address = os.getenv("STREAMLIT_SERVER_ADDRESS", "localhost")
    config.streamlit.max_upload_size_mb = int(os.getenv("STREAMLIT_MAX_UPLOAD_SIZE_MB", "200"))
    config.streamlit.enable_cors = os.getenv("STREAMLIT_ENABLE_CORS", "false").lower() == "true"
    config.streamlit.theme = os.getenv("STREAMLIT_THEME", "dark")
    
    # General Settings
    config.debug = os.getenv("DEBUG", "false").lower() == "true"
    config.development_mode = os.getenv("DEVELOPMENT_MODE", "false").lower() == "true"
    config.testing = os.getenv("TESTING", "false").lower() == "true"
    config.environment = os.getenv("ENVIRONMENT", "production")
    
    return config

def validate_config(config: NBAAgentConfig) -> Dict[str, Any]:
    """
    Validate configuration and return validation results
    
    Args:
        config: Configuration to validate
        
    Returns:
        Dictionary with validation results
    """
    errors = []
    warnings = []
    
    # Check required settings
    if not config.api.openai_api_key:
        errors.append("OPENAI_API_KEY is required")
    
    # Check cache directory exists or can be created
    cache_path = Path(config.cache.cache_dir)
    if not cache_path.exists():
        try:
            cache_path.mkdir(parents=True, exist_ok=True)
        except Exception as e:
            errors.append(f"Cannot create cache directory: {e}")
    
    # Check log level is valid
    valid_log_levels = {"DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"}
    if config.logging.level not in valid_log_levels:
        warnings.append(f"Invalid log level '{config.logging.level}', using INFO")
        config.logging.level = "INFO"
    
    # Check reasonable timeout values
    if config.api.request_timeout < 1 or config.api.request_timeout > 300:
        warnings.append("Request timeout should be between 1 and 300 seconds")
    
    if config.cache.ttl_seconds < 60:
        warnings.append("Cache TTL less than 60 seconds may cause excessive API calls")
    
    # Check port availability for Streamlit
    if config.streamlit.server_port < 1024 or config.streamlit.server_port > 65535:
        warnings.append("Streamlit port should be between 1024 and 65535")
    
    return {
        "is_valid": len(errors) == 0,
        "errors": errors,
        "warnings": warnings
    }

def create_env_template() -> str:
    """
    Create a template .env file content with all available options
    
    Returns:
        String content for .env.example file
    """
    template = """# NBA Agent Environment Configuration
# Copy this file to .env and fill in your actual values

# ============================================================================
# REQUIRED CONFIGURATION
# ============================================================================

# OpenAI API Configuration (Required)
OPENAI_API_KEY=your_openai_api_key_here

# ============================================================================
# OPTIONAL CONFIGURATION
# ============================================================================

# Judgment Labs Configuration (for testing and monitoring)
JUDGMENT_API_KEY=your_judgment_labs_api_key_here
JUDGMENT_ORG_ID=your_judgment_organization_id_here

# API Settings
NBA_AGENT_REQUEST_TIMEOUT=30          # Request timeout in seconds
NBA_AGENT_MAX_RETRIES=3               # API retry attempts
NBA_AGENT_RATE_LIMIT=100              # Requests per minute limit
NBA_AGENT_MAX_CONCURRENT=10           # Maximum concurrent requests

# Cache Settings
NBA_AGENT_CACHE_TTL=3600              # Cache timeout in seconds (1 hour)
NBA_AGENT_CACHE_DIR=cache             # Cache directory
NBA_AGENT_MAX_CACHE_SIZE_MB=100       # Maximum cache size in MB
NBA_AGENT_ENABLE_MEMORY_CACHE=true    # Enable in-memory caching
NBA_AGENT_ENABLE_DISK_CACHE=true      # Enable disk caching

# Logging Settings
NBA_AGENT_LOG_LEVEL=INFO              # Logging level (DEBUG, INFO, WARNING, ERROR)
LOG_FORMAT=colored                    # Log format (colored or json)
NBA_AGENT_LOG_FILE=                   # Optional log file path
NBA_AGENT_MAX_LOG_SIZE_MB=10          # Max log file size in MB
NBA_AGENT_LOG_ROTATION_COUNT=5        # Number of log files to keep

# Security Settings
NBA_AGENT_ENABLE_VALIDATION=true      # Enable input validation
API_RATE_LIMIT_ENABLED=true           # Enable API rate limiting
NBA_AGENT_MAX_QUERY_LENGTH=500        # Maximum query length
NBA_AGENT_MAX_PLAYER_NAME_LENGTH=50   # Maximum player name length
NBA_AGENT_MAX_TEAM_NAME_LENGTH=50     # Maximum team name length
NBA_AGENT_ENABLE_SANITIZATION=true    # Enable request sanitization

# Performance Settings
NBA_AGENT_ENABLE_ASYNC=false          # Enable async processing
NBA_AGENT_POOL_SIZE=10                # Connection pool size
NBA_AGENT_ENABLE_COMPRESSION=true     # Enable response compression
NBA_AGENT_QUERY_TIMEOUT=30            # Query timeout in seconds
NBA_AGENT_ENABLE_MONITORING=true      # Enable performance monitoring

# Streamlit Configuration
STREAMLIT_SERVER_PORT=8501            # Default Streamlit port
STREAMLIT_SERVER_ADDRESS=localhost    # Server address
STREAMLIT_MAX_UPLOAD_SIZE_MB=200      # Max upload size in MB
STREAMLIT_ENABLE_CORS=false           # Enable CORS
STREAMLIT_THEME=dark                  # UI theme

# Development Settings
DEBUG=false                           # Enable debug mode
DEVELOPMENT_MODE=false                # Enable development features
TESTING=false                         # Enable testing mode
ENVIRONMENT=production                # Environment (development, staging, production)
"""
    return template

# Global configuration instance
_config: Optional[NBAAgentConfig] = None

def get_config() -> NBAAgentConfig:
    """
    Get the global configuration instance (singleton pattern)
    
    Returns:
        NBAAgentConfig instance
    """
    global _config
    if _config is None:
        _config = load_config()
    return _config

def reload_config() -> NBAAgentConfig:
    """
    Force reload of configuration from environment
    
    Returns:
        Newly loaded NBAAgentConfig instance
    """
    global _config
    _config = load_config()
    return _config

# Export main functions and classes
__all__ = [
    'NBAAgentConfig',
    'APIConfig',
    'CacheConfig', 
    'LoggingConfig',
    'SecurityConfig',
    'PerformanceConfig',
    'StreamlitConfig',
    'load_config',
    'validate_config',
    'create_env_template',
    'get_config',
    'reload_config'
] 