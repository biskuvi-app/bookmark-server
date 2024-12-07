# install atproto first
from atproto import Client, models

# Edit this section. Go to README.md for details

HANDLE: str = 'bookmarks.bskv.site'
PASSWORD: str = '<app-password>'
RECORD_NAME: str = 'bookmarks'
DISPLAY_NAME: str = 'Bookmarks'
DESCRIPTION: str = 'Bookmark feed'
ICON: str = './assets/logo.png'

# Once you are done editing the values above, run this script.

client = Client()
client.login(HANDLE, PASSWORD)


def feed_icon():
    if ICON:
        with open(ICON, 'rb') as f:
            avatar_data = f.read()
            return client.upload_blob(avatar_data).blob
    else:
        return None


response = client.com.atproto.repo.put_record(models.ComAtprotoRepoPutRecord.Data(
    repo=client.me.did,
    collection=models.ids.AppBskyFeedGenerator,
    rkey=RECORD_NAME,
    record=models.AppBskyFeedGenerator.Record(
        did=client.me.did,
        display_name=DISPLAY_NAME,
        description=DESCRIPTION,
        avatar=feed_icon(),
        created_at=client.get_current_time_iso(),
    )
))

print('Successfully published!')
print('Feed URI (put in "BOOKMARKS_URI"):', response.uri)
