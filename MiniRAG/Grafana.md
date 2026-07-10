in the docker-compose.yml
```python
services:
	grafana:
	    image: grafana/grafana:11.6.0-ubuntu
	    container_name: grafana
	    ports:
	      - "3000:3000"
	    volumes:
	      - grafana_data:/var/lib/grafana
	    env_file:
	      - ./envi/.env.grafana
	    depends_on:
	      - prometheus
	    networks:
	      - backend
	    restart: always
    
volumes:
	grafana_data:
```

.env.grafana
```python
GF_SECURITY_ADMIN_PASSWORD = 
GF_SECURITY_ADMIN_USER = 
GF_USERS_ALLOW_SIGN_UP = 
```