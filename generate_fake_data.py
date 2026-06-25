#!/usr/bin/env python3
"""
generate_fake_data.py
Generates fake GT 2019 leaderboard entries and weekly_challenge.json data
to preview the site with Season 1 (complete) + Season 2 in progress.

Run: python generate_fake_data.py
Restore: python generate_fake_data.py --restore
"""

import json
import random
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

LEADERBOARD_FILE = "golden_tee_leaderboard.json"
WEEKLY_FILE = "weekly_challenge.json"
BACKUP_LB = "golden_tee_leaderboard.json.bak"
BACKUP_WC = "weekly_challenge.json.bak"

GAME = "Golden Tee Unplugged 2019"
PAR = 72  # 18-hole par

# Player skill ranges (score vs par integer, lower = better)
PLAYER_SKILL = {
    "vpfiends":      (-15, -9),
    "ed20910":       (-13, -8),
    "Paladin242":    (-11, -7),
    "KeenCobra":     (-10, -5),
    "LynnInDenver":  (-8,  -4),
    "dreaddazzman":  (-7,  -3),
    "intelekt":      (-6,  -2),
    "DaaxPlays":     (-5,  -1),
    "dstructv":      (-4,   0),
}

def fmt_score(n):
    if n == 0: return "E"
    return f"+{n}" if n > 0 else str(n)

def random_dt(start_iso, end_iso):
    start = datetime.fromisoformat(start_iso).replace(tzinfo=timezone.utc)
    end   = datetime.fromisoformat(end_iso).replace(tzinfo=timezone.utc)
    delta = int((end - start).total_seconds())
    offset = random.randint(3600, delta - 7200)
    dt = start + timedelta(seconds=offset)
    return dt.strftime("%d-%m-%Y %H:%M:%S")

def make_entry(player, course, start_iso, end_iso, score_override=None, has_video=False):
    skill = PLAYER_SKILL[player]
    vs_par = score_override if score_override is not None else random.randint(*skill)
    total  = PAR + vs_par
    video_url   = f"https://www.youtube.com/watch?v=fake{player[:3]}" if has_video else None
    video_embed = f"https://www.youtube.com/embed/fake{player[:3]}" if has_video else None
    return {
        "username":      player,
        "game":          GAME,
        "course":        course,
        "score_vs_par":  fmt_score(vs_par),
        "total_score":   str(total),
        "date":          random_dt(start_iso, end_iso),
        "holes":         ["Hole","1","2","3","4","5","6","7","8","9","10","11","12","13","14","15","16","17","18"],
        "pars":          [4,4,3,5,4,3,4,5,4,4,3,5,4,4,3,5,4,4],
        "players":       [{"name": player, "scores": [4]*18}],
        "youtube_video": video_url,
        "youtube_embed": video_embed,
        "scraped_at":    end_iso + "Z",
    }

# ── Week definitions ──────────────────────────────────────────────────────────
# (course, start_iso, end_iso, season, season_week, [(player, score, has_video)])
WEEKS = [
    # ── Season 1 ──
    {
        "course": "Alpine Run", "season": 1, "season_week": 1,
        "start": "2026-06-26T16:00:00", "end": "2026-07-03T16:00:00",
        "players": [
            ("vpfiends",    -13, True),
            ("ed20910",     -11, False),
            ("Paladin242",   -9, False),
            ("KeenCobra",    -7, False),
            ("dreaddazzman", -5, False),
        ],
    },
    {
        "course": "Antelope Pass", "season": 1, "season_week": 2,
        "start": "2026-07-03T16:00:00", "end": "2026-07-10T16:00:00",
        "players": [
            ("ed20910",      -12, True),
            ("vpfiends",     -11, False),
            ("LynnInDenver",  -8, False),
            ("Paladin242",    -7, False),
            ("KeenCobra",     -5, False),
            ("dreaddazzman",  -3, False),
        ],
    },
    {
        "course": "Bear Lodge", "season": 1, "season_week": 3,
        "start": "2026-07-10T16:00:00", "end": "2026-07-17T16:00:00",
        "players": [
            ("vpfiends",    -14, True),
            ("Paladin242",  -10, False),
            ("KeenCobra",    -9, False),
            ("ed20910",      -8, False),
            ("intelekt",     -4, False),
        ],
    },
    {
        "course": "Celtic Shores", "season": 1, "season_week": 4,
        "start": "2026-07-17T16:00:00", "end": "2026-07-24T16:00:00",
        "players": [
            ("Paladin242",   -11, False),
            ("KeenCobra",    -10, False),
            ("vpfiends",      -9, False),
            ("ed20910",       -7, True),
            ("LynnInDenver",  -5, False),
            ("dreaddazzman",  -3, False),
        ],
    },
    {
        "course": "Desert Valley Resort", "season": 1, "season_week": 5,
        "start": "2026-07-24T16:00:00", "end": "2026-07-31T16:00:00",
        "players": [
            ("ed20910",      -13, True),
            ("vpfiends",     -12, False),
            ("dreaddazzman",  -9, False),
            ("DaaxPlays",     -6, False),
            ("intelekt",      -4, False),
            ("dstructv",      -2, False),
        ],
    },
    {
        "course": "Grand Canyon", "season": 1, "season_week": 6,
        "start": "2026-07-31T16:00:00", "end": "2026-08-07T16:00:00",
        "players": [
            ("vpfiends",     -15, True),
            ("KeenCobra",    -11, False),
            ("ed20910",      -10, False),
            ("Paladin242",    -8, False),
            ("LynnInDenver",  -6, False),
            ("dstructv",      -3, False),
        ],
    },
    # ── Season 2 ──
    {
        "course": "Hawthorne Manor", "season": 2, "season_week": 1,
        "start": "2026-08-07T16:00:00", "end": "2026-08-14T16:00:00",
        "players": [
            ("ed20910",      -12, True),
            ("vpfiends",     -11, False),
            ("Paladin242",    -9, False),
            ("KeenCobra",     -7, False),
            ("LynnInDenver",  -5, False),
        ],
    },
    # Week 8 = Season 2 Week 2 = CURRENT (partial entries)
    {
        "course": "Juniper Falls", "season": 2, "season_week": 2,
        "start": "2026-08-14T16:00:00", "end": "2026-08-21T16:00:00",
        "players": [
            ("vpfiends",    -12, False),
            ("Paladin242",   -9, False),
            ("dreaddazzman", -6, False),
        ],
    },
]

CURRENT_WEEK = WEEKS[-1]
COMPLETED_WEEKS = WEEKS[:-1]


def build_history():
    history = []
    for w in reversed(COMPLETED_WEEKS):
        sorted_players = sorted(w["players"], key=lambda x: x[1])
        results = []
        for rank, (player, score, _) in enumerate(sorted_players, 1):
            results.append({
                "rank": rank,
                "player": player,
                "score_vs_par": fmt_score(score),
                "total_score": str(PAR + score),
                "date": datetime.fromisoformat(w["start"])
                            .strftime(f"%b {random.randint(1,6) + datetime.fromisoformat(w['start']).day}"),
            })
        history.insert(0, {
            "week_start":   w["start"][:10],
            "course":       w["course"],
            "game":         GAME,
            "season":       w["season"],
            "season_week":  w["season_week"],
            "start":        w["start"],
            "end":          w["end"],
            "results":      results,
            "winner":       sorted_players[0][0],
        })
    # Newest first
    history.reverse()
    return history


def build_standings(weeks):
    s = {}
    for w in weeks:
        sorted_players = sorted(w["players"], key=lambda x: x[1])
        for rank, (player, _, _) in enumerate(sorted_players, 1):
            if player not in s:
                s[player] = {"wins": 0, "top3": 0, "played": 0}
            s[player]["played"] += 1
            if rank == 1: s[player]["wins"] += 1
            if rank <= 3: s[player]["top3"] += 1
    return s


def champion(standings):
    if not standings: return None
    return max(standings.items(), key=lambda x: (x[1]["wins"], x[1]["top3"]))[0]


def main():
    if "--restore" in sys.argv:
        for src, dst in [(BACKUP_LB, LEADERBOARD_FILE), (BACKUP_WC, WEEKLY_FILE)]:
            if Path(src).exists():
                Path(dst).write_text(Path(src).read_text(encoding="utf-8"), encoding="utf-8")
                print(f"Restored {dst}")
            else:
                print(f"No backup found: {src}")
        return

    random.seed(42)

    # ── Backup originals ──
    for src, dst in [(LEADERBOARD_FILE, BACKUP_LB), (WEEKLY_FILE, BACKUP_WC)]:
        Path(dst).write_text(Path(src).read_text(encoding="utf-8"), encoding="utf-8")
    print("Backed up originals (.bak files)")

    # ── Leaderboard: remove old GT 2019 fakes, add new ones ──
    with open(LEADERBOARD_FILE, encoding="utf-8") as f:
        lb = json.load(f)

    lb = [e for e in lb if e.get("game") != GAME]
    fake_entries = []
    for w in WEEKS:
        for player, score, has_video in w["players"]:
            fake_entries.append(make_entry(player, w["course"], w["start"], w["end"], score, has_video))

    lb = fake_entries + lb
    with open(LEADERBOARD_FILE, "w", encoding="utf-8") as f:
        json.dump(lb, f, indent=2, ensure_ascii=False)
    print(f"Leaderboard: added {len(fake_entries)} GT 2019 entries ({len(lb)} total)")

    # ── weekly_challenge.json ──
    with open(WEEKLY_FILE, encoding="utf-8") as f:
        wc = json.load(f)

    season1_weeks = [w for w in COMPLETED_WEEKS if w["season"] == 1]
    season2_weeks = [w for w in COMPLETED_WEEKS if w["season"] == 2]

    s1_standings = build_standings(season1_weeks)
    s2_standings = build_standings(season2_weeks)
    all_standings = build_standings(COMPLETED_WEEKS)

    # Merge with existing GT 2018 standings
    for player, data in wc.get("standings", {}).items():
        if player not in all_standings:
            all_standings[player] = data
        else:
            all_standings[player]["wins"]   += data["wins"]
            all_standings[player]["top3"]   += data["top3"]
            all_standings[player]["played"] += data["played"]

    history = build_history()
    # Prepend to existing GT 2018 history
    existing_history = [h for h in wc.get("history", []) if h.get("game") != GAME]
    history = history + existing_history

    wc["season_config"] = {"first_season_start": "2026-06-26", "weeks_per_season": 6}
    wc["current_season"] = {"number": 2, "week": 2}
    wc["season_standings"] = s2_standings
    wc["seasons"] = [
        {
            "number": 1,
            "weeks": 6,
            "champion": champion(s1_standings),
            "standings": s1_standings,
        }
    ]
    wc["standings"] = all_standings
    wc["history"] = history
    wc["used_courses_2019"] = [w["course"] for w in WEEKS]
    wc["current"] = {
        "course":        CURRENT_WEEK["course"],
        "game":          GAME,
        "game_year":     "2019",
        "season":        CURRENT_WEEK["season"],
        "season_week":   CURRENT_WEEK["season_week"],
        "start":         CURRENT_WEEK["start"],
        "end":           CURRENT_WEEK["end"],
        "deadline_text": "Friday, August 21st @ 12:00 PM ET",
    }

    with open(WEEKLY_FILE, "w", encoding="utf-8") as f:
        json.dump(wc, f, indent=2, ensure_ascii=False)

    print(f"weekly_challenge.json updated:")
    print(f"  Season 1 complete — champion: {champion(s1_standings)}")
    print(f"  Season 2 Week 1 complete — winner: {sorted(season2_weeks[0]['players'], key=lambda x:x[1])[0][0]}")
    print(f"  Current: Season 2 Week 2 — {CURRENT_WEEK['course']} ({len(CURRENT_WEEK['players'])} entries so far)")
    print(f"  History: {len(history)} total weeks")
    print()
    print("To restore originals: python generate_fake_data.py --restore")


if __name__ == "__main__":
    main()
