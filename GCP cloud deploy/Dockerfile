FROM        nginx:stable-alpine3.17-slim

ENV         DEBUG_MESSAGE='Debug Message'

COPY        ./default.conf.template default.conf.template

CMD         ["/bin/sh" , "-c" , "envsubst < /default.conf.template > /etc/nginx/conf.d/default.conf && exec nginx -g 'daemon off;'"]
