import socketio

mgr = socketio.AsyncRedisManager("redis://redis")
sio = socketio.AsyncServer(
    client_manager=mgr,
    async_mode="asgi",
    cors_allowed_origins="*",
)
