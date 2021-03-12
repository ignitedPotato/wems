FROM node AS builder
WORKDIR /app
COPY . ./
RUN yarn \
	&& yarn build \
	&& rm -rf node_modules \
	&& rm -f yarn.lock


FROM python:alpine
RUN apk add --no-cache sqlite

COPY requirements.txt ./
RUN pip install -r requirements.txt gunicorn

WORKDIR /app
COPY --from=builder /app ./

VOLUME /app/static
VOLUME /app/db

EXPOSE 8000
CMD ["./docker-entrypoint.sh"]
