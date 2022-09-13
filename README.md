Create a Google Cloud Function running this command in the same line:
```
# Deploy a **NEW** project to cloud functions
gcloud functions deploy telegram_bot --set-env-vars "TELEGRAM_TOKEN=<TELEGRAM_TOKEN>" --runtime python38 --trigger-http --project=<project_name>
```
you can also specify the region by appending the following string to the previous command
```
--region=<region_name>
```
[list of the available regions](https://cloud.google.com/compute/docs/regions-zones)

Some details:

* Here webhook is the name of the function in the `main.py` file
* You need to specify your Telegram token with the `--set-env-vars` option
* `--runtime python38` describe the environment used by our function, Python 3.8 in this case
* `--trigger-http` is the type of trigger associated to this function, you can find here the complete list of triggers
The above command will return something like this:
  
Step three, you need to set up your Webhook URL using this API call:
```
# Set a webhook for sending messages updates from update_queue
foo@bar:~$ curl "https://api.telegram.org/bot<TELEGRAM_TOKEN>/setWebhook?url=<URL>"
```


Utilities & useful commands:

```
# Add your Project ID to ENV variable
foo@bar:~$ export PROJECT_ID=<PROJECT_ID>
```

```
# Get info on webhook (such as pending updates and errors):
foo@bar:~$ https://api.telegram.org/botYOUR_TOKEN/getWebhookInfo
```
```
# Re-Deploy new code to the function
gcloud functions deploy telegram_bot --runtime python38 --trigger-http --project=$PROJECT_ID
```

