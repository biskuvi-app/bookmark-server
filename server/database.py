import os
import sqlite3
from datetime import datetime

BOOKMARKS_DIR = "repo_bookmarks"
CURSOR_EOF = 'eof'
EMPTY_FEED = {'cursor': CURSOR_EOF, 'feed': []}


class BookmarkError(BaseException):
    pass


# not intended to be used externally as each init will create a database per DID
class Bookmarks:
    def __init__(self, did: str):
        if not did.startswith("did:plc:"):
            raise BookmarkError("Invalid repo DID")

        db_id = did.split("did:plc:")[1]
        if not db_id.isalnum():
            raise BookmarkError("Invalid non-alphanumeric repo DID")

        self.con = sqlite3.connect(f"{BOOKMARKS_DIR}/{db_id}")
        self.cur = self.con.cursor()
        self.cur.execute(
            "CREATE TABLE IF NOT EXISTS post(id INTEGER PRIMARY KEY, uri TEXT NOT NULL UNIQUE)"
        )

    def is_bookmarked(self, uri: str):
        sql = "SELECT COUNT(*) > 0 FROM post WHERE uri='?' LIMIT 1"
        res = self.cur.execute(sql, (uri,))
        return res.fetchone() is not None

    def add_bookmark(self, uri: str):
        self.cur.execute("INSERT OR IGNORE INTO post VALUES(?)", (uri,))
        self.con.commit()

    def remove_bookmark(self, uri: str):
        self.cur.execute("DELETE FROM post WHERE uri='?' LIMIT 1", (uri,))

    def get_bookmarks(self, cursor: str | None = None, limit=50):
        # reached end
        if cursor == CURSOR_EOF:
            return EMPTY_FEED

        # default bsky limit
        if limit > 100:
            limit = 100

        # select from cursor
        if cursor:
            int_cursor = int(cursor, 10)
            self.cur.execute("SELECT id, uri FROM post WHERE id < ? LIMIT ?", (int_cursor, limit))
        else:
            self.cur.execute("SELECT id, uri FROM post LIMIT ?", (limit,))

        items = self.cur.fetchall()
        if len(items) > 1:
            feed = [{'post': item[0]} for item in items]
            return {'cursor': str(items[-1][0]), 'feed': feed}
        else:
            return EMPTY_FEED

    def __exit__(self):
        self.con.close()


class Databases:
    def __init__(self) -> None:
        self.databases: dict[str, Bookmarks] = {}
        os.makedirs(BOOKMARKS_DIR, exist_ok=True)

    def _get_database(self, did: str) -> Bookmarks:
        if did not in self.databases:
            self.databases[did] = Bookmarks(did)
        return self.databases[did]

    def get_bookmarks(self, did: str, cursor: str, limit: str) -> dict[str, str | list]:
        if did not in self.databases:
            return EMPTY_FEED
        self._get_database(did).get_bookmarks(cursor, limit)

    def is_bookmarked(self, did: str, uri: str) -> bool:
        self._get_database(did).is_bookmarked(uri)

    def add_bookmark(self, did: str, uri: str):
        self._get_database(did).add_bookmark(uri)

    def remove_bookmark(self, did: str, uri: str):
        self._get_database(did).remove_bookmark(uri)
