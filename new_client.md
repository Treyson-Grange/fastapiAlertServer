# New Client Instructions

# Table of Contents

-   [API Key](#api-key)
-   [Client Keys](#client-keys)
-   [Requests](#requests)
-   [Tips and Tricks for Alerts](#tips-and-tricks-for-alerts)

## API Key

USU Alert box requires multiple things in order to interact with it. Each client shall have a unique key, allowing for a more secure box.

### Generate Key

To generate a key for your new Client, you will have to run the script `/scripts/create_api_key.py` It is run through the terminal as so: `python create_api_key.py <api_key> <client_name> <perm1,perm2,perm3>`

-   api_key: We prefer a character count of 64, if you need a command to get one, use this: `dd if=<(cat /dev/urandom | base32 - | tr -d '\n') bs=1 of=>(wl-copy) count=64` (copies to your clipboard)
-   client_name: The name of the client, e.g., usuNoc, usuGul4, etc.
-   perm1,perm2,perm3: The client permissions. At this point, the only permissions are `create`, `delete`, and `read`.

Running this script will insert this new client API key into the database.

## Client Keys

Client keys must be stored securely. They shall never be seen in a git commit, or exposed to any front end.

This means that api keys should live in BW, ideally stored in the note under the name `alert_box_api_key`. This will make it easy on our `rotate_keys.py` script, which will update the keys to BW directly, only needing a reload to get the keys in place.

## Requests

To perform a request to the alert box, you must include different headers depending on the situation.

All requests require the following Headers:

-   Access-Control-Allow-Origin: \*
-   Content-Type: application/json
-   API-Key: ClientAPIKey

To perform a GET request you need to include the USU-Group with the others, corresponding the the group you want alerts from.

Acknowledging an alert, has 2 endpoints, depending on the type of alert. One for auto alerts, the other for manual alerts. Both endpoints accept an alert ID in the format `delete/{id}`.

Creating an alert also has 2 separate endpoints.

The `/create` endpoint requires a JSON object that includes message, criticality, autoClear, clearAfter, and the alert group.

The `/create-manual` endpoint requires a JSON object that includes a dueDate, daysNotice, a message, and a group.

## Tips and tricks for Alerts

Don't include a timestamp when you create an auto alert, unless you need the timestamp to not be right now. If we receive a date that does not follow the correct format, it will break all GET requests.

For an example of how to interact with the alert box, see [nx-usunoc](https://github.com/utahstate/nx-usunoc).
