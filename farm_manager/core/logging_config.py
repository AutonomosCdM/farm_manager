import logging
import os
from logging.handlers import RotatingFileHandler
from datetime import datetime


def setup_logging(log_level=logging.INFO):
    """
    Configure centralized logging for the Farm Manager application.

    Args:
        log_level (int): Logging level (default: logging.INFO)
    """
    # Ensure logs directory exists
    logs_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "logs")
    os.makedirs(logs_dir, exist_ok=True)

    # Create log filename with timestamp
    log_filename = os.path.join(
        logs_dir, f'farm_manager_{datetime.now().strftime("%Y%m%d_%H%M%S")}.log'
    )

    # Configure root logger
    logging.basicConfig(
        level=log_level,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        handlers=[
            # Console handler
            logging.StreamHandler(),
            # File handler with rotation
            RotatingFileHandler(log_filename, maxBytes=10 * 1024 * 1024, backupCount=5),  # 10 MB
        ],
    )

    # Create a logger for performance tracking
    performance_logger = logging.getLogger("performance")
    performance_logger.setLevel(logging.INFO)

    return {
        "main_logger": logging.getLogger(__name__),
        "performance_logger": performance_logger,
    }


# Performance tracking decorator
def track_performance(logger=None):
    """
    Decorator to track function performance and log execution time.

    Args:
        logger (logging.Logger, optional): Logger to use. Defaults to performance logger.
    """
    import functools
    import time

    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            nonlocal logger
            if logger is None:
                logger = logging.getLogger("performance")

            start_time = time.perf_counter()
            try:
                result = func(*args, **kwargs)
                end_time = time.perf_counter()

                # Log performance metrics
                logger.info(
                    f"Performance: {func.__name__} "
                    f"Execution time: {(end_time - start_time) * 1000:.2f} ms"
                )

                return result
            except Exception as e:
                logger.error(f"Error in {func.__name__}: {str(e)}", exc_info=True)
                raise

        return wrapper

    return decorator


# Global error handler
class FarmManagerError(Exception):
    """Base exception for Farm Manager application."""

    pass


class ResourceAllocationError(FarmManagerError):
    """Raised when there are issues with resource allocation."""

    pass


class DataValidationError(FarmManagerError):
    """Raised when data validation fails."""

    pass


def global_exception_handler(exc_type, exc_value, exc_traceback):
    """
    Global exception handler to log unhandled exceptions.

    Args:
        exc_type (type): Exception type
        exc_value (Exception): Exception instance
        exc_traceback (traceback): Traceback object
    """
    logger = logging.getLogger("error")
    logger.error("Uncaught exception", exc_info=(exc_type, exc_value, exc_traceback))


# Set the global exception handler
import sys

sys.excepthook = global_exception_handler
