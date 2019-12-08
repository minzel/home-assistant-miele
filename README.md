# Miele@home custom component

[![GitHub Release][releases-shield]][releases]
[![hacs_badge][hacs-shield]][hacs]

_Homeassistant Custom Component sensors provides miele devices from the [Miele 3rd Party API](https://www.miele.com/developer)._

## Installation

### HACS

The easiest way to add this to your Homeassistant installation is using [HACS](https://custom-components.github.io/hacs/).

1. Include this repository as a custom integration in the HACS settings.
2. Install the Miele@home integration via HACS.
3. Follow the instructions under [Configuration](#configuration) below.

## Setup

To enable the integration, you need to register for an API key by following the instructions [here](https://www.miele.com/f/com/en/register_api.aspx).

## Configuration

To enable the integration, add the following lines to your configuration.yaml file:

```yaml
miele:
  client_id: YOUR_CLIENT_ID
  client_secret: YOUR_CLIENT_SECRET
```

## Configuration options

Key | Type | Required | Description
-- | -- | -- | --
`client_id` | `string` | `true` | Your application's API id (get one by following the instructions above).
`client_secret` | `string` | `true` | Your application's API id (get one by following the instructions above).
`language` | `string` | `false` | Choose the language of your choice. The default is `en`.


[releases-shield]: https://img.shields.io/github/v/release/minzel/home-assistant-miele
[releases]: https://github.com/minzel/home-assistant-miele/releases
[hacs-shield]: https://img.shields.io/badge/HACS-Custom-orange.svg
[hacs]: https://github.com/custom-components/hacs
