from httpx import AsyncClient

BASE_URL = "https://www.googleapis.com/youtube/v3/playlists"


async def get_playlist_metadata(
    playlist_id: str, api_key: str, client: AsyncClient
) -> tuple[str, str]:
    params: dict[str, str] = {"part": "snippet", "id": playlist_id, "key": api_key}

    response = await client.get(BASE_URL, params=params)

    if response.status_code != 200:
        raise RuntimeError(
            f"YouTube API error {response.status_code}: {response.reason_phrase}"
        )

    data = response.json()

    playlist = data["items"][0]

    channel_name = playlist["snippet"]["channelTitle"]
    playlist_title = playlist["snippet"]["title"]

    return playlist_title, channel_name
