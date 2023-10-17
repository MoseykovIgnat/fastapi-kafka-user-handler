from dataclasses import dataclass


@dataclass(frozen=True)
class EndpointsTags:
    """Values of endpoints tags"""

    USER_ENDPOINTS = "User endpoints"
    KAFKA_CHECKER_ENDPOINT_TAG = "Kafka checker endpoints"
    SERVICE_ENDPOINT_TAG = "Technical endpoints"
