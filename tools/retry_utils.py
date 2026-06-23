import time
import functools
import random

def with_retry(max_retries=3, initial_delay=1.0, backoff_factor=2.0):
    """
    Robust decorator to automatically retry flaky network/API tool calls,
    with specialized handling for 429 (Rate Limit) and 403 (Forbidden).
    """
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            delay = initial_delay
            last_exception = None
            for attempt in range(max_retries):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    last_exception = e
                    err_str = str(e).lower()
                    
                    is_rate_limit = "429" in err_str or "too many requests" in err_str or "rate limit" in err_str
                    is_forbidden = "403" in err_str or "forbidden" in err_str or "unauthorized" in err_str
                    
                    print(f"[*] Tool '{func.__name__}' failed on attempt {attempt + 1}/{max_retries}: {str(e)[:100]}")
                    
                    if attempt < max_retries - 1:
                        # Dynamic backoff scaling
                        current_delay = delay
                        if is_rate_limit:
                            print(f"[*] Rate limit (429) hit in tool '{func.__name__}'. Applying heavy backoff.")
                            current_delay *= 3.0  # Triple the delay on rate limits
                        elif is_forbidden:
                            print(f"[*] Forbidden (403) hit in tool '{func.__name__}'. May be IP blocked. Waiting before retry.")
                            current_delay *= 2.0  # Double the delay on 403s
                            
                        # Add jitter to prevent thundering herd
                        sleep_time = current_delay * random.uniform(0.8, 1.2)
                        time.sleep(sleep_time)
                        delay *= backoff_factor
            
            print(f"[*] Tool '{func.__name__}' completely exhausted retries. Returning fallback empty state.")
            # Return a graceful fallback instead of crashing the backend
            return f"Error: Tool {func.__name__} failed to fetch data due to network error: {str(last_exception)[:50]}"
        return wrapper
    return decorator
