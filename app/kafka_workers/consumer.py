import asyncio

from aiokafka import AIOKafkaConsumer

from app.core.kafka_settings import get_kafka_settings
from app.kafka_workers.controllers import KafkaUserController
from app.schemas.general import ConsumerTopics


class Consumer:
    def __init__(self):
        self.loop: asyncio.AbstractEventLoop = asyncio.get_running_loop()
        self.consumer_client: AIOKafkaConsumer = AIOKafkaConsumer(
            *(ConsumerTopics.user_executor, ConsumerTopics.user_results),
            bootstrap_servers=get_kafka_settings().instance,
            loop=self.loop,
        )

    async def consume_messages(self):
        await self.consumer_client.start()
        try:
            async for msg in self.consumer_client:
                await KafkaUserController.control_topic(msg)

        finally:
            await self.consumer_client.stop()


kafka_consumer = Consumer()
