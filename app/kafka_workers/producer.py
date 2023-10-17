import asyncio

from aiokafka import AIOKafkaProducer

from app.core.kafka_settings import get_kafka_settings
from app.schemas.general import ConsumerTopics


class Producer:
    def __init__(self):
        self.loop: asyncio.AbstractEventLoop = asyncio.get_running_loop()
        self.producer_client: AIOKafkaProducer = AIOKafkaProducer(
            bootstrap_servers=get_kafka_settings().instance,
            loop=self.loop,
        )

    async def response_with_result_of_user_saving(self, response: bytes) -> None:
        await self.producer_client.send(ConsumerTopics.user_results, response)


kafka_producer = Producer()
