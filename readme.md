See me in action [@ToddlerDon](https://twitter.com/ToddlerDon)! Inspired by [this tweet](https://twitter.com/bessbell/status/1296121107129360384).

Prepends `Mommy, ` to the beginning of each of Trump's tweets. If a tweet's last word is in all caps, appends ` WAAAHHH!` to the end.

Run as `python toddlerifier.py`. For testing purposes, you can set it to follow a different account by adding that account's handle as a command-line argument: `python toddlerifier.py <handle>`

To authenticate with Twitter's API, expects the following environment variables to exist:
* `API_KEY`
* `API_KEY_SECRET`
* `ACCESS_TOKEN`
* `ACCESS_TOKEN_SECRET`
