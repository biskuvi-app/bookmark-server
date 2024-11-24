# Bookmark Feed Server

## Setup

Install uv and sync:

```shell
pip install uv
uv sync
```

## Publish feed

Open `publish_feed.py`, fill in the variables.

### Run server

Edit variables in `server/config.py`

> **Note**
> To get value for "BOOKMARKS_URI" you should publish the feed first.

Run development flask server:

```shell
uv run flask run
```

Run development server with debug:

```shell
uv run flask --debug run
```

> **Warning**
> Use WSGI in production

Endpoints:

- /.well-known/did.json
- /xrpc/app.bsky.feed.describeFeedGenerator
- /xrpc/app.bsky.feed.getFeedSkeleton

Custom endpoints:  
- /xrpc/app.biskuvi.bookmark.isBookmarked  
  - param:
    - uri (string): `at://<did:plc:...>/app.bsky.feed.post/<postId>`  
  - response:
    - code: `200`
    - body: `{"is_bookmarked": <boolean>}`  
- /xrpc/app.biskuvi.bookmark.addBookmark  
  - param:
      - uri (string): `at://<did:plc:...>/app.bsky.feed.post/<postId>`  
  - response:
    - code: `200`
- /xrpc/app.biskuvi.bookmark.removeBookmark  
  - param:
      - uri (string): `at://<did:plc:...>/app.bsky.feed.post/<postId>`  
  - response:
    - code: `200`  

### License

MIT
