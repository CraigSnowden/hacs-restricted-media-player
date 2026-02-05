# Testing Checklist for Restricted Media Player

## Pre-Installation Verification

- [ ] All Python files have valid syntax
- [ ] manifest.json is valid JSON
- [ ] strings.json and translations/en.json are valid JSON
- [ ] File structure matches Home Assistant requirements

## Installation Testing

### Manual Installation
- [ ] Copy `custom_components/restricted_media_player` to Home Assistant
- [ ] Restart Home Assistant
- [ ] Check logs for any errors during loading

### HACS Installation (after publishing)
- [ ] Integration appears in HACS
- [ ] Installation completes without errors
- [ ] Restart Home Assistant
- [ ] Integration loads successfully

## Configuration Flow Testing

### Initial Setup
- [ ] Integration appears in "Add Integration" list
- [ ] Step 1: Base entity selector shows only media players
- [ ] Step 1: Selecting a media player advances to step 2
- [ ] Step 2: Source list dynamically populates from base player
- [ ] Step 2: Can select multiple sources
- [ ] Step 2: Can customize the name
- [ ] Step 2: Submitting creates the restricted player entity
- [ ] Entity appears with correct name
- [ ] Entity ID is properly formatted

### Error Handling
- [ ] Selecting a player with no sources shows appropriate error
- [ ] Attempting to configure the same player twice is prevented
- [ ] Invalid inputs are caught and explained

## Functionality Testing

### Normal Operation (base on allowed source)
- [ ] Restricted player shows only allowed sources
- [ ] Current source displays correctly
- [ ] Can switch between allowed sources
- [ ] Source changes reflect on base player
- [ ] Source list doesn't include "Technician Mode"

### Technician Mode (base on hidden source)
- [ ] "Technician Mode" appears as first source in list
- [ ] "Technician Mode" shows as current source
- [ ] Can select an allowed source from the list
- [ ] Selecting allowed source switches base player
- [ ] Selecting "Technician Mode" does nothing (logs debug message)

### Pass-through Operations
- [ ] Volume up works
- [ ] Volume down works
- [ ] Set volume level works
- [ ] Mute/unmute works
- [ ] Play works
- [ ] Pause works
- [ ] Stop works
- [ ] Next track works
- [ ] Previous track works
- [ ] Turn on works
- [ ] Turn off works
- [ ] Media seeking works (if supported)
- [ ] Play media works (if supported)

### State Synchronization
- [ ] Changes to base player reflect immediately
- [ ] Volume changes sync
- [ ] Source changes sync
- [ ] Play state syncs
- [ ] Media info syncs (title, artist, album, etc.)
- [ ] Base player unavailable → restricted player unavailable

### Attributes
- [ ] All base player attributes pass through correctly:
  - [ ] volume_level
  - [ ] is_volume_muted
  - [ ] media_content_id
  - [ ] media_content_type
  - [ ] media_duration
  - [ ] media_position
  - [ ] media_title
  - [ ] media_artist
  - [ ] media_album_name
  - [ ] app_name
  - [ ] supported_features

## Options Flow Testing

- [ ] Click "Configure" on the integration
- [ ] Current allowed sources are pre-selected
- [ ] Can modify source selection
- [ ] Submitting updates the configuration
- [ ] Changes take effect immediately (no restart needed)
- [ ] Source list updates correctly after change
- [ ] Base player with no sources shows error

## Edge Cases

- [ ] Base player removed → restricted player becomes unavailable
- [ ] Base player has no sources → appropriate handling
- [ ] Base player state is "unknown" → restricted player handles gracefully
- [ ] Base player state is "unavailable" → restricted player unavailable
- [ ] Rapid source changes don't cause issues
- [ ] Multiple restricted players from same base work independently
- [ ] Home Assistant restart preserves configuration
- [ ] Config entry reload works correctly

## UI Testing

### Lovelace Card
- [ ] Restricted player works in media control card
- [ ] Source dropdown shows correct options
- [ ] Current source displays correctly
- [ ] "Technician Mode" appears when appropriate
- [ ] Volume slider works
- [ ] Play/pause buttons work

### Developer Tools
- [ ] Entity state shows correct values
- [ ] Attributes display properly
- [ ] Can call services on the entity
- [ ] State changes reflect in real-time

## Multi-Player Testing

- [ ] Create multiple restricted players from different base players
- [ ] All work independently
- [ ] Can configure different source sets
- [ ] State changes don't interfere

## Logging

- [ ] No errors in Home Assistant logs during normal operation
- [ ] Debug logging shows "Technician Mode is informational" when selected
- [ ] Warnings appear if base entity becomes unavailable

## Performance

- [ ] Entity updates are responsive
- [ ] No noticeable lag when changing sources
- [ ] State tracking doesn't cause excessive updates
- [ ] Memory usage is reasonable

## Documentation

- [ ] README.md is clear and accurate
- [ ] Installation instructions work
- [ ] Configuration steps are accurate
- [ ] Examples match actual behavior
- [ ] Troubleshooting section is helpful

## Cleanup

- [ ] Removing integration removes entity
- [ ] No orphaned entities after removal
- [ ] Logs are clean after removal

## Test Media Players

Recommended test targets:
- [ ] Sonos speaker (good source list)
- [ ] Roku TV (multiple HDMI inputs)
- [ ] Chromecast (apps as sources)
- [ ] Apple TV (if available)
- [ ] Any media player with 5+ sources

## Notes

Record any issues found during testing:

1.
2.
3.

## Sign-off

- [ ] All critical functionality tested
- [ ] No blocking issues found
- [ ] Ready for release

Tested by: ________________
Date: ________________
Version: ________________
