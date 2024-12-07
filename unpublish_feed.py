#!/usr/bin/env python3
# YOU MUST INSTALL ATPROTO SDK
# pip3 install atproto

from atproto import Client, models

from config import PublishFeedConfig as Config


def unpublish():
    client = Client()
    client.login(Config.HANDLE, Config.PASSWORD)

    def main():
        client = Client()
        client.login(Config.HANDLE, Config.PASSWORD)

        feed_did = Config.SERVICE_DID
        if not feed_did:
            feed_did = f'did:web:{Config.HOSTNAME}'

        print(dir(client.com.atproto.repo))

        response = client.com.atproto.repo.list_records(
            data={
                'repo': client.me.did,
                'collection': models.ids.AppBskyFeedGenerator,
                'rkey': Config.RECORD_NAME
            }
        )

        print(response.records)


if __name__ == '__main__':
    unpublish()
