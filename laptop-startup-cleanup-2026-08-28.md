---
date: 2026-08-28
type: note
tags: [windows, performance, maintenance]
description: Startup/RAM cleanup on the Dell laptop — what was disabled and how to reverse it
---
# Laptop Startup + RAM Cleanup — 2026-08-28

## Why
Felt performance degradation. Diagnosis: hardware fine (NVMe SSD healthy, CPU ~10%, disk 2% busy).
Real cause = RAM pressure (16 GB, 77% used, 3.7 GB free) + 15-day uptime + heavy startup sprawl.
Not degradation.

## What was changed
- **Edge**: closed all 17 processes (~1.2 GB) incl. the `--no-startup-window` background respawner.
  To stop it relaunching: edge://settings/system → turn off "Continue running background apps"
  and "Startup boost".
- **User startup (HKCU Run) → emptied (was 13):** Docker Desktop, AltServer, Sideloadly Daemon,
  ONVO TV, AppleIEDAV, iCloudDrive, ApplePhotoStreams, iCloudPhotos, ApidogAppAgent,
  MicrosoftEdgeAutoLaunch, Warp, Ferdium, io.tldv.desktop.
- **Admin startup (HKLM Run):** removed iTunesHelper + Nearby Share. KEPT SecurityHealth (Defender)
  + RtkAudUService (Realtek audio).
- **All-users Startup folder:** AnyDesk.lnk moved out (→ Desktop\AnyDesk.lnk.disabled).
- Docker confirmed NOT running.

## These are "remove from startup", NOT uninstalls. Apps still installed; open manually anytime.

## How to reverse
- User apps: `reg import` the backup `startup-run-backup.reg` (was in the Claude session scratchpad —
  may be gone after cleanup; if so re-add via Task Manager → Startup).
- Admin apps: `reg import "$env:USERPROFILE\Desktop\startup-hklm-backup.reg"` (elevated).
- AnyDesk: drag `Desktop\AnyDesk.lnk.disabled` back into
  `C:\ProgramData\Microsoft\Windows\Start Menu\Programs\StartUp`.

## Note
Same-engine fact: Edge/Chrome/Brave/Opera/Vivaldi all Chromium → similar per-tab RAM.
For a genuinely lighter browser, Firefox (Gecko, non-Chromium, aggressive tab-unloading) or
Brave (Chromium + built-in ad/tracker block). Not switched yet.
