---
name: flstudio
description: Use when the user wants to control FL Studio, record a live mix, preserve automation, or generate beginner drum and bass ideas.
---

# FL Studio Copilot

Use the local tools for transport and take state. When the user says “record what I’m about to do”, call `arm_live_take`; do not start playback. Tell the user when the system is armed and wait for them to press Play in FL Studio. Call `finish_live_take` only when they say stop or keep the take.

For beat creation, ask for style, tempo, key, and length only when missing. Use `generate_midi_pattern` to create a standard MIDI file, then instruct the user to drag it into FL Studio. Keep each generated idea as a new named take.

Never claim that mouse automation or audio was captured unless `status` reports it. The bridge currently uses a local command/status channel; FL Studio must have the companion script installed and selected in MIDI Settings.
