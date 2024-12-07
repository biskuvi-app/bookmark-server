# noinspection SpellCheckingInspection
class Config:
    HOSTNAME = "bookmarks.bskv.site"
    SERVICE_DID = "did:plc:qvmvynssslo5yhstrnc2cwv6"
    BOOKMARKS_URI = f"at://{SERVICE_DID}/app.bsky.feed.generator/bookmarks"
    GIT_REPO_URL = "https://biskuvi-app.github.io"
    BOOKMARKS_DIR = "repo_bookmarks"
    LOGS_DIR = "logs"


# Go to README.md for details
class PublishFeedConfig:
    # login
    HANDLE: str = 'bookmarks.bskv.site'
    PASSWORD: str = '<app-password>'
    # server
    HOSTNAME: str = 'bookmarks.bskv.site'
    SERVICE_DID: str = 'did:plc:qvmvynssslo5yhstrnc2cwv6'
    # feed info
    RECORD_NAME: str = 'bookmarks'
    DISPLAY_NAME: str = 'Bookmarks'
    DESCRIPTION: str = 'Bookmark feed'
    AVATAR_PATH: str = './assets/logo.png'
