# AA Fleet Pings<a name="aa-fleet-pings"></a>

[![Version](https://img.shields.io/pypi/v/aa-fleetpings?label=release)](https://pypi.org/project/aa-fleetpings/)
[![License](https://img.shields.io/github/license/ppfeufer/aa-fleetpings)](https://github.com/ppfeufer/aa-fleetpings/blob/master/LICENSE)
[![Python](https://img.shields.io/pypi/pyversions/aa-fleetpings)](https://pypi.org/project/aa-fleetpings/)
[![Django](https://img.shields.io/pypi/djversions/aa-fleetpings?label=django)](https://pypi.org/project/aa-fleetpings/)
![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)
[![pre-commit.ci status](https://results.pre-commit.ci/badge/github/ppfeufer/aa-fleetpings/master.svg)](https://results.pre-commit.ci/latest/github/ppfeufer/aa-fleetpings/master)
[![Code Style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](http://black.readthedocs.io/en/latest/)
[![Discord](https://img.shields.io/discord/790364535294132234?label=discord)](https://discord.gg/zmh52wnfvM)
[![Checks](https://github.com/ppfeufer/aa-fleetpings/actions/workflows/automated-checks.yml/badge.svg)](https://github.com/ppfeufer/aa-fleetpings/actions/workflows/automated-checks.yml)
[![codecov](https://codecov.io/gh/ppfeufer/aa-fleetpings/branch/master/graph/badge.svg?token=9I6HQB6W6J)](https://codecov.io/gh/ppfeufer/aa-fleetpings)
[![Translation status](https://weblate.ppfeufer.de/widget/alliance-auth-apps/aa-fleetpings/svg-badge.svg)](https://weblate.ppfeufer.de/engage/alliance-auth-apps/)
[![Contributor Covenant](https://img.shields.io/badge/Contributor%20Covenant-2.1-4baaaa.svg)](https://github.com/ppfeufer/aa-fleetpings/blob/master/CODE_OF_CONDUCT.md)

[![ko-fi](https://ko-fi.com/img/githubbutton_sm.svg)](https://ko-fi.com/N4N8CL1BY)

App for Alliance Auth that can format your fleet pings and ping for you to
Discord.

______________________________________________________________________

<!-- mdformat-toc start --slug=github --maxlevel=6 --minlevel=2 -->

- [Screenshots](#screenshots)
  - [View in Alliance Auth](#view-in-alliance-auth)
  - [Discord Ping Examples](#discord-ping-examples)
    - [Pre-Ping](#pre-ping)
    - [Formup: NOW](#formup-now)
- [Installation](#installation)
  - [Bare Metal Installation](#bare-metal-installation)
    - [Step 1: Install the App](#step-1-install-the-app)
    - [Step 2: Update Your AA Settings](#step-2-update-your-aa-settings)
    - [Step 3: Finalizing the Installation](#step-3-finalizing-the-installation)
  - [Docker Installation](#docker-installation)
    - [Step 1: Add the App](#step-1-add-the-app)
    - [Step 2: Update Your AA Settings](#step-2-update-your-aa-settings-1)
    - [Step 3: Build Auth and Restart Your Containers](#step-3-build-auth-and-restart-your-containers)
    - [Step 4: Finalizing the Installation](#step-4-finalizing-the-installation)
  - [Common Setup Steps](#common-setup-steps)
    - [Permission Setup](#permission-setup)
    - [App Setup](#app-setup)
- [Updating](#updating)
  - [Bare Metal Installation](#bare-metal-installation-1)
  - [Docker Installation](#docker-installation-1)
- [Configuration](#configuration)
  - [Use Default Fleet Types](#use-default-fleet-types)
  - [Use Default Ping Targets](#use-default-ping-targets)
  - [Use Doctrines From Fittings Module](#use-doctrines-from-fittings-module)
  - [Webhook Verification](#webhook-verification)
  - [Default Embed Color](#default-embed-color)
- [Changelog](#changelog)
- [Translation Status](#translation-status)
- [Contributing](#contributing)

<!-- mdformat-toc end -->

______________________________________________________________________

## Screenshots<a name="screenshots"></a>

### View in Alliance Auth<a name="view-in-alliance-auth"></a>

![View in Alliance Auth](https://raw.githubusercontent.com/ppfeufer/aa-fleetpings/master/docs/images/aa-view.jpg "View in Alliance Auth")

### Discord Ping Examples<a name="discord-ping-examples"></a>

#### Pre-Ping<a name="pre-ping"></a>

![Discord Ping Example: Pre-Ping](https://raw.githubusercontent.com/ppfeufer/aa-fleetpings/master/docs/images/discord-ping.jpg "Discord Ping Example: Pre-Ping")

#### Formup: NOW<a name="formup-now"></a>

![Discord Ping Example: Formup NOW](https://raw.githubusercontent.com/ppfeufer/aa-fleetpings/master/docs/images/discord-ping-formup-now.jpg "Discord Ping Example: Formup NOW")

## Installation<a name="installation"></a>

This app is a plugin for Alliance Auth. If you don't have Alliance Auth running already,
please install it first before proceeding. (See the official [AA installation guide]
for details)

> [!NOTE]
>
> You also want to make sure that you have the
> [Discord service](https://allianceauth.readthedocs.io/en/latest/features/services/discord.html)
> installed, configured and activated before installing this app.

### Bare Metal Installation<a name="bare-metal-installation"></a>

#### Step 1: Install the App<a name="step-1-install-the-app"></a>

Make sure you're in the virtual environment (venv) of your Alliance Auth installation.
Then install the latest version:

```bash
pip install aa-fleetpings==3.7.1
```

#### Step 2: Update Your AA Settings<a name="step-2-update-your-aa-settings"></a>

Configure your AA settings (`local.py`) as follows:

- Add `'fleetpings',` to `INSTALLED_APPS`

#### Step 3: Finalizing the Installation<a name="step-3-finalizing-the-installation"></a>

Copy static files and run migrations

```bash
python manage.py collectstatic
python manage.py migrate
```

Restart your supervisor services for AA

Continue with the [common setup](#common-setup-steps) steps below.

### Docker Installation<a name="docker-installation"></a>

#### Step 1: Add the App<a name="step-1-add-the-app"></a>

Add the app to your `conf/requirements.txt`:

```text
aa-fleetpings==3.7.1
```

#### Step 2: Update Your AA Settings<a name="step-2-update-your-aa-settings-1"></a>

Configure your AA settings (conf/local.py) as follows:

- Add `'fleetpings',` to `INSTALLED_APPS`

#### Step 3: Build Auth and Restart Your Containers<a name="step-3-build-auth-and-restart-your-containers"></a>

Run the following commands from your AA project directory (the one that contains `docker-compose.yml`):

```shell
docker compose build --no-cache
docker compose --env-file=.env up -d
```

#### Step 4: Finalizing the Installation<a name="step-4-finalizing-the-installation"></a>

Copy static files and run migrations

```shell
docker compose exec allianceauth_gunicorn bash

auth collectstatic
auth migrate
```

Continue with the [common setup](#common-setup-steps) steps below.

### Common Setup Steps<a name="common-setup-steps"></a>

#### Permission Setup<a name="permission-setup"></a>

Now you can set up permissions in Alliance Auth for your users.
Add `fleetpings | aa fleetpings | Can access this app` to the states and/or
groups you would like to have access.

#### App Setup<a name="app-setup"></a>

In your admin backend you'll find a new section called `Fleet Pings`.
This is where you set all your stuff up, like the webhooks you want to ping and who
can ping them, fleet types, comms, formup locations, and so on. It's pretty straight
forward, so you shouldn't have any issues. Go nuts!

## Updating<a name="updating"></a>

### Bare Metal Installation<a name="bare-metal-installation-1"></a>

To update your existing installation of AA Discord Ping Formatter, first enable your
virtual environment.

Then run the following commands from your AA project directory (the one that
contains `manage.py`).

```bash
pip install aa-fleetpings==3.7.1

python manage.py collectstatic
python manage.py migrate
```

Finally, restart your AA supervisor services.

### Docker Installation<a name="docker-installation-1"></a>

To update your existing installation of AA Fleet Pings, all you need to do is to update the respective line in your `conf/requirements.txt` file to the latest version.

```text
aa-fleetpings==3.7.1
```

Now rebuild your containers:

```shell
docker compose build --no-cache
docker compose --env-file=.env up -d
```

After that, run the following commands to update your database and static files:

```shell
docker compose exec allianceauth_gunicorn bash

auth collectstatic
auth migrate
```

## Configuration<a name="configuration"></a>

The following settings are available in the Django Admin Backend under
`/admin/fleetpings/setting/`:

### Use Default Fleet Types<a name="use-default-fleet-types"></a>

Enable or disable the default fleet types (Roaming, Home Defense, StratOP, and CTA)
that are shown in the fleet type dropdown in addition to your own.

**Default:** True

### Use Default Ping Targets<a name="use-default-ping-targets"></a>

Enable or disable the default ping targets (@everyone and @here) that are shown in
the ping target dropdown in addition to your own.

**Default:** True

### Use Doctrines From Fittings Module<a name="use-doctrines-from-fittings-module"></a>

If you have the [Fittings and Doctrines] module installed, and your doctrines
configured there, you don't have to re-build your doctrine list for this module. You
can simply use the doctrines you already have configured in the Fittings and
Doctrines module.

**Default:** True

### Webhook Verification<a name="webhook-verification"></a>

If you require your pings to be sent to a webhook, that is not a standard discord
webhook.

When disabling webhook verification and using non-Discord webhooks, it is up to you
to make sure your webhook understands a payload that is formatted for Discord webhooks.

**Default:** True

### Default Embed Color<a name="default-embed-color"></a>

The default highlight for the embed, that is used when no other highlight color is
defined.

**Default:** #FAA61A

## Changelog<a name="changelog"></a>

See [CHANGELOG.md](https://github.com/ppfeufer/aa-fleetpings/blob/master/CHANGELOG.md)

## Translation Status<a name="translation-status"></a>

[![Translation status](https://weblate.ppfeufer.de/widget/alliance-auth-apps/aa-fleetpings/multi-auto.svg)](https://weblate.ppfeufer.de/engage/alliance-auth-apps/)

Do you want to help translate this app into your language or improve the existing
translation? - [Join our team of translators][weblate engage]!

## Contributing<a name="contributing"></a>

You want to contribute to this project? That's cool!

Please make sure to read the [Contribution Guidelines](https://github.com/ppfeufer/aa-fleetpings/blob/master/CONTRIBUTING.md).\
(I promise, it's not much, just some basics)

<!-- URLs -->

[aa installation guide]: https://allianceauth.readthedocs.io/en/latest/installation/allianceauth.html "AA installation guide"
[fittings and doctrines]: https://gitlab.com/colcrunch/fittings "Fittings and Doctrines"
[weblate engage]: https://weblate.ppfeufer.de/engage/alliance-auth-apps/ "Weblate Translations"
