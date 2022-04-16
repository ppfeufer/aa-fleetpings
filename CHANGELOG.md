# Change Log

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](http://keepachangelog.com/)
and this project adheres to [Semantic Versioning](http://semver.org/).


## [In Development] - Unreleased


## [2.13.1] - 2022-04-17

### Added

- Missing `helper` directory


## [2.13.0] - 2022-04-17

### Added

- Local time to formup time segment (#70)

### Changed

- Minimum requirements
  - Alliance Auth >= v2.11.2
  - Alliance Auth App Utils >= 1.13.0
- Switched to Alliance Auth App Utils for logging
- JavaScript cleaned up
- Logic for ping text moved from JavaScript to Python/Django code
- Discord pings are now always embedded
- Get `timezones` app URL from Django instead of it being hardcoded

### Removed

- Support for Slack Webhooks. Slack is not supported by Alliance Auth, so it has
  been dropped from this app as well.


## [2.13.0-beta.1] - 2022-04-06

### Added

- Local time to formup time segment (#70)

### Changed

- Get `timezones` app URL from Django instead of it being hardcoded


## [2.12.0] - 2022-03-02

### Added

- Test suite for AA 3.x and Django 4

### Changed

- Switched to `setup.cfg` as config file, since `setup.py` is deprecated now

### Removed

- Deprecated settings


## [2.11.0] - 2022-02-28

### Fixed

- [Compatibility] AA 3.x / Django 4 :: ImportError: cannot import name
  'ugettext_lazy' from 'django.utils.translation'

### Added

- Error message on missing information for Optimer and SRP
  - Optimer (Mandatrory fields):
    - » FC Name
    - » Fleet Name
    - » Formup Location
    - » Formup Time
    - » Ships / Doctrine
  - SRP (Mandatrory fields):
    - » Fleet Name
    - » Ships / Doctrine

### Changed

- JavaScript modernised


## [2.10.1] - 2022-02-02

### Changed

- Using `path` in URL config instead of soon-to-be removed `url`


## [2.10.0] - 2022-01-12

### Added

- `(Upcoming)` to the header text of pre-pinged fleets to ensure there is no
  confusion between pre-pinged fleets and fleets that start now (#61)

### Changed

- JS rewrite


## [2.9.0] - 2022-01-11

### Added

- Versioned static files to prevent browser cache related errors on app updates

### Fixed

- An issue where the checkboxes haven't been cleared properly when switching between
  "Pre-Ping" and "Formup NOW"


## [2.8.0] - 2022-01-02

### Added

- Tests for Python 3.11 (still allowed failing, since Python 3.11 is still in alpha
  state)

### Changed

- Minimum requirements
  - Alliance Auth v2.9.4

### Removed

- Check for AA-GDPR, since we don't load any external resources it is not needed


## [2.7.0] - 2021-11-30

### Changed

- Minimum requirements
  - Python 3.7
  - Alliance Auth v2.9.3


## [2.6.0] - 2021-11-15

### Added

- Tests
- `allianceauth-app-utils` to replace built-in functions

### Changed

- Minimum Python version set to 3.7
- Minimum AA version set to 2.8.8


## [2.5.5] - 2021-07-08

### Added

- Python 3.9 and Django 3.2 compatibility


## [2.5.4] - 2021-05-05

### Fixed

- Using Django application registry instead of directly accessing `INSTALLED_APPS` (#49)


## [2.5.3] - 2021-05-05

### Fixed

- Interference with Discord service migrations in case the Discord service is
  activated _after_ this app is installed.


## [2.5.2] - 2021-01-19

### Added

- Permission checks for "Create SRP Link" checkbox, so only FC's who have the
  permission to actually add SRP links can use this feature (#46)

### Fixed

- Creating multiple SRP links with the same SRP code.


## [2.5.1] - 2021-01-17

### Changed

- Set input field for formup time to `autocomplete="off"` so you don't have to fiddle
  around to use the datetime picker anymore

### Fixed

- An issue where additionally configured ping targets wouldn't show up in the
  dropdown (#44)


## [2.5.0] - 2021-01-12

### Added

- Checkbox to create SRP link when SRP is active for a fleet and formup time is set
  to "NOW". Supported SRP Modules:
  - allianceauth.srp (that's the built-in module)
  - [aasrp](https://github.com/ppfeufer/aa-srp)
- Colored box in the admin fleet type overview to represent the embed color

### Changed

- Giving the ajax call a proper name

### Removed

- Django 2 support


## [2.4.4] - 2020-12-16

### Fixed

- Bootstrap classes in template


## [2.4.3] - 2020-12-10

### Fixed

- An issue with quotes in the doctrines field (#38)


## [2.4.2] - 2020-11-08

### Fixed

- Create optimer is visible even if optimer is not active (#35)


## [2.4.1] - 2020-11-05

### Added

- "Don't Ping" option to ping targets


## [2.4.0] - 2020-10-26

### Added

- Checkbox to automatically create an fleet operations timer for a pre ping


## [2.3.0] - 2020-10-14

### Important!

Before updating to this version, make sure you have your Alliance Auth updated to version 2.8.0 (or newer).
This version of AA Fleetpings uses a JavaScript library that is introduced in Alliance Auth 2.8.0,
so have your Auth updated before installing this version.

### Fixed

- mySQL text fields can't have default values
- Parameters differ from overridden method warning

### Added

- Filter to the admin backend
- More checks for Discord. Now checking if the Discord Service s actually activated and setup properly
- Compatibility to AA Timezones (v1.2.1) new link style
- Backwards compatibility to versions of AA Timezones before 1.2.1, so the old link style is still generated when using an older version

### Changed

- Use clipboard.js bundled with Alliance Auth
- Minimum required Alliance Auth version set to 2.8.0 due to us using clipboard.js bundled with Alliance Auth
- Unused lib removed


## [2.2.2] - 2020-09-23

### Added

- Django 3 stuff in setup.py, Should probably be in there as well ...


## [2.2.1] - 2020-09-23

### Checked

- Compatibility with the upcoming changes in Alliance Auth v2.8.0 (Django 3)

### Changed

- Fleet type embed color is now a color picker in admin backend


## [2.2.0] - 2020-09-16

### Added

- Option to use the fittings from the [Fittings and Doctrines](https://gitlab.com/colcrunch/fittings) module if you have it installed


## [2.1.0] - 2020-09-16

### Added

- Restrictions to fleet types
- Restrictions to doctrines


## [2.0.0] - 2020-09-15

This is the official re-brand of AA Discord Ping Formatter, since the original name didn't fit anymore with
the new features, like automatic pings and now the new Slack implementation.

If you were testing one of the alpha versions of AA Discord Ping Formatter, make sure to migrate
discordpingformatter zero and deactivate the old app in your local.py before activating this one.
They will not run side by side.

This is how you do it:
```bash
python manage.py migrate discordpingformatter zero
```
Now remove the `'discordpingformatter',` line and add `'fleetpings',` instead.

Once done, run collectstatic and migrations again. You now have to re-do your settings in the admin
backend, since we just nuked them from the old app.

### Added

- **Support for pings to Slack.** If you're using Slack, simply add ``AA_FLEETPINGS_USE_SLACK = True`` to your `local.py`

### Changed

- **!! breaking change !!** Settings are no longer in your `local.py`. You find them now in your admin backend. Which means. after installing this version, you _have_ to re-do you setting in the admin backend of Auth. But trust me, it's worth the effort.
- Minimum AA version set to 2.7.4 since we use a feature that was introduced in this version. So make sure to update your Alliance Auth before testing this app.

### Fixed

- Several logic errors in the JavaScript


## From the discontinued AA Discord Ping Formatter (to keep the history alive)


## [1.1.4] - 2020-08-14

### Fixed

- Little logic error in embedded prepings when no FC is set


## [1.1.3] - 2020-08-11

### Fixed

- Single quote issue finally fixed (#31)


## [1.1.2] - 2020-08-10

### Fixed

- Missing "Fleet" on embedded pings headline when no fleet type is selected
- Hopefully escaped possible single quotes in a characters name so they will not be transformed into their respective HTML-entities in a ping


## [1.1.1] - 2020-08-02

### Changed

- JS modularizing, creation of the link for aa-timezones moved to its own function
- Added a bit more information to the embedded ping, so on mobile phones or system notification there is a bit more than just `@everyone` or `@here` to see.


## [1.1.0] - 2020-07-17

### Added

- Configuration for pre-defined fleet comms, formup locations and doctrines. These can be configured in your `local.py` via `AA_DISCORDFORMATTER_FLEET_COMMS`, `AA_DISCORDFORMATTER_FLEET_DOCTRINES` and `AA_DISCORDFORMATTER_FLEET_FORMUP_LOCATIONS`. See [README](https://github.com/ppfeufer/aa-discord-ping-formatter#fleet-comms-formup-location-and-doctrine) for syntax.


## [1.0.0] - 2020-07-16

### Added

- Restriction for ping targets. Just to make sure not everyone can ping for Capitals or even Supers and Titans if these are configured ping targets. (#18)

### Changed

- Set time selection steps to 15 minutes instead of 60 in te datepicker
- Set Monday as the beginning of the week in the datepicker

### Fixed

- Our Australian time travelers and everyone else who lives in the future (UTC+x) is now able to pre-ping fleets that are coming up in 2 hours Eve time, which might still be in their past local time, depending on how far in the future they live. (#19)


## [0.1.10] - 2020-07-16

### Added

- Option to embed automatic pings via webhook (#13)
- Embedded ping via webhook are color coded. Pre-defined fleet types are by default (Roam = green, Home Defense = yellow, StratOP = orange, CTA = red) and custom fleet types can be defined via settings (see [README](https://github.com/ppfeufer/aa-discord-ping-formatter#embed-webhook-pings))

### Changed

- Link to time zones conversion is now a named link

### Fixed

- Missing semicolons in JavaScript found their way back to where they belong


## [0.1.9] - 2020-07-14

### Added

- Ping creator at the end auf automatic pings via webhooks


## [0.1.8] - 2020-07-09

### Added

- Webhook group restrictions. Webhooks can now be restricted to certain groups (see [README](https://github.com/ppfeufer/aa-discord-ping-formatter#adding-ping-channels)), so not everyone who has access too this module can ping through all webhooks. Webhoos without restrictions are accessible for all with access to the module. (Thanks to Exiom for bringing this up)
- FC name is pre-filled with the users main character name, since the user is most likely te FC pinging for his own fleet.

### Changed

- Formup Time is now a proper date picker so there is a consistent date/time format throughout the pings
- Formup Time disabled by default. To enable it either check the Pre-Ping checkbox or disable the Formup NOW checkbox below the Formup Time field
- Formup Time is set to NOW by default


## [0.1.7] - 2020-07-08

### Added

- Link to timezones conversion on formup time if the [aa-timezones](https://github.com/ppfeufer/aa-timezones) module is installed


## [0.1.6] - 2020-07-04

### Fixed

- Ping for non default roles via Webhook (#9)


## [0.1.5] - 2020-06-24

### Added

- Configurable Discord webhooks to ping channels automagically


## [0.1.4] - 2020-06-18

### Changed

- Ping Type renamed to Ping Target in form

### Fixed

- typo in Additional Information


## [0.1.3] - 2020-06-15

### Added

- Configuration for additional ping targets and fleet types


## [0.1.2] - 2020-06-14

### Fixed

- sanitizing form field input


## [0.1.1] - 2020-06-13

### Fixed

- there should always be an empty line before Additional Information ...


## [0.1.0] - 2020-06-13

### Added

- initial version
