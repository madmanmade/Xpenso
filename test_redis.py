import os
import django
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
import asyncio

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'expensetracker_enhanced.settings')
django.setup()

async def test_redis_connection():
    try:
        # Get the default channel layer (Redis)
        channel_layer = get_channel_layer()
        
        # Test sending a message
        await channel_layer.group_add("test_group", "test_channel")
        await channel_layer.group_send(
            "test_group",
            {
                "type": "test.message",
                "text": "Hello Redis!"
            }
        )
        
        print("✅ Successfully connected to Redis!")
        print("✅ Successfully sent test message!")
        
        # Cleanup
        await channel_layer.group_discard("test_group", "test_channel")
        
    except Exception as e:
        print("❌ Error connecting to Redis:", str(e))

if __name__ == "__main__":
    asyncio.run(test_redis_connection()) 