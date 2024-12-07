# install atproto first
from atproto import Client, models

# Edit this section

HANDLE: str = 'bookmarks.bskv.site'
PASSWORD: str = '<app-password>'
RECORD_NAME: str = 'bookmarks'

# Once you are done editing the values above, run this script.

at_client = Client()
at_client.login(HANDLE, PASSWORD)

response = at_client.com.atproto.repo.delete_record(
    data={
        'repo': at_client.me.did,
        'collection': models.ids.AppBskyFeedGenerator,
        'rkey': RECORD_NAME
    }
)
print(response)
