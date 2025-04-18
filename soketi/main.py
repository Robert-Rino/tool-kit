import pusher

pusher_client = pusher.Pusher(
    '1234', 'some-key', 'some-secret',
    host='nino.baby',
    port=443,
    ssl=True,
)

# Get presence- prefix channel infos
pusher_client.channels_info(u"nino-", [u'user_count'])

# Trigger event
pusher_client.trigger(u'nino-channel', u'my_event', {u'some': u'data'})
