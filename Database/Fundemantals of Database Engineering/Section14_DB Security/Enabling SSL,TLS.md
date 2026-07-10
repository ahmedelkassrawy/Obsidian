# Enabling SSL/TLS for PostgreSQL with Docker

## Why Encrypt Database Connections?

**Traditional Excuse**: "Nobody sniffs between web server and database"
- **Reality**: Databases kept close to applications (low latency)
- **Cloud/Kubernetes**: Public networks, **encryption mandatory**

**TLS/SSL Purpose**:
- Encrypt client ↔ database communication
- Protect against network sniffing/interception
- Standard for modern architectures

## Prerequisites

1. **Docker installed** (verify: `docker run hello-world`)
2. Basic understanding of certificates/TLS (optional)

## Step 1: Spin Up PostgreSQL Container

```bash
docker run \
  --name pg-ssl \
  -p 5432:5432 \
  -e POSTGRES_PASSWORD=postgres \
  -d postgres:12
```

**Parameters**:
- `--name pg-ssl`: Container name
- `-p 5432:5432`: Expose PostgreSQL port
- `-e POSTGRES_PASSWORD`: Root password
- `-d postgres:12`: Latest PostgreSQL 12 image

## Step 2: Spin Up pgAdmin (Management UI)

```bash
docker run \
  -e 'PGADMIN_DEFAULT_EMAIL=admin@local' \
  -e 'PGADMIN_DEFAULT_PASSWORD=admin' \
  -p 5555:80 \
  --name pgadmin \
  -d dpage/pgadmin4
```

**Access**: `http://localhost:5555`
- **Login**: `admin@local` / `admin`

## Step 3: Test Unencrypted Connection

1. **Create connection** in pgAdmin:
   - **Name**: `unsecure-pg`
   - **Host**: `localhost` (or Docker network name)
   - **Port**: `5432`
   - **Username**: `postgres`
   - **Password**: `postgres`

2. **Default behavior**: 
   - pgAdmin shows "Prefers SSL" but connects **unencrypted**
   - PostgreSQL doesn't support SSL by default

3. **Force SSL** → **Connection fails**:
   ```
   Error: Server does not support SSL, but SSL was required
   ```

## Step 4: Enable SSL on PostgreSQL

### Access Container
```bash
docker exec -it pg-ssl bash
```

### Install Editor
```bash
apt-get update && apt-get install -y vim
```

### Configure SSL in `postgresql.conf`

**Location**: `/var/lib/postgresql/data/postgresql.conf`

```bash
cd /var/lib/postgresql/data
vim postgresql.conf
```

**Enable SSL**:
```conf
# SSL Settings
ssl = on                    # Enable SSL
ssl_cert_file = 'server.crt'  # Server certificate
ssl_key_file = 'server.key'   # Server private key

# Optional: Cipher and TLS version control
ssl_ciphers = 'HIGH:MEDIUM:+3DES:!aNULL'  # Supported ciphers
ssl_min_protocol_version = 'TLSv1.2'      # Minimum TLS version
```

### Generate Self-Signed Certificate

**Inside container**:
```bash
# Generate 4096-bit RSA key + certificate
openssl req -new -x509 -days 365 -nodes \
  -text -out server.crt \
  -keyout server.key \
  -subj "/C=US/ST=California/L=Temecula/O=HusseinNasser/CN=localhost"
```

**Certificate Details**:
- **Key size**: 4096-bit RSA (2048-bit minimum, but insecure)
- **`-nodes`**: No DES encryption (PostgreSQL can't read password-protected keys)
- **CN=localhost**: Common Name must match connection hostname
- **Validity**: 365 days

### Secure Private Key

```bash
# Set restrictive permissions (owner read/write only)
chmod 600 server.key
chown postgres:postgres server.key server.crt
```

### Restart PostgreSQL
```bash
# Exit container first
exit

# Restart to apply config
docker restart pg-ssl
```

## Step 5: Verify SSL Connection

1. **In pgAdmin**:
   - Edit connection → **Enable "SSL mode: Require"**
   - **Test connection** → ✅ Success!

2. **Connection now encrypted**:
   - TLS handshake established
   - Data encrypted in transit

## Step 6: Control Unencrypted Access

### Server-Side Control
Even with `ssl = on`, unencrypted connections may still work.

**Options**:
1. **Force client certificates** (mutual TLS)
2. **pg_hba.conf restrictions**:
   ```conf
   # /var/lib/postgresql/data/pg_hba.conf
   hostssl all all 0.0.0.0/0 md5  # SSL only
   # host all all 0.0.0.0/0 md5    # (Uncommented = allows non-SSL)
   ```

3. **Client-specific rules** via `pg_hba.conf`

### Client-Side Control
- pgAdmin: Toggle "SSL mode" (Prefer, Require, Verify-CA, Verify-Full)
- `libpq` connection string: `sslmode=require`

## Production Considerations

### Certificate Management
- **Self-signed**: Testing only
- **Production**: Use CA-signed certificates (Let's Encrypt, internal PKI)
- **Renewal**: Automate certificate rotation

### Security Best Practices
```bash
# Strong private key (4096-bit minimum)
openssl genrsa -out server.key 4096

# Restrictive permissions
chmod 600 server.key
chown postgres:postgres server.key

# TLS 1.2+ only
ssl_min_protocol_version = 'TLSv1.2'
```

### Docker Compose Example
```yaml
version: '3.8'
services:
  postgres:
    image: postgres:12
    environment:
      POSTGRES_PASSWORD: postgres
    ports:
      - "5432:5432"
    volumes:
      - ./certs:/var/lib/postgresql/data/certs:ro
      - pgdata:/var/lib/postgresql/data
    command: >
      postgres -c ssl=on
      -c ssl_cert_file=/var/lib/postgresql/data/certs/server.crt
      -c ssl_key_file=/var/lib/postgresql/data/certs/server.key

  pgadmin:
    image: dpage/pgadmin4
    environment:
      PGADMIN_DEFAULT_EMAIL: admin@local
      PGADMIN_DEFAULT_PASSWORD: admin
    ports:
      - "5555:80"

volumes:
  pgdata:
```

**Mount certificates**:
```bash
# Generate certs locally
mkdir certs
openssl req -new -x509 -days 365 -nodes -out certs/server.crt -keyout certs/server.key ...

# Copy to Docker volume or bind mount
```

## Troubleshooting

### Common Errors
1. **"Server does not support SSL"**:
   - `ssl = on` not configured
   - Missing/invalid certificate files
   - Wrong file permissions

2. **"Permission denied"**:
   ```bash
   chmod 600 server.key
   chown postgres:postgres server.*
   ```

3. **Certificate verification fails**:
   - CN mismatch (must be `localhost` or actual hostname)
   - Expired certificate
   - Client set to `Verify-Full` without CA trust

### Verify SSL Status
```sql
-- Connect and run:
SHOW ssl;
-- Returns: on/off

SELECT * FROM pg_stat_ssl;
-- Shows active SSL connections
```

## Key Takeaways

1. **Default PostgreSQL**: No SSL support
2. **Enable via config**: `ssl = on` + certificate files
3. **Self-signed certs**: Fine for testing, use CA-signed in production
4. **File permissions**: `600` for private key, owned by `postgres`
5. **Client control**: `sslmode=require` enforces encryption
6. **Cloud reality**: Encryption mandatory in distributed architectures

## Study Commands

```bash
# Quick SSL-enabled PostgreSQL
docker run -d --name pg-ssl \
  -p 5432:5432 \
  -e POSTGRES_PASSWORD=postgres \
  -v $(pwd)/certs:/certs:ro \
  postgres:12 \
  postgres -c ssl=on -c ssl_cert_file=/certs/server.crt -c ssl_key_file=/certs/server.key

# Generate cert
openssl req -new -x509 -days 365 -nodes -keyout server.key -out server.crt -subj "/CN=localhost"

# Secure files
chmod 600 server.key && chown 999:999 server.*
```

> **Pro Tip**: Always mount certificates as read-only volumes and automate renewal in production. Use internal PKI or Let's Encrypt for CA-signed certificates.