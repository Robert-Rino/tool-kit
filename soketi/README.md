# Before deploy
## Create tls secret for soketi namespace
The `certificate.crt` and `private.key` should use our `*.swag.live` cert.
```shell
kubectl create secret tls -n soketi nino.baby \
    --cert=tls/certificate.crt \
    --key=tls/private.key
```

# After deploy
## Test frontend client
Open `index.html` in browser, should see it connect to server,

## Test backend client
Should get correct response, and connect client will receive data.

```python
import pusher

pusher_client = pusher.Pusher(
    '1234', 'some-key', 'some-secret',
    host='nino.baby',
    port=443,
    ssl=True,
)

# Get presence- prefix channel infos
pusher_client.channels_info(u"presence-", [u'user_count'])

# Trigger event
pusher_client.trigger(u'nino-channel', u'my_event', {u'some': u'data'})

```
