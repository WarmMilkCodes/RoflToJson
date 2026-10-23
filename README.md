# League of Legends RoflToJson

This Python script reads the player stats (`statsJson`) from League of Legends replay files (.rofl) and shows them as JSON, which you can then save to a file.

## Supported replays

| Patch | Replay format | Supported |
|-------|---------------|-----------|
| Before 14.9 | ROFL (`RIOT\x00\x00`) — metadata after the file header | Yes |
| 14.9 – 14.10 | ROFL2 (`RIOT\x02\x00`) — no metadata in the file | No |
| 14.11 and later | ROFL2 (`RIOT\x02\x00`) — metadata at the end of the file | Yes |

Riot removed the metadata from replays in patch 14.9 and added it back at the end of the file in 14.11, so replays from 14.9 and 14.10 have no stats to read.

Stats are only written when the game finishes, so a replay of a game that didn't end normally may have no player stats.

## Output

For each replay the tool shows the game version, game length (in milliseconds) and, for each player, the stats listed in `keys` in `main.py`:

```json
{
    "gameVersion": "14.21.628.3518",
    "gameLength": 1834123,
    "players": [
        {
            "NAME": "...",
            "ASSISTS": "7",
            "WIN": "Win"
        }
    ]
}
```

Edit the `keys` list in `main.py` to choose which stats are shown.

## Requirements

- Python 3.x
- tkinter

## Usage

```bash
python main.py
```

Click **Open ROFL File** to load a replay, then **Save JSON** to write the output to a file.

## AI disclosure

The original version of this script was written without the use of AI. AI (Claude Code) was used to update the script for the ROFL2 replay format introduced in patch 14.11, and to update this README.
