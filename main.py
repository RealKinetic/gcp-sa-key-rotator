import logging
import os

import googleapiclient.discovery
from googleapiclient.http import HttpError


def rotate(event, context):
    """Triggered from a message on a Cloud Pub/Sub topic. This will rotate the
    key on a service account by creating and adding a new key to the configured
    service account and, if successful, deleting any existing keys.

    Args:
         event (dict): Event payload.
         context (google.cloud.functions.Context): Metadata for the event.
    """

    service = googleapiclient.discovery.build('iam', 'v1',
                                              cache_discovery=False)
    service_account_email = os.getenv('SERVICE_ACCOUNT_EMAIL')

    # Create a new key for the service account.
    name = 'projects/-/serviceAccounts/' + service_account_email
    key = service.projects().serviceAccounts().keys().create(
        name=name, body={}).execute()
    new_key = key['name']
    logging.info('Created key: {}'.format(new_key))

    # TODO: update usages of the key here.

    # Delete any other existing keys.
    keys = service.projects().serviceAccounts().keys().list(
        name='projects/-/serviceAccounts/' + service_account_email).execute()
    for key in keys['keys']:
        if key['name'] != new_key:
            try:
                service.projects().serviceAccounts().keys().delete(
                    name=key['name']).execute()
                logging.info('Deleted old key: {}'.format(key['name']))
            except HttpError as e:
                # Service accounts can have GCP-managed keys which cannot be
                # deleted. This causes a 400 error on the request, so ignore
                # 400 errors.
                if e.resp.status != 400:
                    raise

    return None
