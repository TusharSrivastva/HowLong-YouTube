import asyncio

from httpx import AsyncClient

BASE_URL = "https://www.googleapis.com/youtube/v3/videos"


async def get_video_durations(
    api_key: str, queue: asyncio.Queue[list[str] | None], client: AsyncClient
) -> list[tuple[str, str]]:

    results: list[tuple[str, str]] = []

    while True:
        batch: list[str] | None = await queue.get()

        if batch is None:
            break

        params: dict[str, str] = {
            "part": "contentDetails",
            "id": ",".join(batch),
            "key": api_key,
        }

        response = await client.get(url=BASE_URL, params=params)

        if response.status_code != 200:
            raise RuntimeError(
                f"YouTube API error {response.status_code}: {response.reason_phrase}"
            )

        data = response.json()

        results.extend(
            [(item["id"], item["contentDetails"]["duration"]) for item in data["items"]]
        )

    return results
