FROM python:3.11

RUN pip install uv 

WORKDIR /app

# Start this layer separately here to optimize building speed.
COPY pyproject.toml /app
COPY . /app  

RUN uv venv && uv sync 

EXPOSE 8000

CMD ["uv", "run", "gunicorn", "--bind", "0.0.0.0:8000", "run:app"]






