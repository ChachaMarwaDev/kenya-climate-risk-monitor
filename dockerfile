FROM python:3.11-slim

# Install uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

# Install dlt with bigquery extras
RUN uv pip install dlt[bigquery] --system

# Copy pipeline scripts into the image
COPY extraction/ /app/extraction/
COPY data/ /app/data/

# Copy secrets where dlt will find them
RUN mkdir -p /var/dlt
COPY extraction/.dlt/secrets.toml /var/dlt/secrets.toml