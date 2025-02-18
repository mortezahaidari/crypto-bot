# src/core/utils.py
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type

def retry_on_failure(func):
    return retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=2, max=10),
        retry=retry_if_exception_type((ccxt.NetworkError, ccxt.ExchangeError)),
    )(func)