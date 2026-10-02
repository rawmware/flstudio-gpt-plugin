# FL Studio Copilot

This repository now contains the first local plugin slice: an MCP stdio server, a FL Studio MIDI scripting companion, and MIDI pattern generation.

## Install for local testing

1. Add this repository as a local plugin in the host that supports Agent Plugins/MCP.
2. Copy `flstudio/device_FLStudioCopilot.py` to `%USERPROFILE%/Documents/Image-Line/FL Studio/Settings/Hardware/FL Studio Copilot/device_FLStudioCopilot.py`.
3. In FL Studio, open MIDI Settings and select **FL Studio Copilot (user)** as the controller type.
4. Ask the host for `flstudio_status`. It should report that the companion is connected.

The plugin stores its local command/status channel in `%USERPROFILE%/FL Studio Copilot/`. The GPT can arm a take, wait for the user to press Play, request a finish, and generate `.mid` files for drums or bass. Native FL Studio audio and automation capture still depends on the project's recording filter and must be verified in the user's installation.

## Available tools

- `arm_live_take`: arm and wait; it does not start playback.
- `finish_live_take`: request finalization.
- `flstudio_status`: read companion state.
- `generate_midi_pattern`: create a starter drum or bass MIDI file.

Run `python -m py_compile server/flstudio_mcp.py flstudio/device_FLStudioCopilot.py` to validate the Python files.
