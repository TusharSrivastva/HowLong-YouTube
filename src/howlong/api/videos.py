import asyncio

from httpx import AsyncClient

BASE_URL = "https://www.googleapis.com/youtube/v3/videos"


async def get_video_durations(
    api_key: str,
    queue: asyncio.Queue[list[tuple[int, str]] | None],
    client: AsyncClient,
) -> dict[str, tuple[int, str]]:

    video_durations: dict[str, tuple[int, str]] = {}

    while True:
        batch: list[tuple[int, str]] | None = await queue.get()

        if batch is None:
            break

        id_to_index: dict[str, int] = {video_id: index for index, video_id in batch}

        params: dict[str, str] = {
            "part": "contentDetails",
            "id": ",".join(id_to_index.keys()),
            "key": api_key,
        }

        response = await client.get(url=BASE_URL, params=params)

        if response.status_code != 200:
            raise RuntimeError(
                f"YouTube API error {response.status_code}: {response.reason_phrase}"
            )

        data = response.json()

        for item in data["items"]:
            video_id: str = item["id"]
            duration: str = item["contentDetails"]["duration"]
            video_durations[video_id] = (id_to_index[video_id], duration)

    return video_durations
