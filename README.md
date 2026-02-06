# Restricted Media Player for Home Assistant

A Home Assistant custom integration that creates restricted versions of media player entities, limiting the visible source list to a user-selected subset.

## Features

- **Source Restriction**: Only display selected sources from the base media player
- **Technician Mode**: When the base player is on a hidden source, display "Technician Mode" as the current source
- **Full Control**: Switch from "Technician Mode" to any allowed source
- **Transparent Pass-through**: All other media player operations (play, pause, volume, etc.) pass through unchanged
- **Easy Configuration**: User-friendly config flow with UI-based setup
- **Reconfigurable**: Update allowed sources at any time through the options flow

## Installation

### HACS (Recommended)

1. Open HACS in Home Assistant
2. Go to "Integrations"
3. Click the three dots in the top right corner
4. Select "Custom repositories"
5. Add this repository URL: `https://github.com/craigcabrey/hacs-restricted-media-player`
6. Select category: "Integration"
7. Click "Add"
8. Find "Restricted Media Player" in the integration list
9. Click "Download"
10. Restart Home Assistant

### Manual Installation

1. Download the `custom_components/restricted_media_player` folder from this repository
2. Copy it to your `custom_components` directory in your Home Assistant config folder
3. Restart Home Assistant

## Configuration

### Adding a Restricted Media Player

1. Go to **Settings** → **Devices & Services**
2. Click **Add Integration**
3. Search for "Restricted Media Player"
4. Select the base media player entity you want to restrict
5. Choose which sources should be visible
6. Optionally customize the name of the restricted player
7. Click **Submit**

The new restricted media player entity will be created immediately.

### Updating Allowed Sources

1. Go to **Settings** → **Devices & Services**
2. Find the "Restricted Media Player" integration
3. Click **Configure** on the specific instance you want to update
4. Select/deselect sources as needed
5. Click **Submit**

The changes will take effect immediately without requiring a restart.

## How It Works

### Normal Operation

When the base media player is on an allowed source:
- The restricted player shows only the allowed sources in the source list
- The current source is displayed normally
- All operations pass through to the base player

### Technician Mode

When the base media player is on a hidden (non-allowed) source:
- "Technician Mode" appears as the first option in the source list
- "Technician Mode" is shown as the current source
- The user can still select any allowed source to switch back
- Selecting "Technician Mode" itself does nothing (it's informational only)

This allows you to:
- Hide technical sources (HDMI ports, AUX inputs, etc.) from everyday users
- Still provide visibility that a technician has changed the source
- Allow users to easily switch back to allowed sources

### Pass-through Operations

All media player operations pass through transparently:
- Play, pause, stop
- Volume control (up, down, set level, mute)
- Next/previous track
- Media seeking
- Turn on/off
- Playing specific media

## Use Cases

- **Home Theater**: Hide technical HDMI inputs, only show streaming apps
- **Commercial Displays**: Restrict users to approved content sources
- **Multi-user Environments**: Simplify source selection for non-technical users
- **Parental Controls**: Limit children to approved sources
- **Smart Home Automation**: Create room-specific source restrictions

## Example

Base media player has sources:
- Netflix
- YouTube
- HDMI 1
- HDMI 2
- Bluetooth
- AUX

You configure a restricted player with only:
- Netflix
- YouTube

**Result**:
- Users only see Netflix and YouTube in the source list
- If a technician switches to HDMI 1, users see "Technician Mode" as current source
- Users can select Netflix or YouTube to switch back
- All other controls (volume, play/pause) work normally

## Requirements

- Home Assistant 2023.8.0 or newer
- A media player entity with source selection support

## Troubleshooting

### The integration doesn't appear

- Make sure you've restarted Home Assistant after installation
- Check the Home Assistant logs for errors

### No sources appear during configuration

- Ensure the base media player entity has a `source_list` attribute
- Try selecting a different media player that supports source selection

### Changes don't take effect

- The integration automatically reloads when options are changed
- If issues persist, try restarting Home Assistant

### "Technician Mode" doesn't appear

- This only appears when the base player is actually on a non-allowed source
- Check that the base player's current source is not in your allowed list

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

If you encounter any issues or have questions:
- [Open an issue](https://github.com/craigcabrey/hacs-restricted-media-player/issues) on GitHub
- Check existing issues for solutions

## Credits

Created by Craig Snowden
