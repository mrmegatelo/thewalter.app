FROM node:23-alpine

WORKDIR /app

COPY ./frontend/package.json ./package.json
COPY ./frontend/package-lock.json ./package-lock.json

RUN npm i

ENTRYPOINT ["npm", "run"]