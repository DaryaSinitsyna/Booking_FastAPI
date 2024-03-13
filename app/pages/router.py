from fastapi import APIRouter, Request, Depends
from fastapi.templating import Jinja2Templates

from app.hotels.router import get_hotels_by_location_name_date

router = APIRouter(
    prefix="/pages",
    tags=["Frontend"]
)

templates = Jinja2Templates(directory="app/templates")


@router.get("/hotels")
async def get_hotels_pages(
        request: Request,
        hotels=Depends(get_hotels_by_location_name_date)
):
    return templates.TemplateResponse(name="hotels.html", context={"request": request, "hotels": hotels})
