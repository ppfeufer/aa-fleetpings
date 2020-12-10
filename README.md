# AA Fleet Pings

[![Version](https://img.shields.io/pypi/v/aa-fleetpings?label=release)](https://pypi.org/project/aa-fleetpings/)
[![License](https://img.shields.io/badge/license-GPLv3-green)](https://pypi.org/project/aa-fleetpings/)
[![Python](https://img.shields.io/pypi/pyversions/aa-fleetpings)](https://pypi.org/project/aa-fleetpings/)
[![Django](https://img.shields.io/pypi/djversions/aa-fleetpings?label=django)](https://pypi.org/project/aa-fleetpings/)
[![Code Style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](http://black.readthedocs.io/en/latest/)

App for Alliance Auth that can format your fleet pings and also ping for you to Discord and Slack.

Formerly known as [AA Discord Ping Formatter](https://github.com/ppfeufer/aa-discord-ping-formatter).

Since the original app evolved and with the now added support to ping Slack as well,
I felt the name was no longer fitting, so I re-branded the app as "AA Fleet Pings". The old Discord ping
formatter will be discontinued in favor of this one.

If you used the old app until now (not the alpha versions), don't worry, nothing is breaking. At least I hope so.
Since this app has a complete new code base and a different name it shouldn't interfere with the old one.
All you need to do is to set the new permission for the groups that need to have access to this app.

If you run into any trouble, feel free to shout at me on the [Alliance Auth Support Discord](https://discord.gg/fjnHAmk).
You find me there as Rounon Dax.

## Contents

- [Installation](#installation)
- [Updating](#updating)
- [Screenshots](#screenshots)
- [Configuration](#configuration)
- [Change Log](CHANGELOG.md)

## Installation

**Important**: This app is a plugin for Alliance Auth. If you don't have Alliance Auth running already,
please install it first before proceeding.
(see the official [AA installation guide](https://allianceauth.readthedocs.io/en/latest/installation/allianceauth.html) for details)

### Step 0 - Migrating from AA Discord Ping Formatter

If you have been using the old Discord Ping Formatter until now, it is pretty easy to migrate.

First you have to remove the old app.

```bash
python manage.py migrate discordpingformatter zero
```

```bash
pip uninstall aa-discord-ping-formatter
```

After this, just remove the `'discordpingformatter',` line from your `INSTALLED_APPS` in your `local.py`.
Once done, feel free to install this app by following the steps above.

### Step 1 - Install the app

Make sure you are in the virtual environment (venv) of your Alliance Auth installation.
Then install the latest version:

```bash
pip install aa-fleetpings
```

### Step 2 - Update your AA settings

Configure your AA settings (`local.py`) as follows:

- Add `'fleetpings',` to `INSTALLED_APPS`


### Step 3 - Finalize the installation

Copy static files and run migrations

```bash
python manage.py collectstatic
```

```bash
python manage.py migrate
```

Restart your supervisor services for AA

### Step 4 - Setup permission

Now you can setup permissions in Alliance Auth for your users.
Add ``fleetpings | aa fleet pings | Can access this app`` to the states and/or
groups you would like to have access.

### Step 5 - Setup the app

In your admin backend you'll find a new section called `Fleet Pings`.
This is where you set all your stuff up, like the webhooks you want to ping and who can ping them,
fleet types, comms, formup locations and so on. It's pretty straight forward,
so you shouldn't have any issues. Go nuts!

## Updating

To update your existing installation of AA Discord Ping Formatter first enable your virtual environment.

Then run the following commands from your AA project directory (the one that contains `manage.py`).

```bash
pip install -U aa-fleetpings
```

```bash
python manage.py collectstatic
```

```bash
python manage.py migrate
```

Finally restart your AA supervisor services.

## Screenshots

### View in Alliance Auth

![AA View](https://raw.githubusercontent.com/ppfeufer/aa-fleetpings/master/fleetpings/docs/aa-view.jpg)

### Discord Ping Examples

#### Not embedded

![Discord Ping No Embed](https://raw.githubusercontent.com/ppfeufer/aa-fleetpings/master/fleetpings/docs/discord-ping.jpg)

#### Embedded

![Discord Ping Embed](https://raw.githubusercontent.com/ppfeufer/aa-fleetpings/master/fleetpings/docs/discord-ping-embedded.jpg)


## Configuration

### Using Slack instead of Discord?

Don't worry, I don't judge and you still can use this module. It supports also pings to Slack.
Simply add the following to your `local.py`.

```python
## AA Fleet Pings
AA_FLEETPINGS_USE_SLACK = True
```

Although you cannot use your Auth groups as targets for pings with Slack. Auth doesn't supprt Slack as of yet.
(Maybe if someone writes a service?)

### Slack Ping Example

![Slack Ping](https://raw.githubusercontent.com/ppfeufer/aa-fleetpings/master/fleetpings/docs/slack-ping.jpg)

### Use Doctrines from Fittings module

If you have the [Fittings and Doctrines](https://gitlab.com/colcrunch/fittings) module installed and your doctrines configured there,
you don't have to re-build your doctrine list for this module. You can simply use the doctrines you
already have configured in the Fittings and Doctrines module.

To do so, add the following to your `local.py`:

```python
## AA Fleet Pings
AA_FLEETPINGS_USE_DOCTRINES_FROM_FITTINGS_MODULE = True
```
