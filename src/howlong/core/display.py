from rich import print

from howlong.utils import format_duration

SPEED_LABELS: list[str] = ["1.0x", "1.25x", "1.50x", "1.75x", "2.00x"]
SPEED_COLORS: list[str] = ["cyan", "cyan2", "bright_green", "green", "green4"]

def display(playlist_title: str, channel_name: str, durations: list[int]) -> None:
    print(f"[bold white]{playlist_title}[/bold white]")
    print(f"[dim white]{channel_name}[/dim white]")
    print()
    print(f"[cyan]Total Duration -> {format_duration(durations[0])}[/cyan]")
    print()
    print("[dim white]At speeds:[/dim white]")

    for label, color, duration in zip(SPEED_LABELS, SPEED_COLORS, durations):
        print(f"[{color}]  {label} -> {format_duration(duration)}[/{color}]")
