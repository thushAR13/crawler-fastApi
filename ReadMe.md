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

### Prerequisites
Ensure you have the following installed:
- Python 3.11+
- Docker
- Kubernetes (Minikube or a Kubernetes cluster)

### Steps

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
   - **Start the server**:
     ```bash
     python Crawler/server.py
     ```
   - **Start the client**:
     ```bash
     python Crawler/client/client.py
     ```
     The client interface will be accessible at `http://localhost:8001`.

4. **Run using Docker**:
   - **Build and run the server**:
     ```bash
     docker build -t web-crawler-server -f /Dockerfile .
     docker run -p 8000:8000 web-crawler-server
     ```
   - **Build and run the client**:
     ```bash
     docker build -t web-crawler-client -f client/Dockerfile .
     docker run -p 8001:8001 web-crawler-client
     ```

## Usage

1. **Access the client interface**:
   Open your browser and navigate to `http://localhost:8001`.

2. **Crawl a website**:
   - Enter the URL you wish to crawl in the input field.
   - Click "Crawl" to start the crawling process.

3. **View results**:
   - The sitemap will be displayed in both tree view and JSON format.

## Kubernetes Deployment

This project can be deployed on a Kubernetes cluster. Deployment manifests are available in the `kubernetes/` directory.

### Steps to Deploy on Kubernetes

1. **Ensure Kubernetes is set up**:
   - Use Minikube for local testing:
     ```bash
     minikube start --memory=4096 --cpus=2
     ```
   - Or connect to an existing Kubernetes cluster.

2. **Apply Kubernetes manifests**:
   ```bash
   kubectl apply -f kubernetes/
   ```

3. **Verify Deployment**:
   - Check the status of pods:
     ```bash
     kubectl get pods
     ```
   - Port-forward the client service to access the interface:
     ```bash
     kubectl port-forward service/crawler-client 8001:8001
     ```
     Open `http://localhost:8001` in your browser.

4. **Access the Services**:
   - The server is exposed internally within the cluster.
   - The client communicates with the server via the internal Kubernetes service.

### Health Checks

The Kubernetes deployment includes readiness and liveness probes to monitor the health of the services. These are defined in the deployment manifests:

- **Server**: `/healthz` endpoint at port `8000`.
- **Client**: Probes to ensure the service is ready to accept connections.

## Configuration

- **Crawler Settings**: Modify `Crawler/config.yaml` to adjust concurrency, timeout, and max links.
- **Client Settings**: Modify `Crawler/client/client_config.yaml` to adjust server URL, host, and port.


Let me know if you face any issues or have suggestions for improvement!
