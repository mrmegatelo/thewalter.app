FROM nginx:1.25.3-alpine

RUN rm /etc/nginx/conf.d/default.conf
COPY ./infra/production/nginx/nginx.conf /etc/nginx/conf.d