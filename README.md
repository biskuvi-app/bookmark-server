# Bookmark Feed Server

## Setup

Install uv and sync:

```shell
pip install uv
uv sync
```

## Publish feed

Open `publish_feed.py`, fill in the variables.

### Hints  

HANDLE  
> YOUR bluesky handle
> Ex: user.bsky.social

PASSWORD  
> YOUR bluesky password, or preferably an App Password (found in your client settings)
> Ex: abcd-1234-efgh-5678

HOSTNAME  
> The hostname of the server where feed server will be hosted
> Ex: feed.bsky.dev

RECORD_NAME  
> A short name for the record that will show in urls
> Lowercase with no spaces.
> Ex: whats-hot

DISPLAY_NAME  
> A display name for your feed
> Ex: What's Hot

DESCRIPTION (Optional)  
>  A description of your feed
> Ex: Top trending content from the whole network

AVATAR_PATH (Optional)  
>  The path to an image to be used as your feed's avatar
> Ex: ./path/to/avatar.jpeg

SERVICE_DID (Optional)  
> Only use this if you want a service did different from did:web

## Run server

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
  - description: checks if uri exists in bookmarks
  - method: GET
  - param:
    - uri (string): `at://<did:plc:...>/app.bsky.feed.post/<postId>`  
  - response:
    - code: `200`
    - body: `{"is_bookmarked": <boolean>}`  
- /xrpc/app.biskuvi.bookmark.arePostsBookmarked  
  - description: checks if uris exist in bookmarks, returns only uris of bookmarked posts  
  - method: POST
  - body:
    - uris (string[]): `[at://<did:plc:...>/app.bsky.feed.post/<postId>, ...]`  
  - response:
    - code: `200`
    - uris (string[]): `[at://<did:plc:...>/app.bsky.feed.post/<postId>, ...]`
- /xrpc/app.biskuvi.bookmark.addBookmark  
  - description: add post uri to bookmarks  
  - param:
      - uri (string): `at://<did:plc:...>/app.bsky.feed.post/<postId>`  
  - response:
    - code: `200`
- /xrpc/app.biskuvi.bookmark.removeBookmark  
  - description: remove post uri from bookmarks  
  - param:
      - uri (string): `at://<did:plc:...>/app.bsky.feed.post/<postId>`  
  - response:
    - code: `200`  

### License

MIT
