FROM python:latest

RUN apt-get update \
	&& apt-get install -y --no-install-recommends sqlite3 \
	&& apt-get clean -y \
	&& rm -rf /var/lib/apt/lists/*

COPY requirements.txt ./
RUN pip install -r requirements.txt gunicorn

WORKDIR /app
COPY . ./

RUN curl -sS https://dl.yarnpkg.com/debian/pubkey.gpg | apt-key add - \
	&& echo "deb https://dl.yarnpkg.com/debian/ stable main" | tee /etc/apt/sources.list.d/yarn.list \
	&& apt-get update \
	&& apt-get install -y --no-install-recommends nodejs yarn \
	&& yarn \
	&& yarn build \
	&& rm -f yarn.lock \
	&& rm -rf node_modules \
	&& rm -rf /usr/local/share/.cache \
	&& apt-get remove -y nodejs yarn \
	&& apt-get autoremove -y \
	&& apt-get clean -y \
	&& rm -rf /var/lib/apt/lists/*

VOLUME /app/static
VOLUME /app/db

EXPOSE 8000
CMD "./docker-entrypoint.sh"
