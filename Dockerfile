FROM python:latest

RUN apt-get update \
	&& apt-get install -y --no-install-recommends sqlite3 \
	&& rm -rf /var/lib/apt/lists/*

COPY requirements.txt ./
RUN pip install -r requirements.txt gunicorn

WORKDIR /app
COPY . ./

VOLUME /app/static
VOLUME /app/db

EXPOSE 8000
CMD "./docker-entrypoint.sh"
