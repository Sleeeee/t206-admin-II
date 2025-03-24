FROM nginx:latest

RUN mkdir -p /var/www/html/blog

COPY nginx.conf /etc/nginx/nginx.conf
COPY www_index.html /var/www/html/www/index.html
COPY blog_index.html /var/www/html/blog/index.html
