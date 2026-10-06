# Google Drive Retention Policy

Drive is limited storage and is **not** the canonical archive.

## Keep

- Final published master MP4 only when useful for re-edit or reuse
- Final thumbnail
- Final voice WAV only when it has reuse/re-edit value
- Irreplaceable source assets
- Shared reusable binary assets that cannot live efficiently in GitHub

## Delete after production

- Frame sequences
- Preview renders
- Temporary audio
- Rejected thumbnail variants
- Intermediate exports
- Duplicate assets
- Cache/temp folders
- Reproducible generated media

## Retention

- During production: temporary files permitted.
- At publish: aggressive cleanup.
- At 30 days: retain only files useful for re-edit, reuse or audit.
- Shared assets: one canonical copy only.

## Rule

If it can be regenerated deterministically and cheaply, do not archive it in Drive.
