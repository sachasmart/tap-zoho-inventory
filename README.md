# tap-zoho-inventory

`tap-zoho-inventory` is a Singer tap for zoho-inventory.

Built with the [Meltano Tap SDK](https://sdk.meltano.com) for Singer Taps.

## Installation

- [ ] `Developer TODO:` Update the below as needed to correctly describe the install procedure. For instance, if you do not have a PyPi repo, or if you want users to directly install from your git repo, you can modify this step as appropriate.

```bash
pipx install tap-zoho-inventory
```

## Configuration

## Zoho Inventory

1. [Zoho Inventory API Docs](https://www.zoho.com/inventory/api/v1/#introduction)
2. Its a fairly annoying API to work with given the OAuth2 authorization. However, once a `refresh_token` is acquired it is somewhat straight forward. 1. To get a `refresh_token` (non-expiring token used to get `access_tokens`) you need to create a `code`. Visit: [Zoho API Console](https://api-console.zoho.com/client/1000.QZFPBX41GSLI12U9ASGDXSBKWFLT0F) and enter: 
    1. `ZohoInventory.FullAccess.all` for both "Scope" and "Scope Description". May as well up the time duration to 10 minutes. Run the follow command to get `access_token` and `refresh_token` with the code (replace `{{code}}`, `{{redirect_uri}}`, `{{client_id}}`, `{{client_secret}}` with the values from the API Console)
      ```bash
           curl --location 'https://accounts.zoho.com/oauth/v2/token' \
        --header 'Content-Type: application/x-www-form-urlencoded' \
        --data-urlencode 'code={{code}}' \
        --data-urlencode 'redirect_uri={{redirect_uri}}' \
        --data-urlencode 'client_id={{client_id}}' \
        --data-urlencode 'client_secret={{client_secret}}' \
        --data-urlencode 'grant_type=authorization_code' \
        --data-urlencode 'scope=ZohoInventory.FullAccess.all'
      ```
      3. Take the `refresh_token` and add run `meltano config tap-zoho-inventory set --interactive`. Set token values as needed (`refresh_token` and `access_token`).
1. To view all the parameters for a `tap` run `meltano select <tap> --list --all`
1. To invoke the tap (don't push data to a `loader`), run `meltano invoke tap-zoho-inventory` and the data will be outputted to `./output/out.jsonl`

### Accepted Config Options

- [ ] `Developer TODO:` Provide a list of config options accepted by the tap.

A full list of supported settings and capabilities for this
tap is available by running:

```bash
tap-zoho-inventory --about
```

### Configure using environment variables

This Singer tap will automatically import any environment variables within the working directory's
`.env` if the `--config=ENV` is provided, such that config values will be considered if a matching
environment variable is set either in the terminal context or in the `.env` file.

### Source Authentication and Authorization

- [ ] `Developer TODO:` If your tap requires special access on the source system, or any special authentication requirements, provide those here.

## Usage

You can easily run `tap-zoho-inventory` by itself or in a pipeline using [Meltano](https://meltano.com/).

### Executing the Tap Directly

```bash
tap-zoho-inventory --version
tap-zoho-inventory --help
tap-zoho-inventory --config CONFIG --discover > ./catalog.json
```

## Developer Resources

- [ ] `Developer TODO:` As a first step, scan the entire project for the text "`TODO:`" and complete any recommended steps, deleting the "TODO" references once completed.

### Initialize your Development Environment

```bash
pipx install poetry
poetry install
```

### Create and Run Tests

Create tests within the `tap_zoho_inventory/tests` subfolder and
then run:

```bash
poetry run pytest
```

You can also test the `tap-zoho-inventory` CLI interface directly using `poetry run`:

```bash
poetry run tap-zoho-inventory --help
```

### Testing with [Meltano](https://www.meltano.com)

_**Note:** This tap will work in any Singer environment and does not require Meltano.
Examples here are for convenience and to streamline end-to-end orchestration scenarios._

Your project comes with a custom `meltano.yml` project file already created. Open the `meltano.yml` and follow any _"TODO"_ items listed in
the file.

Next, install Meltano (if you haven't already) and any needed plugins:

```bash
# Install meltano
pipx install meltano
# Initialize meltano within this directory
cd tap-zoho-inventory
meltano install
```

Now you can test and orchestrate using Meltano:

```bash
# Test invocation:
meltano invoke tap-zoho-inventory --version
# OR run a test `elt` pipeline:
meltano elt tap-zoho-inventory target-jsonl
```

### SDK Dev Guide

See the [dev guide](https://sdk.meltano.com/en/latest/dev_guide.html) for more instructions on how to use the SDK to
develop your own taps and targets.
