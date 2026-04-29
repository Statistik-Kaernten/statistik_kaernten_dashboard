FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    HOME=/home/appuser \
    STREAMLIT_CONFIG_DIR=/home/appuser/.streamlit

RUN useradd -m appuser

WORKDIR /app

COPY requirements.txt ./

RUN pip install --upgrade pip && \
    pip install -r requirements.txt && \
    pip install streamlit

COPY . .

RUN mkdir -p /home/appuser/.streamlit && \
    chown -R appuser:appuser /home/appuser /app

USER appuser

EXPOSE 8501

CMD ["streamlit", "run", "Überblick.py", "--server.address=0.0.0.0", "--server.port=8501"]
