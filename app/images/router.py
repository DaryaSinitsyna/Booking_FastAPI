from fastapi import APIRouter, UploadFile
import aiofiles

from app.tasks.tasks import process_pic

router = APIRouter(
    prefix="/images",
    tags=["Uploading images"]
)


@router.post("/hotels", status_code=201)
async def add_hotel_image(name: int, file: UploadFile):
    im_path = f"app/static/images/{name}.webp"
    async with aiofiles.open(im_path, "wb+") as file_object:
        contents = await file.read()  # Чтение содержимого загруженного файла
        await file_object.write(contents)  # Запись содержимого в файл
    process_pic.delay(im_path)
    return {"message": "File downloaded"}
