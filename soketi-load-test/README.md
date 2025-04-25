# Soketi load test
Use k6/ws test soketi server

envars:
- CLIENT_COUNT = Stress test client count
- PUSHER_CHANNELS = Pusher channel names client will connect, space separete string
- PUSHER_APP_KEY = Pusher app key
- PUSHER_WH_HOST = Pusher host
- PUSHER_AUTHORIZATION_ENDPOINT = Pusher authorization endpoint

# Run test
`docker compose up`
