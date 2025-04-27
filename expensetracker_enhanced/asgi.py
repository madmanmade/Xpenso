"""
ASGI config for expensetracker_enhanced project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.2/howto/deployment/asgi/
"""

import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from django.urls import path
from expenses.consumers import ExpenseConsumer, CategoryConsumer, BudgetConsumer, StatisticsConsumer

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'expensetracker_enhanced.settings')

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AuthMiddlewareStack(
        URLRouter([
            path("ws/expenses/", ExpenseConsumer.as_asgi()),
            path("ws/categories/", CategoryConsumer.as_asgi()),
            path("ws/budget/", BudgetConsumer.as_asgi()),
            path("ws/statistics/", StatisticsConsumer.as_asgi()),
        ])
    ),
})
