FROM python:3.11
RUN apt-get update && apt-get install -y \
    libgirepository1.0-dev \
    libcairo2-dev \
    libdbus-1-dev \
    libdbus-glib-1-dev \
    pkg-config \
    python3-dev \
    libffi-dev \
    libxml2-dev \
    libxslt-dev \
    libssl-dev \
    build-essential \
    gcc \
    gobject-introspection \
    && apt-get clean
ENV PKG_CONFIG_PATH=/usr/lib/x86_64-linux-gnu/pkgconfig:/usr/lib/pkgconfig:/usr/local/lib/pkgconfig
WORKDIR /app
COPY requirements.txt /app/
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt
EXPOSE 8000
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
