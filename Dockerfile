FROM python:3.12-alpine

WORKDIR /neolockout
COPY . .
RUN pip install uv --break-system-packages
RUN uv venv && source .venv/bin/activate 
RUN uv sync
COPY .env .env
RUN source .env
CMD ["uv", "run", "main.py"]
