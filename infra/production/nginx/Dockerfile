FROM nginx:1.25.3-alpine

RUN rm /etc/nginx/conf.d/default.conf
COPY nginx.conf /etc/nginx/conf.d
COPY ./letsencrypt/live/thewalter.app/fullchain.pem /etc/ssl/certsfullchain.pem
COPY ./letsencrypt/live/thewalter.app/privkey.pem /etc/ssl/certs/privkey.pem