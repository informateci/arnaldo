import os

PORT = int(os.environ.get("HTTP_PORT"))
SERVER = os.environ.get("IRC_SERVER")
CHAN = os.environ.get("IRC_CHAN")
NICK = os.environ.get("IRC_NICK")
PASSWORD = os.environ.get("IRC_PASSWORD")
SLISTEN = os.environ.get("HTTP_SLISTEN")
imgur_client_id = os.environ.get("imgur_client_id")
imgur_client_secret = os.environ.get("imgur_client_secret")
REDIS = os.environ.get("REDIS", "localhost")
