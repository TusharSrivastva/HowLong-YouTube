from howlong.utils import build_durations_list, compute_speeds


def compute(
    video_durations: dict[str, tuple[int, str]],
    start: int | None = None,
    end: int | None = None,
    exclude: list[int] | None = None,
):
    duration_list: list[int] = build_durations_list(video_durations)

    if start is None:
        start = 1

    if end is None:
        end = len(duration_list) - 1

    total: int = sum(duration_list[start : end + 1])

    if exclude:
        for index in exclude:
            if start <= index <= end:
                total -= duration_list[index]

    return compute_speeds(total)
