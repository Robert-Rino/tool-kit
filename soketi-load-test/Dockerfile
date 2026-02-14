FROM grafana/k6:latest

WORKDIR /scripts

COPY loadtest.js ./

CMD ["run", "loadtest.js"]
