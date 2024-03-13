from fastapi import APIRouter, UploadFile
import aiofiles

router = APIRouter(
    prefix="/images",
    tags=["Uploading images"]
)


@router.post("/hotels", status_code=201)
async def add_hotel_image(name: int, file: UploadFile):
    async with aiofiles.open(f"app/static/images/{name}.webp", "wb+") as file_object:
        contents = await file.read()  # Чтение содержимого загруженного файла
        await file_object.write(contents)  # Запись содержимого в файл
    return {"message": "File downloaded"}

# от автора
# @router.post("/hotels")
# async def add_hotel_image(name: int, file: UploadFile):
#     im_path = f"app/static/images/{name}.webp"
#     with open(im_path, "wb+") as file_object:
#         shutil.copyfileobj(file.file, file_object)
#     process_pic.delay(im_path)