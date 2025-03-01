import functools
import time
import logging
from typing import Callable, Any
import asyncio
import concurrent.futures


class PerformanceOptimizer:
    """
    Performance optimization utilities for Farm Manager.
    """

    @staticmethod
    def memoize(func: Callable) -> Callable:
        """
        Memoization decorator to cache function results.

        Args:
            func (Callable): Function to memoize

        Returns:
            Callable: Memoized function
        """
        cache = {}

        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            # Create a hashable key from arguments
            key = str(args) + str(kwargs)

            # Check if result is in cache
            if key not in cache:
                cache[key] = func(*args, **kwargs)

            return cache[key]

        return wrapper

    @staticmethod
    def retry(max_attempts: int = 3, delay: float = 1.0) -> Callable:
        """
        Retry decorator for handling transient failures.

        Args:
            max_attempts (int): Maximum number of retry attempts
            delay (float): Delay between retry attempts in seconds

        Returns:
            Callable: Decorated function with retry logic
        """

        def decorator(func: Callable) -> Callable:
            @functools.wraps(func)
            def wrapper(*args, **kwargs):
                logger = logging.getLogger("performance")
                attempts = 0

                while attempts < max_attempts:
                    try:
                        return func(*args, **kwargs)
                    except Exception as e:
                        attempts += 1
                        logger.warning(
                            f"Attempt {attempts} failed: {str(e)}. " f"Retrying in {delay} seconds."
                        )

                        if attempts == max_attempts:
                            logger.error(f"All {max_attempts} attempts failed.")
                            raise

                        time.sleep(delay)

            return wrapper

        return decorator

    @staticmethod
    def async_parallel_executor(max_workers: int = None):
        """
        Decorator to execute functions in parallel using thread pool.

        Args:
            max_workers (int, optional): Maximum number of worker threads

        Returns:
            Callable: Decorator for parallel execution
        """

        def decorator(func: Callable) -> Callable:
            @functools.wraps(func)
            def wrapper(*args, **kwargs):
                with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
                    future = executor.submit(func, *args, **kwargs)
                    return future.result()

            return wrapper

        return decorator

    @staticmethod
    def circuit_breaker(failure_threshold: int = 3, recovery_timeout: float = 60.0) -> Callable:
        """
        Circuit breaker pattern to prevent system overload.

        Args:
            failure_threshold (int): Number of consecutive failures before breaking
            recovery_timeout (float): Time to wait before attempting recovery

        Returns:
            Callable: Decorated function with circuit breaker logic
        """

        def decorator(func: Callable) -> Callable:
            failures = 0
            last_failure_time = 0

            @functools.wraps(func)
            def wrapper(*args, **kwargs):
                nonlocal failures, last_failure_time
                current_time = time.time()

                # Check if in recovery period
                if (current_time - last_failure_time) < recovery_timeout:
                    raise RuntimeError("Circuit is open. Service temporarily unavailable.")

                try:
                    result = func(*args, **kwargs)
                    failures = 0  # Reset on success
                    return result
                except Exception as e:
                    failures += 1
                    last_failure_time = current_time

                    if failures >= failure_threshold:
                        logging.getLogger("performance").error(
                            f"Circuit breaker activated for {func.__name__}"
                        )

                    raise

            return wrapper

        return decorator
