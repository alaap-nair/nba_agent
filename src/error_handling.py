#!/usr/bin/env python3
"""
Comprehensive error handling for NBA Agent
Custom exceptions, retry logic, and graceful degradation strategies
"""

import time
import functools
from typing import Optional, Dict, Any, Callable, Type, Union
from dataclasses import dataclass
from enum import Enum
import requests
from logger import get_logger, log_error_with_context

logger = get_logger(__name__)

class ErrorSeverity(Enum):
    """Error severity levels"""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

class ErrorCategory(Enum):
    """Error categories for better handling"""
    VALIDATION = "validation"
    API = "api"
    NETWORK = "network"
    AUTHENTICATION = "authentication"
    RATE_LIMIT = "rate_limit"
    DATA = "data"
    SYSTEM = "system"
    USER = "user"

@dataclass
class ErrorContext:
    """Context information for errors"""
    operation: str
    user_query: Optional[str] = None
    api_endpoint: Optional[str] = None
    player_name: Optional[str] = None
    team_name: Optional[str] = None
    season: Optional[str] = None
    additional_data: Optional[Dict[str, Any]] = None

class NBAAgentError(Exception):
    """Base exception for NBA Agent"""
    
    def __init__(
        self, 
        message: str, 
        category: ErrorCategory = ErrorCategory.SYSTEM,
        severity: ErrorSeverity = ErrorSeverity.MEDIUM,
        context: Optional[ErrorContext] = None,
        original_error: Optional[Exception] = None
    ):
        super().__init__(message)
        self.message = message
        self.category = category
        self.severity = severity
        self.context = context or ErrorContext("unknown")
        self.original_error = original_error
        self.timestamp = time.time()

class ValidationError(NBAAgentError):
    """Input validation errors"""
    
    def __init__(self, message: str, context: Optional[ErrorContext] = None):
        super().__init__(
            message, 
            category=ErrorCategory.VALIDATION,
            severity=ErrorSeverity.LOW,
            context=context
        )

class APIError(NBAAgentError):
    """NBA API related errors"""
    
    def __init__(
        self, 
        message: str, 
        status_code: Optional[int] = None,
        endpoint: Optional[str] = None,
        context: Optional[ErrorContext] = None,
        original_error: Optional[Exception] = None
    ):
        super().__init__(
            message,
            category=ErrorCategory.API,
            severity=ErrorSeverity.MEDIUM,
            context=context,
            original_error=original_error
        )
        self.status_code = status_code
        self.endpoint = endpoint

class NetworkError(NBAAgentError):
    """Network connectivity errors"""
    
    def __init__(self, message: str, context: Optional[ErrorContext] = None, original_error: Optional[Exception] = None):
        super().__init__(
            message,
            category=ErrorCategory.NETWORK,
            severity=ErrorSeverity.HIGH,
            context=context,
            original_error=original_error
        )

class RateLimitError(NBAAgentError):
    """Rate limiting errors"""
    
    def __init__(
        self, 
        message: str, 
        retry_after: Optional[int] = None,
        context: Optional[ErrorContext] = None
    ):
        super().__init__(
            message,
            category=ErrorCategory.RATE_LIMIT,
            severity=ErrorSeverity.MEDIUM,
            context=context
        )
        self.retry_after = retry_after

class AuthenticationError(NBAAgentError):
    """Authentication and authorization errors"""
    
    def __init__(self, message: str, context: Optional[ErrorContext] = None):
        super().__init__(
            message,
            category=ErrorCategory.AUTHENTICATION,
            severity=ErrorSeverity.HIGH,
            context=context
        )

class DataError(NBAAgentError):
    """Data integrity and processing errors"""
    
    def __init__(self, message: str, context: Optional[ErrorContext] = None, original_error: Optional[Exception] = None):
        super().__init__(
            message,
            category=ErrorCategory.DATA,
            severity=ErrorSeverity.MEDIUM,
            context=context,
            original_error=original_error
        )

class UserError(NBAAgentError):
    """User input errors (friendly messages)"""
    
    def __init__(self, message: str, context: Optional[ErrorContext] = None):
        super().__init__(
            message,
            category=ErrorCategory.USER,
            severity=ErrorSeverity.LOW,
            context=context
        )

def retry_with_backoff(
    max_retries: int = 3,
    base_delay: float = 1.0,
    max_delay: float = 60.0,
    backoff_factor: float = 2.0,
    exceptions: tuple = (Exception,)
):
    """
    Decorator for retrying functions with exponential backoff
    
    Args:
        max_retries: Maximum number of retry attempts
        base_delay: Initial delay between retries
        max_delay: Maximum delay between retries
        backoff_factor: Multiplier for delay after each retry
        exceptions: Tuple of exceptions to catch and retry
    """
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            last_exception = None
            
            for attempt in range(max_retries + 1):
                try:
                    return func(*args, **kwargs)
                except exceptions as e:
                    last_exception = e
                    
                    if attempt == max_retries:
                        # Log final failure
                        log_error_with_context(
                            logger, 
                            e, 
                            {
                                "function": func.__name__,
                                "max_retries": max_retries,
                                "final_attempt": True
                            }
                        )
                        raise
                    
                    # Calculate delay with exponential backoff
                    delay = min(base_delay * (backoff_factor ** attempt), max_delay)
                    
                    logger.warning(
                        f"Attempt {attempt + 1}/{max_retries + 1} failed for {func.__name__}: {str(e)}. "
                        f"Retrying in {delay:.1f}s"
                    )
                    
                    time.sleep(delay)
            
            # This should never be reached, but just in case
            if last_exception:
                raise last_exception
        
        return wrapper
    return decorator

def handle_api_errors(func: Callable) -> Callable:
    """
    Decorator to handle common NBA API errors with appropriate exceptions
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except requests.exceptions.ConnectionError as e:
            context = ErrorContext(
                operation=func.__name__,
                additional_data={"args": str(args), "kwargs": str(kwargs)}
            )
            raise NetworkError("Failed to connect to NBA API", context=context, original_error=e)
        except requests.exceptions.Timeout as e:
            context = ErrorContext(operation=func.__name__)
            raise APIError("NBA API request timed out", context=context, original_error=e)
        except requests.exceptions.HTTPError as e:
            status_code = e.response.status_code if e.response else None
            context = ErrorContext(operation=func.__name__)
            
            if status_code == 429:
                retry_after = e.response.headers.get('Retry-After')
                raise RateLimitError(
                    "NBA API rate limit exceeded", 
                    retry_after=int(retry_after) if retry_after else None,
                    context=context
                )
            elif status_code in [401, 403]:
                raise AuthenticationError("NBA API authentication failed", context=context)
            else:
                raise APIError(
                    f"NBA API error: {status_code}", 
                    status_code=status_code,
                    context=context,
                    original_error=e
                )
        except ValueError as e:
            context = ErrorContext(operation=func.__name__)
            raise DataError(f"Invalid data received from NBA API: {str(e)}", context=context, original_error=e)
        except Exception as e:
            context = ErrorContext(operation=func.__name__)
            raise NBAAgentError(
                f"Unexpected error in {func.__name__}: {str(e)}",
                category=ErrorCategory.SYSTEM,
                severity=ErrorSeverity.HIGH,
                context=context,
                original_error=e
            )
    
    return wrapper

def safe_execute(
    func: Callable,
    default_return: Any = None,
    error_message: str = "Operation failed",
    log_errors: bool = True
) -> Any:
    """
    Safely execute a function with error handling and optional default return
    
    Args:
        func: Function to execute
        default_return: Value to return if function fails
        error_message: Message to log on error
        log_errors: Whether to log errors
        
    Returns:
        Function result or default_return on error
    """
    try:
        return func()
    except Exception as e:
        if log_errors:
            log_error_with_context(
                logger, 
                e, 
                {
                    "function": func.__name__ if hasattr(func, '__name__') else str(func),
                    "error_message": error_message
                }
            )
        return default_return

def format_user_error(error: Exception) -> str:
    """
    Format an error message for user display (removing technical details)
    
    Args:
        error: Exception to format
        
    Returns:
        User-friendly error message
    """
    if isinstance(error, UserError):
        return error.message
    elif isinstance(error, ValidationError):
        return f"Input error: {error.message}"
    elif isinstance(error, RateLimitError):
        return "We're currently receiving a lot of requests. Please try again in a moment."
    elif isinstance(error, NetworkError):
        return "We're having trouble connecting to the NBA data service. Please check your internet connection and try again."
    elif isinstance(error, AuthenticationError):
        return "There's an issue with our API access. Please contact support if this persists."
    elif isinstance(error, APIError):
        return "We're experiencing issues retrieving NBA data. Please try again later."
    elif isinstance(error, DataError):
        return "We found some inconsistent data. Please try a different query or contact support."
    else:
        return "An unexpected error occurred. Please try again or contact support if the problem persists."

def create_error_response(error: Exception, include_details: bool = False) -> Dict[str, Any]:
    """
    Create a standardized error response dictionary
    
    Args:
        error: Exception to format
        include_details: Whether to include technical details
        
    Returns:
        Error response dictionary
    """
    response = {
        "error": True,
        "message": format_user_error(error),
        "timestamp": time.time()
    }
    
    if isinstance(error, NBAAgentError):
        response["category"] = error.category.value
        response["severity"] = error.severity.value
        
        if include_details and error.context:
            response["context"] = {
                "operation": error.context.operation,
                "query": error.context.user_query
            }
    
    if include_details:
        response["technical_message"] = str(error)
        response["error_type"] = type(error).__name__
    
    return response

# Context manager for error handling
class ErrorHandler:
    """Context manager for comprehensive error handling"""
    
    def __init__(
        self, 
        operation: str,
        context: Optional[ErrorContext] = None,
        reraise: bool = True,
        log_errors: bool = True
    ):
        self.operation = operation
        self.context = context or ErrorContext(operation)
        self.reraise = reraise
        self.log_errors = log_errors
        self.start_time = time.time()
    
    def __enter__(self):
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is not None:
            duration = time.time() - self.start_time
            
            if self.log_errors:
                log_error_with_context(
                    logger,
                    exc_val,
                    {
                        "operation": self.operation,
                        "duration": duration,
                        "context": self.context.__dict__
                    }
                )
            
            if not self.reraise:
                return True  # Suppress the exception
        
        return False

# Export main classes and functions
__all__ = [
    'ErrorSeverity',
    'ErrorCategory', 
    'ErrorContext',
    'NBAAgentError',
    'ValidationError',
    'APIError',
    'NetworkError',
    'RateLimitError',
    'AuthenticationError',
    'DataError',
    'UserError',
    'retry_with_backoff',
    'handle_api_errors',
    'safe_execute',
    'format_user_error',
    'create_error_response',
    'ErrorHandler'
] 