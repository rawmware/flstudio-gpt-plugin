# Live performance workflow reference

Source: the user's `Desktop 2026.10.02 - 19.00.18.01.mp4`, reviewed on October 2, 2026. Duration: approximately 3 minutes 5 seconds. The private video is not included in this repository.

## Observed on screen

- FL Studio 2024.2.1, with the footer identifying Fruity Edition. This does not independently establish the user's license entitlements.
- A single existing stereo audio clip plays in the Playlist in Song mode. The displayed project tempo is 130 BPM; this is not a measured tempo of the audio.
- Playback begins near the beginning of the recording and continues through almost the entire clip.
- The Master mixer channel is selected. Its visible effects include `Bass boost` and `Fruity Limiter`.
- The open `Bass boost (Master)` effect has low-, mid-, and high-band dynamics controls.
- The user repeatedly changes the LOW BAND THRES control during playback. The FL Studio hint display shows `L Threshold: 0.0dB` and `L Threshold: -60.0dB` at multiple points.
- The cursor also visits low-band knee, ratio, and release controls and the mixer. A hover/hint alone is not evidence of a parameter change.
- The recording shows a live effect performance over an existing track, rather than drum programming, piano-roll composition, or arranging clips.

Review method: visual samples across the full clip at six-second intervals, with additional two-second samples of the controls from 00:08 through 03:02. Audio was not auditioned. Exact gesture timing and continuous parameter curves cannot be recovered from these samples.

## Product intent derived from the demonstration

The first workflow is **perform and preserve**. The user wants to press play and improvise with effects using their mouse, with the assistant taking care of preparing and preserving the take.

Desired interaction:

1. User says, "Record what I'm about to do."
2. The plugin checks the connection and recording readiness, prepares a new take, and reports "Armed — press Play when you're ready."
3. It waits for the user's playback action. It must not start playback merely because recording was requested.
4. During playback, preserve the processed mix and editable automation where FL Studio supports it. Capture the starting parameter state as well as changes and their song positions.
5. Let the user perform without questions, unsolicited adjustments, or interruptions.
6. On stop/end, finalize the take, report what was actually captured and where it was saved, and offer audition/retry.
7. Subsequent requests such as "keep that take" or "redo the last section" should operate on explicit take boundaries and preserve earlier takes.

Both audio and editable automation are the working default from the original request, not a confirmed answer to the earlier preference question. Native automation recording should provide timing accuracy; observing parameter values is useful telemetry, not a substitute for native automation.

## Separate creation workflow

The original request also includes beginner-oriented drum patterns, bass lines, arrangement, and progression from an idea to a finished track. Retain this scope, but do not treat this video as a demonstration of those features. Explain one useful next action at a time, create auditionable musical material, and keep versions so the user can compare and undo changes.

## Verification requirements

- An armed take stays idle until playback begins.
- Capture starts with the first intended musical event; it does not lose the opening while waiting on a chat response.
- Mouse-driven effect changes are included, not only hardware MIDI messages.
- Replaying the saved performance reproduces the recorded changes at their original song positions.
- The audio capture includes the intended Master processing, with the capture point documented.
- Silence, missing audio routing, disabled automation filters, disconnects, and unavailable recording features produce specific status, not a false success.
- Native recording availability must be checked against the installed edition and actual configuration.
- A screenshot/video is context for understanding the workflow, not an editable automation file.
- No successful recording, audio quality judgment, or end-to-end FL Studio connection has yet been verified.

## Current build state

The requested repository has been cloned locally and branch `codex/fl-studio-copilot` created. This document records the demonstrated workflow; a working plugin has not yet been implemented or installed.
