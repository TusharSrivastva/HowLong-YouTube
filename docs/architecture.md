# Architecture: How Long - YouTube Playlist Duration CLI Tool

## Overview

`howlong` is a command-line tool for computing the total duration of a YouTube playlist, with support for slicing, exclusion, playback speed breakdown, and local caching. It is written in Python, packaged for PyPI, and managed with `uv`.

---

## Project Structure

```
howlong/
├── main.py           # Orchestrates the full execution flow
├── cli.py            # Argument parsing (argparse), returns parsed args
├── api/
│   ├── playlist.py   # Fetches video IDs from a YouTube playlist
│   └── videos.py     # Fetches video durations from video IDs
└── core/
    ├── cache.py       # LRU cache with Pickle-based persistence
    ├── config.py      # First-run API key prompt and config.json management
    ├── compute.py     # Duration math, filtering, and speed calculations
    └── display.py     # Terminal output formatting
```

---

## Layer Responsibilities

### `main.py`
The single orchestrator. Calls each layer in sequence and passes data through. Contains no business logic of its own.

### `cli.py`
Single responsibility: parse CLI arguments using `argparse` and return a structured args object. Nothing else.

Supported flags:
```
howlong <url>
howlong <url> --start <n> --end <n> --exclude <n,n,...>
```

### `api/playlist.py`
Calls the YouTube Data API `playlistItems` endpoint. Handles pagination to retrieve all video IDs for a given playlist, regardless of size. Returns a list of video IDs.

### `api/videos.py`
Accepts a list of video IDs and calls the YouTube Data API `videos` endpoint (batched, up to 50 per request) to retrieve duration metadata. Returns a list of `(video_id, duration_seconds)` tuples.

### `core/cache.py`
Manages a Pickle-based local cache stored at `~/.cache/howlong/cache.pkl`.

- **Eviction policy**: LRU, max 50 records
- **TTL**: 7 days per entry
- **Manual invalidation**: supported via flag (future)
- Implemented using `collections.OrderedDict` for O(1) LRU operations

### `core/config.py`
Handles API key management.

- **End users (PyPI)**: On first run, prompts for a YouTube Data API key, validates it, and writes it to `~/.config/howlong/config.json`
- **Developers**: Read from `.env` via `python-dotenv`
- Exposes a single `get_api_key()` function consumed by `main.py`

### `core/compute.py`
Pure functions, no I/O.

- Applies `--start` / `--end` range (1-based user input → 0-based internally)
- Applies `--exclude` (1-based indices → 0-based internally)
- Computes total duration in seconds
- Returns duration at all playback speeds: `1x, 1.25x, 1.5x, 1.75x, 2x`

### `core/display.py`
Formats and prints results to stdout using plain `print`. No external dependencies in MVP.

Output format:
```
<Playlist Title>
Total Duration -> H:MM

At speeds:
  1.25x -> H:MM
  1.50x -> H:MM
  1.75x -> H:MM
  2.00x -> H:MM
```

---

## Data Flow

```
User input (URL + flags)
        │
        ▼
    cli.py          Parse args
        │
        ▼
    main.py         Orchestrate
        │
        ▼
  config.py         Resolve API key
        │
        ▼
  utils/cache.py    Cache lookup
        │
   ┌────┴────┐
  HIT       MISS
   │         │
   │    api/playlist.py   Fetch video IDs (paginated)
   │         │
   │    api/videos.py     Fetch durations (batched)
   │         │
   │    core/cache.py     Store result
   └────┬────┘
        │
        ▼
  core/compute.py   Apply filters → calculate durations
        │
        ▼
  core/display.py   Print output
```

---

## API Design

### YouTube Data API v3

| Module | Endpoint | Purpose |
|---|---|---|
| `playlist.py` | `playlistItems.list` | Retrieve video IDs from a playlist |
| `videos.py` | `videos.list` | Retrieve duration for a batch of video IDs |

- API key is passed via the `key` parameter on every request
- `videos.list` is batched at 50 IDs per request to minimize quota usage
- Pagination is handled via `nextPageToken` in `playlist.py`

### Quota Considerations
- Each `playlistItems.list` page costs 1 unit
- Each `videos.list` batch costs 1 unit
- Caching ensures subsequent runs consume zero quota for previously fetched playlists

---

## Caching

| Property | Value |
|---|---|
| Storage format | Pickle (`.pkl`) |
| Location | `~/.cache/howlong/cache.pkl` |
| Eviction policy | LRU |
| Max records | 50 |
| TTL | 7 days |
| Cache key | Playlist ID |
| Cache value | `{ title, videos: [(id, duration_seconds)], fetched_at }` |

Cache is checked before any API call. On a miss, the full playlist is fetched and stored atomically. Partial results are never cached or displayed.

---

## Index Convention

User-facing indices (via `--start`, `--end`, `--exclude`) are **1-based**. All internal operations use **0-based** indices. Conversion happens once in `core/compute.py` at the boundary.

---

## Error Handling

| Scenario | Behavior |
|---|---|
| Missing API key | Prompt (end user) or raise with `.env` instructions (dev) |
| Invalid playlist URL | Exit with descriptive error message |
| API request failure | Exponential backoff, limited retries, then hard exit |
| Large playlist fetch interrupted | Hard fail, no partial results stored or displayed |
| Private / deleted videos | Omitted by YouTube API; not handled specially |

---

## Packaging

- **Package manager**: `uv`
- **Config**: `pyproject.toml` (no `setup.py`)
- **Entry point**:
  ```toml
  [project.scripts]
  howlong = "howlong.main:main"
  ```
- **Distribution**: PyPI via `uv publish`
- **Lock file**: `uv.lock` committed for reproducible installs

### Dependencies

| Package | Purpose |
|---|---|
| `google-api-python-client` | YouTube Data API v3 |
| `python-dotenv` | `.env` support for developers |

---

## Future Enhancements

- Rich terminal output (`rich` library) replacing plain `print`
- Manual cache invalidation flag (`--refresh`)
- Export results to JSON or CSV
- Support for private playlists via OAuth