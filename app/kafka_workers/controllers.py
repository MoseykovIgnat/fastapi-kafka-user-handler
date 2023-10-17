from aiokafka import ConsumerRecord
from loguru import logger
from app.kafka_workers.handlers import ConsumerHandler
from app.schemas.general import ConsumerTopics


class KafkaUserController:
    @staticmethod
    async def control_topic(msg: ConsumerRecord):
        match msg.topic:
            case ConsumerTopics.user_results:
                ConsumerHandler.display_results_from_kafka(msg=msg)
            case ConsumerTopics.user_executor:
                await ConsumerHandler.execute_user_addition_to_database(msg=msg)
            case _:
                logger.warning("Another topic was read")
