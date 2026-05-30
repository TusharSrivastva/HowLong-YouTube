import argparse


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Calculate the total duration of a YouTube Playlist"
    )

    parser.add_argument("url", type=str, help="Youtube Playlist URL")

    parser.add_argument("--start", type=int, default=None, help="Start index (1-based)")

    parser.add_argument("--end", type=int, default=None, help="End index (1-based)")

    parser.add_argument(
        "--exclude",
        type=int,
        nargs="+",
        default=None,
        help="Space-separated list of video indices to exclude (1-based)",
    )

    return parser.parse_args()
