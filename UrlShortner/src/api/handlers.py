from typing import Annotated
from aiosqlite import Connection
from fastapi import APIRouter, status, Depends, HTTPException, Request
from fastapi.responses import RedirectResponse
from src.api.utils import get_client_ip, utcnow
from src.api.schemas import OriginalUrlRequest, StatsResponse
from src.services.url_shortner import UrlShortnerService
from src.db.database import get_connection
router = APIRouter()


@router.post("/shortner", status_code=status.HTTP_201_CREATED)
async def create_short_url(
    data: OriginalUrlRequest,
    session: Annotated[Connection, Depends(get_connection)]
):  
    try:
        short_url= await UrlShortnerService(session).create_short_url(data.original_url)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail={
                "error": str(e)
            }
        )
    return short_url

@router.get("/{short_id}", status_code=status.HTTP_200_OK)
async def redirect(short_id: int,
                   request: Request,
                   session: Annotated[Connection, Depends(get_connection)]):
    try:
        link = await UrlShortnerService(session).get_original_link(short_id=short_id)
        if link is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="short_id not found")
        
        clicked_at = utcnow()
        ip_address = get_client_ip(request)
        await UrlShortnerService(session).register_click(short_id, ip_address, clicked_at)

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail={
                "error": str(e)
            }
        )
    return RedirectResponse(url=f"https://{link}", status_code=status.HTTP_302_FOUND)


@router.get("/stats/{short_id}", response_model=StatsResponse)
def stats(short_id: str,
          session: Annotated[Connection, Depends(get_connection)]):
    statistics = UrlShortnerService(session).get_statistics(short_id)
    if statistics is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="short_id not found")

    return StatsResponse(
        short_id=statistics.short_id,
        original_url=str(statistics.original_url),
        created_at=statistics.created_at,
        clicks_count=statistics.clicks_count,
        last_click_at=statistics.last_click_at,
        ip_addresses=statistics.ip_addresses,
    )
