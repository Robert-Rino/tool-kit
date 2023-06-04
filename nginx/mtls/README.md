# Create certificate

```shell
openssl req \
  -newkey rsa:4096 \
  -x509 \
  -keyout ca.key \
  -out ca.crt \
  -days 30 \
  -nodes \
  -subj "/CN=my_ca"
```


## Server cert
```shell
openssl req \
  -newkey rsa:4096 \
  -keyout server.key \
  -out server.csr \
  -nodes \
  -days 30 \
  -subj "/CN=localhost"
openssl x509 \
  -req \
  -in server.csr \
  -out server.crt \
  -CA ca.crt \
  -CAkey ca.key \
  -CAcreateserial \
  -days 30
```

## Client cert
```shell
openssl req \
  -newkey rsa:4096 \
  -keyout client.key \
  -out client.csr \
  -nodes \
  -days 30 \
  -subj "/CN=client"
openssl x509 \
  -req \
  -in client.csr \
  -out client.crt \
  -CA ca.crt \
  -CAkey ca.key \
  -CAcreateserial \
  -days 30
```



## Test request
### Curl
```shell
curl https://localhost \
  --cacert ca.crt \
  --key client.key \
  --cert client.crt
```

### Httpie
```shell
http -v https://localhost --cert-key=client.key --cert=client.crt --verify=ca.crt --ssl=tls1.2
```
