import asyncio

from httpx import AsyncClient

BASE_URL = "https://www.googleapis.com/youtube/v3/playlistItems"
MAX_ITERATIONS = 200
MAX_RESULTS = 50


async def get_video_ids(
    playlist_id: str,
    api_key: str,
    queue: asyncio.Queue[list[tuple[int, str]] | None],
    client: AsyncClient,
) -> None:
    page_token: str | None = None
    iterations: int = 0
    video_index_global: int = 0

    while iterations < MAX_ITERATIONS:
        iterations += 1

        params: dict[str, str | int] = {
            "part": "contentDetails",
            "playlistId": playlist_id,
            "maxResults": MAX_RESULTS,
            "key": api_key,
        }

        if page_token:
            params["pageToken"] = page_token

        response = await client.get(BASE_URL, params=params)

        if response.status_code != 200:
            await queue.put(None)
            raise RuntimeError(
                f"YouTube API error {response.status_code}: {response.reason_phrase}"
            )

        data = response.json()

        video_ids: list[tuple[int, str]] = [
            (video_index_global + idx, item["contentDetails"]["videoId"])
            for idx, item in enumerate(data["items"])
        ]

        video_index_global += len(data["items"])

        await queue.put(video_ids)

        page_token = data.get("nextPageToken")

        if not page_token:
            break

    else:
        await queue.put(None)
        raise RuntimeError("Playlist too long: exceeds 10,000 videos. Aborting.")

    await queue.put(None)
