#!/usr/bin/env python3
# YOU MUST INSTALL ATPROTO SDK
# pip3 install atproto

from atproto import Client, models

from config import PublishFeedConfig as Config


def publish():
    client = Client()
    client.login(Config.HANDLE, Config.PASSWORD)

    feed_did = Config.SERVICE_DID or f'did:web:{Config.HOSTNAME}'

    avatar_blob = None
    if Config.AVATAR_PATH:
        with open(Config.AVATAR_PATH, 'rb') as f:
            avatar_data = f.read()
            avatar_blob = client.upload_blob(avatar_data).blob

    response = client.com.atproto.repo.put_record(models.ComAtprotoRepoPutRecord.Data(
        repo=client.me.did,
        collection=models.ids.AppBskyFeedGenerator,
        rkey=Config.RECORD_NAME,
        record=models.AppBskyFeedGenerator.Record(
            did=feed_did,
            display_name=Config.DISPLAY_NAME,
            description=Config.DESCRIPTION,
            avatar=avatar_blob,
            created_at=client.get_current_time_iso(),
        )
    ))

    print('Successfully published!')
    print('Feed URI (put in "BOOKMARKS_URI"):', response.uri)


if __name__ == '__main__':
    publish()
