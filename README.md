# Home Assistant Miele@home

![GitHub release (latest by date)](https://img.shields.io/github/v/release/minzel/home-assistant-miele?style=for-the-badge)
![GitHub Releases](https://img.shields.io/github/downloads/minzel/home-assistant-miele/latest/total?label=Downloads&style=for-the-badge)
[![hacs_badge](https://img.shields.io/badge/HACS-Custom-orange.svg?style=for-the-badge)](https://github.com/custom-components/hacs)

## Intro

Home Assistant Miele@home sensors provides miele devices from the [Miele 3rd Party API][miele-developer]. It will find all devices over Miele 3rd Party API and add them to Home Assistant.

![Logo](https://raw.githubusercontent.com/minzel/home-assistant-miele/master/images/miele@home.png)

## Installation

### Install with HACS (recomended)

The easiest way to add this to your Homeassistant installation is using [HACS][hacs-integration].

1. Include this repository as a custom integration in the HACS settings.
2. Install the Miele@home integration via HACS.
3. Follow the instructions under [Configuration](#configuration) below.

### Install manually

1. Install this platform by creating a custom_components folder in the same folder as your configuration.yaml, if it doesn't already exist.
2. Create another folder miele in the custom_components folder. Copy all files from custom_components into the miele folder. Do not copy files from master branch, download latest release (.zip) from [here](https://github.com/minzel/home-assistant-miele/releases).

## Setup

To enable the integration, you need to register for an API key by following the instructions [here][miele-register].

### Configuration

When you have installed miele and make sure it exists under custom_components folder it is time to configure it in Home Assistant.

To enable the integration, add the following lines to your configuration.yaml file:

```yaml
miele:
  client_id: YOUR_CLIENT_ID
  client_secret: YOUR_CLIENT_SECRET
  language: de
```

#### Configuration options

Key | Type | Required | Description
-- | -- | -- | --
`client_id` | `string` | `true` | Your application's API id (get one by following the instructions above).
`client_secret` | `string` | `true` | Your application's API id (get one by following the instructions above).
`language` | `string` | `false` | Choose the language of your choice. The default is `en`.

### Restart Home Assistant

Now you should restart Home Assistant to load miele.

Adding Miele@home integration in Home Assistant Web UI will show you a UI to configure the Miele platform. Follow the instructions to log into the Miele 3rd Party API. Miele will discover all devices and show them as sensors in Home Assistant.

[releases-shield]: https://img.shields.io/github/v/release/minzel/home-assistant-miele
[releases]: https://github.com/minzel/home-assistant-miele/releases
[hacs-shield]: https://img.shields.io/badge/HACS-Custom-orange.svg
[hacs]: https://hacs.xyz/
[hacs-integration]: https://github.com/hacs/integration
[miele-developer]: https://www.miele.com/developer
[miele-register]: https://www.miele.com/f/com/en/register_api.aspx
