import re


def parse_duration(duration: str) -> int:
    pattern = r"PT(?:(\d+)H)?(?:(\d+)M)?(?:(\d+)S)?"
    match = re.fullmatch(pattern, duration)

    if not match:
        raise ValueError(f"Invalid ISO 8601 duration: {duration}")

    hours: int = int(match.group(1) or 0)
    minutes: int = int(match.group(2) or 0)
    seconds: int = int(match.group(3) or 0)

    return hours * 3600 + minutes * 60 + seconds


def build_durations_list(video_durations: dict[str, tuple[int, str]]) -> list[int]:
    duration_list = [0] * (len(video_durations) + 1)

    for item in video_durations.values():
        duration_list[item[0]] = parse_duration(item[1])

    return duration_list


def compute_speeds(total: int) -> list[int]:
    speeds: list[float] = [1.0, 1.25, 1.5, 1.75, 2.0]

    return [int(total / speed) for speed in speeds]
