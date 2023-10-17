from json import JSONDecodeError

from fastapi import APIRouter, Body
from starlette import status

from app.endpoints.settings import EndpointsTags
from app.kafka_workers.producer import kafka_producer
from app.schemas.general import ResponseStatuses, ConsumerTopics

router = APIRouter(
    prefix="/kafka_checker",
    tags=[EndpointsTags.KAFKA_CHECKER_ENDPOINT_TAG],
)


@router.post(
    "/{topic_name}",
    status_code=status.HTTP_200_OK,
    summary="Create new user",
)
async def kafka_produce(topic_name: ConsumerTopics, user=Body(..., media_type="application/xml", openapi_examples={"valid_example":
       {
           "summary": "valid_example",
           "value": "<project><foo>1</foo><bar>2</bar></project>",
   }
})):
    try:
        await kafka_producer.producer_client.send(
            topic=topic_name,
            value=user,
        )
        return {"status": ResponseStatuses.posted}
    except JSONDecodeError:
        return {"status": ResponseStatuses.invalid_XML}
