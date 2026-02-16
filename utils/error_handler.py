"""
Centralized error handling system
"""
import logging
import traceback
from typing import Optional, Callable
from enum import Enum
from datetime import datetime


class ErrorSeverity(Enum):
    """Error severity levels"""
    INFO = "info"
    WARNING = "warning"
    ERROR = "error"
    CRITICAL = "critical"


class AppError(Exception):
    """Base application error"""
    
    def __init__(self, message: str, severity: ErrorSeverity = ErrorSeverity.ERROR, 
                 details: Optional[str] = None, user_message: Optional[str] = None):
        self.message = message
        self.severity = severity
        self.details = details
        self.user_message = user_message or self._get_user_friendly_message()
        self.timestamp = datetime.now()
        super().__init__(self.message)
    
    def _get_user_friendly_message(self) -> str:
        """Convert technical error to user-friendly message"""
        return "Đã xảy ra lỗi. Vui lòng thử lại."


class DataError(AppError):
    """Data-related errors"""
    
    def _get_user_friendly_message(self) -> str:
        return "Lỗi xử lý dữ liệu. Vui lòng kiểm tra định dạng file."


class ConnectionError(AppError):
    """Connection-related errors"""
    
    def _get_user_friendly_message(self) -> str:
        return "Không thể kết nối. Vui lòng kiểm tra thông tin kết nối."


class ValidationError(AppError):
    """Validation errors"""
    
    def _get_user_friendly_message(self) -> str:
        return "Dữ liệu không hợp lệ. Vui lòng kiểm tra lại."


class ErrorHandler:
    """Centralized error handler"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.error_callbacks = []
        self._setup_logging()
    
    def _setup_logging(self):
        """Setup logging configuration"""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('logs/app.log'),
                logging.StreamHandler()
            ]
        )
    
    def register_callback(self, callback: Callable):
        """Register error callback for UI notifications"""
        self.error_callbacks.append(callback)
    
    def handle_error(self, error: Exception, context: Optional[str] = None) -> AppError:
        """
        Handle any error and convert to AppError
        
        Args:
            error: The exception to handle
            context: Additional context about where error occurred
            
        Returns:
            AppError: Standardized error object
        """
        # Convert to AppError if not already
        if isinstance(error, AppError):
            app_error = error
        else:
            app_error = AppError(
                message=str(error),
                severity=ErrorSeverity.ERROR,
                details=traceback.format_exc()
            )
        
        # Log error
        self._log_error(app_error, context)
        
        # Notify callbacks
        self._notify_callbacks(app_error)
        
        return app_error
    
    def _log_error(self, error: AppError, context: Optional[str] = None):
        """Log error with appropriate level"""
        log_message = f"{context}: {error.message}" if context else error.message
        
        if error.severity == ErrorSeverity.CRITICAL:
            self.logger.critical(log_message, exc_info=True)
        elif error.severity == ErrorSeverity.ERROR:
            self.logger.error(log_message, exc_info=True)
        elif error.severity == ErrorSeverity.WARNING:
            self.logger.warning(log_message)
        else:
            self.logger.info(log_message)
    
    def _notify_callbacks(self, error: AppError):
        """Notify registered callbacks"""
        for callback in self.error_callbacks:
            try:
                callback(error)
            except Exception as e:
                self.logger.error(f"Error in callback: {e}")


# Global error handler instance
error_handler = ErrorHandler()


def handle_errors(context: str = ""):
    """Decorator for error handling"""
    def decorator(func):
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                error = error_handler.handle_error(e, context or func.__name__)
                raise error
        return wrapper
    return decorator
