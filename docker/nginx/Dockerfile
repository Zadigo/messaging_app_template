FROM nginx

LABEL "com.nginx.app"="nginx"

COPY ./nginx.conf /etc/nginx/nginx.conf

RUN mkdir etc/nginx/logs/ && \
        touch etc/nginx/logs/error.log && \
        touch etc/nginx/logs/access.log

EXPOSE 8080

CMD [ "nginx", "-g", "daemon off;" ]