FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    HOME=/tmp \
    STREAMLIT_CONFIG_DIR=/tmp/.streamlit \
    XDG_CACHE_HOME=/tmp/.cache \
    MPLCONFIGDIR=/tmp/matplotlib

RUN useradd -m appuser

WORKDIR /app

COPY requirements.txt ./

RUN pip install --upgrade pip && \
    pip install -r requirements.txt && \
    pip install streamlit

COPY . .

RUN mkdir -p /tmp/.streamlit /tmp/.cache /tmp/matplotlib && \
    cp .streamlit/config.toml /tmp/.streamlit/config.toml && \
    chown -R appuser:0 /app /home/appuser /tmp/.streamlit /tmp/.cache /tmp/matplotlib && \
    chmod -R g=u /app /home/appuser /tmp/.streamlit /tmp/.cache /tmp/matplotlib

USER appuser

EXPOSE 8501

CMD ["sh", "-c", "streamlit run Überblick.py --server.address=0.0.0.0 --server.port=${PORT:-8501}"]
