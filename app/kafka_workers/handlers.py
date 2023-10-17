from typing import Literal

import xmltodict
from aiokafka import ConsumerRecord
from dicttoxml import dicttoxml
from loguru import logger

from app.crud.users import UsersCRUD
from app.dependencies.db import async_session
from app.kafka_workers.producer import kafka_producer
from app.schemas.general import ResponseStatuses, ConsumerTopics
from app.utils.general_utils import GeneralUtils


class ConsumerHandler:
    @staticmethod
    def display_results_from_kafka(msg: ConsumerRecord) -> None:
        logger.info(f"Got a request to execute msg in {ConsumerTopics.user_results} topic")
        logger.success(f"Result in XML.\n{msg.value.decode('utf-8')}")

    @staticmethod
    async def execute_user_addition_to_database(msg: ConsumerRecord) -> None:
        logger.info(f"Got a request to execute msg in {ConsumerTopics.user_executor} topic")
        xmltodict.parse(
            msg.value,
            process_namespaces=True,
            namespaces={"urn://www.example.com": None},
        )

        input_data = xmltodict.parse(
            msg.value,
            process_namespaces=True,
            namespaces={"urn://www.example.com": None},
        )
        try:
            user = GeneralUtils.transform_xml_bytes_to_user_object(msg)
            async with async_session() as session:
                if await UsersCRUD.get_user_by_email(
                    async_session=session,
                    email=user.email,
                ):
                    raise ValueError(f"Email {user.email} already exists.")
                await UsersCRUD.create_user(
                    async_session=session,
                    user_info=user,
                )
                logger.success(f"Successfully created user. {user=}")
            ConsumerHandler.add_status_into_xml(input_data, ResponseStatuses.SUCCESS)

        except ValueError as e:
            logger.error(
                f"Got an error while executing addition user from kafka. Error: {e}",
            )
            ConsumerHandler.add_status_into_xml(input_data, ResponseStatuses.FAILED)
        finally:
            await kafka_producer.response_with_result_of_user_saving(
                dicttoxml(input_data),
            )
            logger.info(
                f"Consumed: {msg.topic=}; {msg.partition=}; {msg.offset=}; {msg.key=}; {msg.timestamp=};"
                f"\nValue:\n{msg.value.decode('utf-8')}",
            )

    @staticmethod
    def add_status_into_xml(input_data: dict, status: str):
        if input_data.get("Request") and input_data.get("Request"):
            input_data["Request"]["User"].update(Status=status)
