# gcp-sa-key-rotator

Google Cloud Function for rotating GCP service account keys.

## Deployment

```sh
$ gcloud beta functions deploy sa-key-rotation \
    --env-vars-file env.yaml \
    --runtime python37 \
    --entry-point rotate \
    --trigger-resource sa-rotate \
    --trigger-event google.pubsub.topic.publish
```
