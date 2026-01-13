from datetime import datetime
from src.api.schemas import ShortUrlResponse
from src.db.database import get_connection
from src.requests.entities import Statistics


class UrlRepository:

    async def create(self, session, short_id: str, original_url:str, created_at: datetime):
        await session.execute(
                """
                INSERT INTO shortened_links (short_id, original_url, created_at, clicks_count, last_click_at)
                VALUES (?, ?, ?, 0, NULL)
                """,
                (short_id, str(original_url), created_at.isoformat()),
            )

        return ShortUrlResponse(
            shorten_url=f"https://{short_id}"
        )

    async def get_by_short_id(self, session, short_id: str):
        row = await session.execute(
                """
                SELECT short_id, original_url, created_at, clicks_count, last_click_at
                FROM shortened_links
                WHERE short_id = ?
                """,
                (short_id,),
            ).fetchone()

        if row is None:
            return None


        return row["short_id"]
    
    async def record_click(self, session, clicked_at, short_id, ip_address) -> None:
        cursor = session.execute(
                """
                UPDATE shortened_links
                SET clicks_count = clicks_count + 1,
                    last_click_at = ?
                WHERE short_id = ?
                """,
                (clicked_at.isoformat(), short_id),
            )
        if cursor.rowcount == 0:
            raise KeyError(short_id)

        session.execute(
                """
                INSERT INTO link_clicks (short_id, ip_address, clicked_at)
                VALUES (?, ?, ?)
                """,
                (short_id, ip_address, clicked_at.isoformat()),
            )

    async def get_statistics(self, short_id: str) -> Statistics | None:
        link = self.get_by_short_id(short_id)
        if link is None:
            return None

        with get_connection() as conn:
            rows = conn.execute(
                """
                SELECT ip_address
                FROM link_clicks
                WHERE short_id = ?
                ORDER BY id ASC
                """,
                (short_id,),
            ).fetchall()

        seen: set[str] = set()
        unique_ips: list[str] = []
        for row in rows:
            ip = str(row["ip_address"])
            if ip not in seen:
                unique_ips.append(ip)
                seen.add(ip)

        return Statistics(
            short_id=link.short_id,
            original_url=link.original_url,
            created_at=link.created_at,
            clicks_count=link.clicks_count,
            last_click_at=link.last_click_at,
            ip_addresses=unique_ips,
        )
