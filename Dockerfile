FROM python:3.12-slim
WORKDIR /benchmark
COPY pyproject.toml ./
COPY src/ ./src/
COPY tests/ ./tests/
RUN pip install --no-cache-dir -e '.[test]'
CMD ["pytest", "-q"]
