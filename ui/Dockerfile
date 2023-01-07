FROM node:18-alpine as client-build
WORKDIR /client

RUN echo 'Starting Frontend Build...'

COPY . .

RUN npm install
RUN npm run build


RUN echo "Starting NGINX server..."

FROM nginx
COPY --from=client-build /client/build /usr/share/nginx/html
COPY nginx.conf /etc/nginx/conf.d/default.conf
