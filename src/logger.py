#!/usr/bin/env python3
"""
Structured logging system for NBA Agent
Provides consistent logging across all components with proper formatting and levels
"""

import logging
import sys
import os
from datetime import datetime
from typing import Optional
import json

class JSONFormatter(logging.Formatter):
    """Custom JSON formatter for structured logging"""
    
    def format(self, record):
        log_entry = {
            'timestamp': datetime.utcnow().isoformat() + 'Z',
            'level': record.levelname,
            'logger': record.name,
            'message': record.getMessage(),
            'module': record.module,
            'function': record.funcName,
            'line': record.lineno
        }
        
        # Add exception info if present
        if record.exc_info:
            log_entry['exception'] = self.formatException(record.exc_info)
        
        # Add extra fields if present
        if hasattr(record, 'user_id'):
            log_entry['user_id'] = record.user_id
        if hasattr(record, 'query'):
            log_entry['query'] = record.query
        if hasattr(record, 'response_time'):
            log_entry['response_time'] = record.response_time
        if hasattr(record, 'api_endpoint'):
            log_entry['api_endpoint'] = record.api_endpoint
        
        return json.dumps(log_entry)

class ColoredFormatter(logging.Formatter):
    """Colored formatter for console output"""
    
    COLORS = {
        'DEBUG': '\033[36m',     # Cyan
        'INFO': '\033[32m',      # Green
        'WARNING': '\033[33m',   # Yellow
        'ERROR': '\033[31m',     # Red
        'CRITICAL': '\033[35m',  # Magenta
        'RESET': '\033[0m'       # Reset
    }
    
    def format(self, record):
        color = self.COLORS.get(record.levelname, self.COLORS['RESET'])
        reset = self.COLORS['RESET']
        
        # Format timestamp
        timestamp = datetime.fromtimestamp(record.created).strftime('%Y-%m-%d %H:%M:%S')
        
        # Create formatted message
        formatted_message = (
            f"{color}[{timestamp}] {record.levelname:8} "
            f"{record.name}:{record.lineno} - {record.getMessage()}{reset}"
        )
        
        return formatted_message

def setup_logger(
    name: str = "nba_agent",
    level: Optional[str] = None,
    enable_json: bool = False,
    log_file: Optional[str] = None
) -> logging.Logger:
    """
    Set up a logger with appropriate handlers and formatters
    
    Args:
        name: Logger name
        level: Log level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        enable_json: Whether to use JSON formatting
        log_file: Optional log file path
    
    Returns:
        Configured logger instance
    """
    # Get log level from environment or use provided level
    if level is None:
        level = os.getenv('NBA_AGENT_LOG_LEVEL', 'INFO').upper()
    
    # Create logger
    logger = logging.getLogger(name)
    logger.setLevel(getattr(logging, level, logging.INFO))
    
    # Clear existing handlers to avoid duplicates
    logger.handlers.clear()
    
    # Console handler
    console_handler = logging.StreamHandler(sys.stdout)
    
    if enable_json or os.getenv('LOG_FORMAT') == 'json':
        console_formatter = JSONFormatter()
    else:
        console_formatter = ColoredFormatter()
    
    console_handler.setFormatter(console_formatter)
    logger.addHandler(console_handler)
    
    # File handler (if specified)
    if log_file:
        file_handler = logging.FileHandler(log_file)
        file_formatter = JSONFormatter()  # Always use JSON for file logs
        file_handler.setFormatter(file_formatter)
        logger.addHandler(file_handler)
    
    return logger

def get_logger(name: str = None) -> logging.Logger:
    """
    Get a logger instance with the NBA Agent configuration
    
    Args:
        name: Logger name (defaults to calling module name)
    
    Returns:
        Configured logger instance
    """
    if name is None:
        # Get the calling module name
        import inspect
        frame = inspect.currentframe().f_back
        name = frame.f_globals['__name__']
    
    return setup_logger(name)

# Performance logging utilities
def log_performance(logger: logging.Logger, operation: str, duration: float, **kwargs):
    """Log performance metrics"""
    logger.info(
        f"Performance: {operation} completed in {duration:.3f}s",
        extra={
            'operation': operation,
            'duration': duration,
            **kwargs
        }
    )

def log_api_call(logger: logging.Logger, endpoint: str, method: str, status_code: int, 
                duration: float, **kwargs):
    """Log API call details"""
    logger.info(
        f"API Call: {method} {endpoint} - {status_code} ({duration:.3f}s)",
        extra={
            'api_endpoint': endpoint,
            'method': method,
            'status_code': status_code,
            'response_time': duration,
            **kwargs
        }
    )

def log_user_query(logger: logging.Logger, query: str, response_time: float, 
                  success: bool, **kwargs):
    """Log user queries for analytics"""
    level = logging.INFO if success else logging.WARNING
    logger.log(
        level,
        f"User Query: '{query}' - {'Success' if success else 'Failed'} ({response_time:.3f}s)",
        extra={
            'query': query,
            'response_time': response_time,
            'success': success,
            **kwargs
        }
    )

def log_error_with_context(logger: logging.Logger, error: Exception, context: dict = None):
    """Log errors with additional context"""
    context = context or {}
    logger.error(
        f"Error occurred: {type(error).__name__}: {str(error)}",
        extra=context,
        exc_info=True
    )

# Create default logger
default_logger = setup_logger()

# Export commonly used functions
__all__ = [
    'setup_logger',
    'get_logger', 
    'log_performance',
    'log_api_call',
    'log_user_query',
    'log_error_with_context',
    'default_logger'
] 