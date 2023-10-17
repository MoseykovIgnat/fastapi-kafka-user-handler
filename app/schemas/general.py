from dataclasses import dataclass
from enum import StrEnum


@dataclass(frozen=True)
class ResponseStatuses:
    ok: str = "ok"
    posted: str = "posted"
    success: str = "success"
    invalid_xml: str = "invalid XML"
    FAILED: str = "FAILED"
    SUCCESS: str = "SUCCESS"


class ConsumerTopics(StrEnum):
    user_results: str = "user_results"
    user_executor: str = "user_executor"
