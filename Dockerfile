ARG PYTHON_VERSION=3.13-slim

FROM python:${PYTHON_VERSION}

# --- START MODIFICATION ---

# Install necessary build tools and headers for NumPy, SciPy, etc.
# 'build-essential' provides gcc/g++ and 'gfortran' is often needed for SciPy/NumPy.
RUN apt-get update -y && \
    apt-get install -y --no-install-recommends \
    build-essential \
    gfortran && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# --- END MODIFICATION ---

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN mkdir -p /code

WORKDIR /code

COPY requirements.txt /tmp/requirements.txt
RUN set -ex && \
    pip install --upgrade pip && \
    pip install -r /tmp/requirements.txt && \
    rm -rf /root/.cache/
COPY . /code

ENV SECRET_KEY "n0sKVzTa1fWbTyireO8bMy4ulhBiK9jxe6NhTbASq9cvdEz7sF"
RUN python manage.py collectstatic --noinput

EXPOSE 8000

CMD ["gunicorn","--bind",":8000","--workers","2","myproject.wsgi"]