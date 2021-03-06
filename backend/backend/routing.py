from channels.routing import ProtocolTypeRouter,URLRouter
from channels.auth import AuthMiddlewareStack

from django.urls import path

from app import consumer


websocket_urlPattern=[
    path('ws/join',consumer.JoinConsumer),
    path('ws/<str:usercode>',consumer.ChatConsumer)
]


application = ProtocolTypeRouter({
    # (http->django views is added by default)
    'websocket': AuthMiddlewareStack(URLRouter(websocket_urlPattern)), 
    

})