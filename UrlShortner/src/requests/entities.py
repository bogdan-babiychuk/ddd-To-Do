
from dataclasses import dataclass
from datetime import datetime



@dataclass(frozen=True, slots=True)
class Statistics:
    short_id: str
    original_url: str
    created_at: datetime
    clicks_count: int
    last_click_at: datetime | None
    ip_addresses: list[str]
