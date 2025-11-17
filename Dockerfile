FROM python:3.11.9-slim

# Set the working directory inside the container to /code
# All subsequent commands will be run from here
WORKDIR /code

# Add the virtual environment's bin directory to the PATH so Python tools work globally
ENV PATH="/code/.venv/bin:$PATH"

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# Add the virtual environment's bin directory to the PATH so Python tools work globally
ENV PATH="/code/.venv/bin:$PATH"

COPY "./docker/predict/pyproject.toml" ./

# Install dependencies exactly as locked in uv.lock, without updating them
RUN uv sync

# Copy model

# Copy application code and pipeline into the container
COPY "predict.py" ./
COPY "./models/pipeline.bin" ./models/

# Expose TCP port 9696 so it can be accessed from outside the container
EXPOSE 9696

# Run the application using uvicorn (ASGI server)
# predict:app → refers to 'app' object inside predict.py
# --host 0.0.0.0 → listen on all interfaces
# --port 9696    → listen on port 9696
ENTRYPOINT ["uvicorn", "predict:app", "--host", "0.0.0.0", "--port", "9696"]