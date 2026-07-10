prometheus.yml
```python
global:
  scrape_interval: 15s
  evaluation_interval: 15s

scrape_configs:
  - job_name: 'fastapi'
    static_configs:
      - targets: ['fastapi:8000']
    metrics_path: '/TrhBVe_m5gg2002_E5VVq5'

  - job_name: 'node-exporter'
    static_configs:
      - targets: ['node-exporter:9100']

  - job_name: 'prometheus'
    static_configs:
      - targets: ['prometheus:9090']

  - job_name: 'qdrant'
    static_configs:
      - targets: ['qdrant:6333']
    metrics_path: /metrics

  - job_name: 'postgres'
    static_configs:
      - targets: ['postgres-exporter:9187']
```

in the docker-compose.yml
```python
services:
	prometheus:
	    image: prom/prometheus:v3.5.0
	    container_name: prometheus
	    ports:
	      - "9090:9090"
	    volumes:
	      - prometheus_data:/prometheus
	      - ./prometheus/prometheus.yml:/etc/prometheus/prometheus.yml
	    networks:
	      - backend
	    restart: always
	    command:
	      - '--config.file=/etc/prometheus/prometheus.yml'
	      - '--storage.tsdb.path=/prometheus'
	      - '--web.console.libraries=/etc/prometheus/consoles/libraries'
	      - '--web.console.templates=/etc/prometheus/consoles'
	      - '--web.enable-lifecycle'
	    
volumes:
	prometheus_data
```