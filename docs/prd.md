# PRD: How Long - YouTube Playlist Duration CLI Tool

## 1. Overview

YouTube users lack a fast and efficient way to calculate the total duration of playlists, especially when filtering or excluding specific videos. Existing web-based tools are slow, require repeated API calls, and introduce unnecessary interaction overhead.

This project proposes a command-line interface (CLI) tool that enables fast retrieval, caching, and slicing of YouTube playlists for duration analysis directly from the terminal.

---

## 2. Problem Statement

Users cannot easily estimate the total watch time of a YouTube playlist with flexible filtering options. Current solutions depend on web applications that require repeated API calls and page reloads for each modification, leading to slow and inefficient workflows.

---

## 3. Goals

### Primary Goals

* Enable fast retrieval of YouTube playlist metadata
* Accurately compute total playlist duration
* Accurately compute total playlist duration at multiple playback speeds (1x, 1.25x, 1.5x, 1.75x, 2x)
* Support filtering and slicing (e.g., exclude videos, range selection)
* Minimize API usage via caching

### Secondary Goals

* Provide a smooth CLI experience
* Support quick experimentation with playlist subsets
* Ensure low-latency responses for repeated queries

---

## 4. Non-Goals

* Building a graphical/web UI
* Downloading videos or media files
* User authentication systems beyond API key usage

---

## 5. Target Users

* Developers who consume educational playlists
* Students managing learning playlists
* Users comfortable with CLI tools

---

## 6. Use Cases / User Stories

### Core Use Cases

* As a user, I want to input a YouTube URL (playlist, playlist ID, or video URL) and quickly see the total duration at different playback speeds (1x, 1.25x, 1.5x, etc.) so I can plan my viewing time efficiently.
* As a user, I want to exclude specific videos from the playlist and recalculate duration.
* As a user, I want to analyze a subset of the playlist (e.g., first 10 videos).
* As a user, I want repeated queries to be fast via cached results.

---

## 7. Functional Requirements

### Playlist Handling

* Accept YouTube playlist input in multiple forms:

  * Full playlist URL
  * Playlist ID directly
  * Video URL that belongs to a playlist (extract playlist ID automatically)
* Fetch all videos in a playlist
* Extract video duration metadata

### Playlist Data Conventions

* Video indices are 1-based for users and 0-based internally for API handling.
* Private, deleted, or unlisted videos are not returned by the YouTube Data API.
* For filtering and slicing, only the selected subset of videos (after exclusions) is used for duration computation.

### Computation

* Compute total playlist duration
* Compute total playlist duration at alternative playback speeds (e.g., 1.25x, 1.5x, 1.75x, 2x)
* Support filtering:

  * exclude video(s) by index
  * include only a range (slice)
* Recompute duration after filtering

### Caching

* Cache playlist metadata locally
* Avoid redundant API calls for previously fetched playlists
* Cache format is Pickle
* Cache invalidation rules:

  * Automatically after 7 days.
  * When exceeding a maximum of 50 playlists, evict the least recently used (LRU).
  * Or manually, if specifically requested by the user.

### CLI Interface

* Simple commands such as:

  * howlong <url>`
  * howlong <url> --start <video_index> --end <video_index> --exclude <video_index>, <video_index>...

### CLI Output Format

* When a playlist is successfully fetched (from API or cache), output should be structured as follows:

```
<Playlist Title>
Total Duration -> <HH:MM>

At speeds:
1.25x -> <HH:MM>
1.5x  -> <HH:MM>
1.75x -> <HH:MM>
2x    -> <HH:MM>
```

---


## 8. Non-Functional Requirements

* Fast response time (sub-second for cached queries)
* Efficient API usage (minimize quota consumption)
* Reliable parsing of YouTube playlist data

---

## 9. System Constraints

* Dependent on YouTube Data API
* API rate limits must be respected
* Network dependency for uncached playlists

---

## 10. Success Metrics

* ≥80% of queries served from cache after initial fetch
* Playlist duration computed in <1s for cached data
* Reduced number of API calls per session compared to baseline web tools
* Positive user feedback on speed and usability
* Ability to handle large playlists (100+ videos) reliably

---

## 11. Assumptions

* Users have access to a YouTube Data API key, if not point to a guide
* Users operate in a terminal environment
* Playlist structure is publicly accessible

---

## 12. Risks & Mitigations

### Risk: API quota exhaustion

* Mitigation: caching

### Risk: Large playlists slow initial fetch

* Mitigation: pagination + async fetching

### Risk: Inconsistent metadata

* Mitigation: validation + fallback handling

### Risk: Interrupted fetch operation

* Mitigation: Exit with error

### Risk: API request failure

* Mitigation: Exponential backoff + limited retries

---

## 13. Future Enhancements (Out of Scope for MVP)

* Integrate Rich Text
* Customizable cache size
* Integrate tqdm
