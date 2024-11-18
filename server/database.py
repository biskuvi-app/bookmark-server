import os
import sqlite3

BOOKMARKS_DIR = "repo_bookmarks"


class BookmarkError(BaseException):
    pass


class Bookmarks:
    def __init__(self, did: str):
        if not did.startswith("did:plc:"):
            raise BookmarkError("Invalid repo DID")

        db_id = did.split("did:plc:")[1]
        if not db_id.isalnum():
            raise BookmarkError("Invalid non-alphanumeric repo DID")

        self.con = sqlite3.connect(f"{BOOKMARKS_DIR}/{db_id}")
        self.cur = self.con.cursor()
        self.cur.execute("CREATE TABLE IF NOT EXISTS post(uri)")

    def is_bookmarked(self, uri: str):
        res = self.cur.execute("SELECT uri FROM post WHERE uri='?' LIMIT 1", (uri,))
        return res.fetchone() is not None

    def add_bookmark(self, uri: str):
        self.cur.execute("INSERT INTO post VALUES(?)", (uri,))
        self.con.commit()

    def remove_bookmark(self, uri: str):
        self.cur.execute("DELETE FROM post WHERE uri='?' LIMIT 1", (uri,))

    def __exit__(self):
        self.con.close()


class Databases:
    def __init__(self) -> None:
        self.databases: dict[str, Bookmarks] = {}
        os.makedirs(BOOKMARKS_DIR, exist_ok=True)

    def repo_bookmarks(self, did: str) -> Bookmarks:
        if did not in self.databases:
            self.databases[did] = Bookmarks(did)
        return self.databases[did]
