import aiofiles
import aiohttp
import assemblyai as aai


async def upload_file(file_path: str) -> str:
    """Загружает файл на сервер AssemblyAI и возвращает upload_url.

    Args:
        file_path (str): это путь к загружаемому файлу.

    Returns:
        str: URL аудио для транскрибации.
    """
    upload_endpoint = "https://api.assemblyai.com/v2/upload"
    headers = {"authorization": aai.settings.api_key}

    async with aiohttp.ClientSession() as session:
        async with aiofiles.open(file_path, "rb") as f:
            data = await f.read()

        async with session.post(
            upload_endpoint, headers=headers, data=data
        ) as response:
            response.raise_for_status()
            json_response = await response.json()
            return json_response["upload_url"]
