import asyncio

from atomos.core.adapters.messaging import redis_pub_sub_broker

from identity.domain.events import user_events


async def main():
    broker = redis_pub_sub_broker.RedisPubSubBroker()
    for i in range(0, 10):
        await broker.publish('user_created', user_events.UserCreated(f'user{i}', f'user{i}@domain.tld', []))

if __name__ == '__main__':
    asyncio.run(main())
