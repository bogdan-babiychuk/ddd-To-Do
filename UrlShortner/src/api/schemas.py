from datetime import datetime
from textwrap import shorten
from pydantic import BaseModel, Field

class OriginalUrlRequest(BaseModel):

    original_url: str = Field(examples=["https://example.com"])

class ShortUrlResponse(BaseModel):
    shorten_url: str = Field(..., examples=["https://"])




class StatsResponse(BaseModel):
    short_id: str
    original_url: str
    created_at: datetime
    clicks_count: int
    last_click_at: datetime | None
    ip_addresses: list[str]
