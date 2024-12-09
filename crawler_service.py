import asyncio
import aiohttp
from bs4 import BeautifulSoup
from typing import Set, Dict, List
import logging
import yaml
from urllib.parse import urljoin, urlparse

# Load configuration from YAML file
with open('config.yaml', 'r') as file:
    config = yaml.safe_load(file)

# Configure logging with timestamp, level and message format
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

class WebCrawlerService:
    """
    A web crawler service that generates a sitemap by recursively crawling web pages.
    The crawler respects rate limits, timeouts and max link constraints defined in config.
    """
    def __init__(self):
        # Set of URLs that have been crawled to avoid duplicates
        self.visited_urls: Set[str] = set()
        # Dictionary mapping URLs to their outbound links
        self.sitemap: Dict[str, List[str]] = {}
        # Domain being crawled, used to filter external links
        self.base_domain: str = ""
        # Semaphore to limit concurrent requests
        self.semaphore = asyncio.Semaphore(config['crawler']['max_concurrency'])
        # Maximum number of unique URLs to crawl
        self.max_links = config['crawler']['max_links']
        # Timeout for the entire crawl operation
        self.timeout_seconds = config['crawler']['timeout_seconds']

    async def crawl(self, start_url: str) -> Dict[str, List[str]]:
        """
        Main crawling method that initializes the crawl from a starting URL.
        
        Args:
            start_url (str): The URL to start crawling from
            
        Returns:
            Dict[str, List[str]]: A sitemap dictionary where keys are URLs and values are lists of outbound links
            
        Raises:
            TimeoutError: If crawling exceeds configured timeout
            Exception: For any other errors during crawling
        """
        logging.debug(f"Starting crawl for URL: {start_url}")
        self.visited_urls.clear()
        self.sitemap.clear()
        self.base_domain = urlparse(start_url).netloc

        try:
            async with aiohttp.ClientSession() as session:
                await asyncio.wait_for(self._crawl_page(session, start_url), timeout=self.timeout_seconds)
        except asyncio.TimeoutError:
            logging.warning("Crawling timed out.")
        except Exception as e:
            logging.error(f"Error during crawling: {str(e)}")

        logging.debug(f"Crawling completed. Sitemap generated: {self.sitemap}")
        return self.sitemap

    async def _crawl_page(self, session: aiohttp.ClientSession, url: str) -> None:
        """
        Crawls a single page, extracts links and recursively crawls found links.
        
        Args:
            session (aiohttp.ClientSession): Session for making HTTP requests
            url (str): URL of the page to crawl
            
        Note:
            Uses semaphore to limit concurrent requests
            Skips already visited URLs and respects max_links limit
        """
        if url in self.visited_urls or len(self.visited_urls) >= self.max_links:
            return

        async with self.semaphore:
            self.visited_urls.add(url)
            logging.info(f"Crawling URL: {url}")
            try:
                async with session.get(url) as response:
                    if response.status != 200:
                        logging.warning(f"Failed to fetch {url}: HTTP {response.status}")
                        return

                    html = await response.text(errors='ignore')
                    soup = BeautifulSoup(html, 'html.parser')
                    links = self._extract_links(soup, url)
                    self.sitemap[url] = links
                    logging.debug(f"Found {len(links)} links on {url}")

                    # Create tasks for crawling discovered links
                    tasks = [
                        self._crawl_page(session, link)
                        for link in links if link not in self.visited_urls
                    ]
                    if tasks:
                        await asyncio.gather(*tasks)

            except aiohttp.ClientError as e:
                logging.error(f"HTTP error while fetching {url}: {str(e)}")
            except Exception as e:
                logging.error(f"Error crawling {url}: {str(e)}")

    def _extract_links(self, soup: BeautifulSoup, base_url: str) -> List[str]:
        """
        Extracts and filters valid links from a BeautifulSoup parsed page.
        
        Args:
            soup (BeautifulSoup): Parsed HTML content
            base_url (str): Base URL for resolving relative links
            
        Returns:
            List[str]: List of absolute URLs found on the page that belong to the same domain
            
        Note:
            Filters out external domains and invalid schemes
            Removes URL fragments
        """
        links = set()
        for anchor in soup.find_all('a', href=True):
            href = anchor['href']
            absolute_url = urljoin(base_url, href)
            parsed_url = urlparse(absolute_url)

            # Remove URL fragments and filter valid URLs
            absolute_url = absolute_url.split('#')[0]
            if parsed_url.netloc == self.base_domain and parsed_url.scheme in ('http', 'https'):
                links.add(absolute_url)

        logging.debug(f"Extracted {len(links)} valid links from {base_url}")
        return list(links)
