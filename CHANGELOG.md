# Change Log

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](http://keepachangelog.com/)
and this project adheres to [Semantic Versioning](http://semver.org/).

## [2.0.0a4] - 2020-09-13
### Changed
- Minimum AA version set to 2.7.4 since we use a feature that was introduced in this version. So make sure to update your Alliance Auth before testing this app.

## [2.0.0a3] - 2020-09-13
### Fixed
- Using Python 3 style `super()` without arguments
- Import order

### Removed
- template tags since they are no longer needed

## [2.0.0a2] - 2020-09-12
### Changed
- Groups for PingTargets can now be selected via drop down in admin and the respective Discord group_id is assigned automatically. **!! IMPORTANT !!** In case you already defined PingTargets in v2.0.0a1, you have to remove them before migrating.

## [2.0.0a1] - 2020-09-12
### Added
- Support for pings to Slack. If you're using Slack, add ``AA_FLEETPINGFORMATTER_USE_SLACK = True`` to your `local.py`

### Changed
- **!! breaking change !!** Settings are no longer in your `local.py`. You find them now in your admin backend. Which means. after updating to this version, you _have_ to re-do you setting in the admin backend of Auth. 


# From the discontinued AA Discord Ping Formatter (to keep the history alive)

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
