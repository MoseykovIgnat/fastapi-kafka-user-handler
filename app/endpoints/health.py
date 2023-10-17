from fastapi import APIRouter

from app.endpoints.settings import EndpointsTags
from app.schemas.general import ResponseStatuses

router = APIRouter(prefix="/healthz", tags=[EndpointsTags.SERVICE_ENDPOINT_TAG])


@router.get(
    "",
    summary="Health check of whole processing pipeline",
    description="Health check including test call of machine learning module",
    response_model=dict,
)
def health() -> dict:
    return {"status": ResponseStatuses.ok}
