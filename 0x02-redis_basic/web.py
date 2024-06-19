import requests
import redis
import time
from functools import wraps


# Initialize Redis connection
redis_client = redis.Redis(host='localhost', port=6379, db=0)


def track_access_and_cache(func):
    @wraps(func)
    def wrapper(url):
        """
        Check if the URL is from slowwly.robertomurray.co.uk
        for testing slow response
        """
        slow_response = 'slowwly.robertomurray.co.uk' in url

        # Increment access count for the URL in Redis
        url_count_key = f"count:{url}"
        redis_client.incr(url_count_key)

        # Check if HTML content is cached
        cached_html = redis_client.get(url)
        if cached_html:
            return cached_html.decode('utf-8')

        # Fetch HTML content
        response = requests.get(url)
        html_content = response.text

        # Cache HTML content with 10 seconds expiration
        redis_client.setex(url, 10, html_content)

        # Simulate slow response for testing
        if slow_response:
            time.sleep(5)  # Simulate a slow response time

        return html_content

    return wrapper


@track_access_and_cache
def get_page(url: str) -> str:
    """
    Fetch HTML content from a URL and cache it with a 10-second expiration.

    Args:
        url (str): The URL to fetch HTML content from.

    Returns:
        str: The HTML content of the URL.
    """
    return requests.get(url).text


# Example usage
if __name__ == "__main__":
    url = "http://slowwly.robertomurray.co.uk/delay/5000/url/http://www.google.com"
    html = get_page(url)
    print(html)
