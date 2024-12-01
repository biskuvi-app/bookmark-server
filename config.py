# noinspection SpellCheckingInspection
class Config:
    HOSTNAME = "biskuvibookmark.pythonanywhere.com"
    SERVICE_DID = "did:plc:qvmvynssslo5yhstrnc2cwv6"
    BOOKMARKS_URI = f"at://{SERVICE_DID}/app.bsky.feed.generator/bookmarks"
    GIT_REPO_URL = "https://biskuvi-app.github.io"
    BOOKMARKS_DIR = "repo_bookmarks"
    LOGS_DIR = "logs"


# Go to README.md for details
class PublishFeedConfig:
    # login
    HANDLE: str = 'biskuvi-bookmark.bsky.social'
    PASSWORD: str = 'zyiq-3r73-joku-4zbm'
    # server
    HOSTNAME: str = 'biskuvibookmark.pythonanywhere.com'
    SERVICE_DID: str = ''
    # feed info
    RECORD_NAME: str = 'bookmarks'
    DISPLAY_NAME: str = 'Bookmarks'
    DESCRIPTION: str = 'Bookmark feed by Biskuvi. Please log in to account to see the correct feed.'
    AVATAR_PATH: str = './assets/biscuit-flat.png'
