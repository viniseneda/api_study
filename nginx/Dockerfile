FROM nginx:latest

COPY nginx.conf /etc/nginx/nginx.conf
COPY certificate.pem /etc/nginx/certificate.pem
COPY key.pem /etc/nginx/key.pem

ENTRYPOINT ["nginx"]
CMD ["-g", "daemon off;"]
