# Web Crawler Project

This project is a web crawler application built using FastAPI and aiohttp. It allows users to input a URL and generates a sitemap by recursively crawling web pages. The application is designed to respect rate limits, timeouts, and maximum link constraints defined in the configuration.

## Features

- **Concurrency Control**: Limits the number of concurrent requests using asyncio semaphores.
- **Timeout Management**: Configurable timeout for the entire crawl operation.
- **Domain Filtering**: Only crawls links within the same domain as the starting URL.
- **Sitemap Generation**: Outputs a tree view and JSON format of the sitemap.

## Project Structure

- **Crawler**: Contains the main crawling logic and configuration.
  - `crawler_service.py`: Implements the web crawler logic.
  - `server.py`: FastAPI server that handles crawl requests.
  - `client.py`: FastAPI client for user interaction.
  - `config.yaml`: Configuration file for crawler settings.
  - `client_config.yaml`: Configuration file for client settings.
  - `templates/`: HTML templates for the client interface.

- **Tests**: Contains unit tests for the crawler service.
  - `test_crawler.py`: Tests for the crawler service.

- **Dockerfile**: Docker configuration for containerizing the application.

## Installation

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd <repository-directory>
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**:
   - **Using Python**:
     ```bash
     python Crawler/server.py
     ```
   - **Using Docker**:
     ```bash
     docker build -t web-crawler .
     docker run -p 8000:8000 web-crawler
     ```

## Usage

1. **Access the client interface**:
   Open your browser and navigate to `http://localhost:8001`.

2. **Crawl a website**:
   - Enter the URL you wish to crawl in the input field.
   - Click "Crawl" to start the crawling process.

3. **View results**:
   - The sitemap will be displayed in both tree view and JSON format.

## Configuration

- **Crawler Settings**: Modify `Crawler/config.yaml` to adjust concurrency, timeout, and max links.
- **Client Settings**: Modify `Crawler/client/client_config.yaml` to adjust server URL, host, and port.

