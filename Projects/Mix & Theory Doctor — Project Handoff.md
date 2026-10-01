# Mix & Theory Doctor — Project Handoff

Sep 30, 2026 · @Shutterabia

## Summary

Mix & Theory Doctor is an LLM agent that repairs a rough song recording by ear and by music theory, using only tools I build. No model training is involved: the LLM plans and reasons, while deterministic DSP and theory tools measure, act and verify.

The goal is a portfolio project that proves agent engineering beyond an LLM wrapper: custom tools, a closed measure-act-verify loop, and a benchmark with real numbers.

## Core concept

The user uploads a rough recording or stems, plus an optional reference track and a request ("make it cleaner, fix sour notes"). The agent analyzes the song on two layers, decides what is wrong, applies fixes, and re-measures after every change.

- **Audio layer:** loudness (LUFS), spectral balance, frequency masking between instruments, muddiness, clipping, stereo and phase issues.
- **Musical layer:** key, chords, melody notes, out-of-key notes, harmonic clashes between parts, and timing drift against the beat grid.

The two layers catch each other's problems. A clash may be a mix issue (two parts crowding 300 Hz) or a theory issue (a major third over a minor chord). Deciding which one it is, is the agent's core reasoning task.

## Design principles

1. **No training.** Every tool is classic DSP or rule-based music theory. Off-the-shelf libraries are fine.
2. **LLM plans, tools measure.** The LLM never guesses a number. Keys, frequencies, loudness and timing always come from a tool.
3. **Verify and revert.** Every change is re-measured. If a metric gets worse, the change is undone.
4. **Typed, testable tools.** Each tool is a standalone function with clear JSON inputs and outputs and unit tests, exposed over MCP.
5. **Non-destructive.** Originals are never overwritten; every step writes a new version so any state can be restored.
6. **Transparent.** The agent's reasoning trace and a before/after metric report are shown to the user.

## Tool inventory

The first version needs about 14 tools across three groups. Libraries are suggestions, all usable without training.

| Tool | Group | Returns / does | Library |
| --- | --- | --- | --- |
| `measure_loudness` | Audio analysis | Integrated LUFS, true peak, clipping count | pyloudnorm, numpy |
| `spectral_profile` | Audio analysis | Energy per frequency band, compared with a reference track | librosa, scipy |
| `detect_masking` | Audio analysis | Band overlaps between two stems, severity score | librosa |
| `stereo_check` | Audio analysis | Width, phase correlation, mono compatibility | numpy |
| `detect_key` | Musical analysis | Key + confidence (chroma template matching) | librosa |
| `detect_chords` | Musical analysis | Chord per beat with timestamps | librosa chroma + templates |
| `track_pitch` | Musical analysis | Note sequence of a melodic stem (pYIN) | librosa |
| `find_out_of_key_notes` | Musical analysis | Notes that clash with key or current chord | music21 |
| `beat_grid` | Musical analysis | Tempo, beat times, per-onset timing error in ms | librosa |
| `apply_eq` | Action | Parametric EQ on a stem | pedalboard |
| `apply_dynamics` | Action | Compression, limiting, gain | pedalboard |
| `pitch_correct_note` | Action | Shift one note region to the target pitch | librosa, pyrubberband |
| `quantize_hit` | Action | Nudge an onset onto the beat grid | numpy slicing + crossfade |
| `generate_part` | Action (stretch) | Rule-based bassline or harmony from detected chords, rendered to audio | mido, FluidSynth |

Support tools: `mix_stems`, `render_version` and `revert_to(version_id)` for non-destructive history.

## Agent loop

The agent fixes one issue at a time and keeps a change only when the metrics improve.

&#91;embedded content: agent loop · plan, act, verify, keep or revert\]

Analysis runs once up front and again after every fix. The LLM picks the most severe issue, chooses a tool, and the re-measure step decides keep or revert. The loop ends when no issues remain or a step budget runs out, then outputs the final mix and a before/after metric report.

## Build roadmap

Plan for about 7 weeks part-time, starting with stems because instruments arrive already separated.

1. **Weeks 1–2: Audio analysis tools.** Loudness, spectral profile, masking, stereo check. Unit-test each on known test tones and a few real stem sets.
2. **Week 3: Action tools + versioning.** EQ and dynamics via pedalboard, plus render, mix and revert. Expose all tools through one MCP server.
3. **Week 4: First agent loop (mix only).** A hand-written plan → act → verify loop, no heavy framework. Goal: fix masking and loudness on one song end to end.
4. **Week 5: Musical layer.** Key, chords, pitch tracking, out-of-key detection, beat grid, then pitch correction and quantize actions.
5. **Week 6: Evaluation harness.** Build the test set and run the benchmark described below.
6. **Week 7: Demo + write-up.** Web app, before/after video, README and blog post.
7. **Stretch:** `generate_part` for chord-aware basslines or harmonies, reference-track matching, and a DAW connection through an existing Ableton MCP server.

## Evaluation plan

The headline result compares the agent with and without the verify-and-revert loop on the same task set.

**Test set.** About 50 tasks built by damaging clean multitracks on purpose, so the correct fix is known: boosted mud bands, a clashing pair of stems, a detuned note, a late drum hit, clipped peaks. Clean stems can come from open multitrack collections such as MUSDB18 or Cambridge-MT.

| Metric | Layer | Target direction |
| --- | --- | --- |
| Masking score between stems | Audio | Lower |
| Distance to target loudness (LU) | Audio | Lower |
| Spectral distance to reference | Audio | Lower |
| Out-of-key notes remaining | Musical | Lower |
| Timing error, mean ms | Musical | Lower |
| Task success rate (%) | Both | Higher |
| Changes reverted / tool calls per task | Agent | Lower |

**Ablations.** No verify loop; audio tools only; musical tools only. Add a small blind listening test with 5–10 people for a human check.

## Prior work and differentiation

Similar systems exist, but none found combine audio and theory diagnosis with measured verification and a public benchmark.

| Project | What it does | Gap this project fills |
| --- | --- | --- |
| [MusicAgent](https://microsoft.github.io/muzic/musicagent) (Microsoft, 2023) | LLM orchestrates music understanding and generation tools | No self-verification loop or repair focus |
| [Loop Copilot](https://arxiv.org/abs/2310.12404) (2023) | LLM picks specialized models for iterative loop editing; keeps a Global Attribute Table | Evaluated by interviews, no automatic metrics, no public code |
| [Ableton MCP](https://github.com/MCPBlender/ableton-mcp) and forks | Lets an LLM control an Ableton Live session | Remote control only; no listening or measurement |
| [MusicForge](https://github.com/csa7mdm/MusicForge) | LLM plans, MusicGen and Bark generate | Generation wrapper, no analysis |
| [samplespace](https://github.com/topics/music-production-tools) | Sample search by sound with agentic orchestration | Library search, not mix or theory repair |
| [fls-pilot](https://github.com/topics/music-production-tools) | FL Studio MCP assistant for mix reviews and rollback-first edits | Closest in spirit; no theory layer or benchmark |

Worth borrowing: Loop Copilot's attribute table as the agent's song state, and an existing Ableton MCP server as a later action layer.

## Portfolio deliverables

- [ ] Public GitHub repo with tested tools, MCP server and agent loop
- [ ] Live demo (e.g. Hugging Face Spaces): upload stems, type a request, hear before/after, see the reasoning trace
- [ ] 30–60 second before/after video for LinkedIn or X
- [ ] README with architecture diagram and benchmark table
- [ ] Blog post on design decisions, failures and ablation results

Target résumé line: "Built a music repair agent with 14 custom DSP and theory tools and a verify-and-revert loop that raised task success from X% to Y%."

## Open questions and next step

- Input format for v1: stems only, or also full mixes (which would need stem separation with a pretrained model such as Demucs)?
- Which LLM plans the loop, and does it run through an agent SDK or a hand-written loop?
- Genre focus for the test set (e.g. pop/rock with vocals, drums, bass, guitar)?
- Where the demo runs, given audio processing cost.

**Next step:** write the JSON input/output schema for each tool in the inventory, then build `measure_loudness` and `detect_masking` first.
