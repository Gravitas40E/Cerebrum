from __future__ import annotations

import random
from datetime import date, timedelta

from database.manager import Database
from services.data_service import NoteService, FolderService

DB_PATH = None  # use default ~/.cerebrum/cerebrum.db

TITLES = [
    "Project roadmap for Q3",
    "Meeting notes: design review",
    "Reading list on distributed systems",
    "Daily log: deep work summary",
    "Architecture decision record #12",
    "Research: attention mechanisms",
    "Sprint retrospective notes",
]

BODIES = [
    "## Goals\n- Ship auth module\n- Improve search latency by 20%",
    "### Discussion\nAgreed on moving the graph queries behind a service boundary.",
    "- Designing Data-Intensive Applications\n- papers on Raft/Paxos variants",
    "Completed 3 focused blocks. Main blocker: infra access.",
    "Chose SQLite WAL mode for local-first durability instead of client-server DB.",
    "Notes on transformers, sparse attention, and routing mixtures.",
    "Done: dashboard refresh; Next: tag filtering UX.",
]

TAGS_POOL = [
    ["engineering", "planning"],
    ["meeting", "design"],
    ["research", "reading"],
    ["daily-log"],
    ["architecture"],
    ["research", "ai"],
    ["retrospective", "sprint"],
]

ROOT = "c:\\Workspace\\cerebrum"


def main() -> None:
    db = Database(DB_PATH)
    notes = NoteService(db)
    folders = FolderService(db)

    folder_ids: list[int] = []
    for name in ["Work", "Projects", "Research"]:
        folder_ids.append(folders.create_folder(name))

    for idx in range(7):
        tag_names = TAGS_POOL[idx]
        note_id = notes.create_note(
            title=TITLES[idx],
            body=BODIES[idx],
            folder_id=random.choice(folder_ids + [None]),
        )
        if idx % 3 == 0:
            notes.update_note(note_id, is_pinned=1)
        if idx % 4 == 0:
            notes.update_note(note_id, is_favorite=1)
        if idx % 5 == 0:
            notes.update_note(note_id, is_brain_vault=1)
        notes.set_note_tag_names(note_id, tag_names)

    # Create a couple of extra notes specifically for daily log view/screenshots
    for day_offset in range(3):
        day = (date.today() - timedelta(days=day_offset)).isoformat()
        notes.get_or_create_daily_log(day)
        # Touch it to make recent activity more interesting
        existing = notes.get_daily_log(day)
        if existing:
            notes.update_note(existing.id, body=f"# {day}\n\n- Logged progress")

    db.close()
    print("Populated notes and folders.")


if __name__ == "__main__":
    main()
