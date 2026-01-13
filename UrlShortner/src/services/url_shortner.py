from dataclasses import dataclass
from datetime import datetime
import random
import secrets

from aiosqlite import Connection
import string
from UrlShortner.src.api.schemas import OriginalUrlRequest
from UrlShortner.src.requests.requests import UrlRepository

ALPHABET = string.ascii_letters + string.digits


@dataclass
class UrlShortnerService:
    session: Connection

    async def create_short_url(self, original_url:str):
        short_id = self.generate_short_url()
        
        return await UrlRepository().create(session=self.session,
                                      short_id=short_id,
                                      original_url=original_url,
                                      created_at=datetime.utcnow()
                                      )
    async def get_original_link(self, short_id:int):
        return await UrlRepository().get_by_short_id(
            session=self.session,
            short_id=short_id)
    
    async def register_click(self, short_id, ip_address, clicked_at):
        await UrlRepository().record_click(session=self.session,
                                           clicked_at=clicked_at,
                                           short_id=short_id,
                                           ip_address=ip_address)
    async def get_stat(self, short_id):
        return await UrlRepository().get_statistics(short_id)

    @staticmethod
    def generate_short_url():
        length = random.randint(6, 8)
        return "".join(secrets.choice(ALPHABET) for _ in range(length))

