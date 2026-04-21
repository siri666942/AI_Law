FROM node:22-alpine AS build

WORKDIR /app
COPY frontend/package.json frontend/package-lock.json /app/
RUN npm ci --legacy-peer-deps
COPY frontend /app
RUN npm run build

FROM nginx:1.27-alpine

RUN apk add --no-cache openssl \
  && mkdir -p /etc/nginx/ssl \
  && openssl req -x509 -nodes -days 3650 -newkey rsa:2048 \
    -keyout /etc/nginx/ssl/selfsigned.key \
    -out /etc/nginx/ssl/selfsigned.crt \
    -subj "/CN=lvbao"

COPY deploy/nginx/nginx.conf /etc/nginx/conf.d/default.conf
COPY --from=build /app/dist /usr/share/nginx/html

EXPOSE 80 443
