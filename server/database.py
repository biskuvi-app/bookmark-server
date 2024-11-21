import os
import sqlite3

BOOKMARKS_DIR = "repo_bookmarks"
CURSOR_EOF = 'eof'
EMPTY_FEED = {'cursor': CURSOR_EOF, 'feed': []}


class BookmarkError(Exception):
    pass


class BookmarkRepository:

    def __init__(self, did: str):
        if not did.startswith("did:plc:"):
            raise BookmarkError("Invalid repo DID")

        db_id = did.split("did:plc:")[1]
        if not db_id.isalnum():
            raise BookmarkError("Invalid non-alphanumeric repo DID")

        self.con = sqlite3.connect(f"{BOOKMARKS_DIR}/{db_id}")
        self.cur = self.con.cursor()
        self._create_table()

    def _create_table(self):
        self.cur.execute(
            "CREATE TABLE IF NOT EXISTS post(id INTEGER PRIMARY KEY, uri TEXT NOT NULL UNIQUE)"
        )
        self.con.commit()

    def is_bookmarked(self, uri: str) -> bool:
        sql = "SELECT COUNT(*) FROM post WHERE uri = ? LIMIT 1"
        res = self.cur.execute(sql, (uri,))
        return res.fetchone()[0] > 0

    def add_bookmark(self, uri: str):
        try:
            self.cur.execute("INSERT OR IGNORE INTO post(uri) VALUES(?)", (uri,))
            self.con.commit()
        except sqlite3.Error as e:
            raise BookmarkError(f"Failed to add bookmark: {e}")

    def remove_bookmark(self, uri: str):
        try:
            self.cur.execute("DELETE FROM post WHERE uri = ? LIMIT 1", (uri,))
            self.con.commit()
        except sqlite3.Error as e:
            raise BookmarkError(f"Failed to remove bookmark: {e}")

    def get_bookmarks(self, cursor: str | None = None, limit: int = 50) -> dict:
        if limit > 100:
            limit = 100

        if cursor == CURSOR_EOF:
            return EMPTY_FEED

        try:
            if cursor:
                int_cursor = int(cursor, 10)
                self.cur.execute(
                    "SELECT id, uri FROM post WHERE id < ? ORDER BY id DESC LIMIT ?",
                    (int_cursor, limit)
                )
            else:
                self.cur.execute(
                    "SELECT id, uri FROM post ORDER BY id DESC LIMIT ?",
                    (limit,)
                )

            items = self.cur.fetchall()

            if items:
                feed = [{'post': item[1]} for item in items]
                return {
                    'cursor': str(items[-1][0]),
                    'feed': feed
                }
            else:
                return EMPTY_FEED
        except sqlite3.Error as e:
            raise BookmarkError(f"Failed to retrieve bookmarks: {e}")

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.con.close()


class BookmarkManager:
    def __init__(self):
        os.makedirs(BOOKMARKS_DIR, exist_ok=True)
        self._repositories: dict[str, BookmarkRepository] = {}

    def _get_repository(self, did: str) -> BookmarkRepository:
        if did not in self._repositories:
            self._repositories[did] = BookmarkRepository(did)
        return self._repositories[did]

    def get_bookmarks(self, did: str, cursor: str | None = None, limit: int = 50) -> dict:
        try:
            return self._get_repository(did).get_bookmarks(cursor, limit)
        except BookmarkError:
            return EMPTY_FEED

    def is_bookmarked(self, did: str, uri: str) -> bool:
        return self._get_repository(did).is_bookmarked(uri)

    def add_bookmark(self, did: str, uri: str):
        self._get_repository(did).add_bookmark(uri)

    def remove_bookmark(self, did: str, uri: str):
        self._get_repository(did).remove_bookmark(uri)


bookmark_manager = BookmarkManager()
