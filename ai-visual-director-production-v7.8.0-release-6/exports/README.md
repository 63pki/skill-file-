# Production Package Exports

At Delivery Gate, create files only when the host actually supports file creation.

Preferred package when relevant and requested:

```text
[project]_MASTER_production_[version]_[status].pdf or .docx
[project]_PROMPTS_[version]_[status].txt
[project]_ASSETS_[version]_[status].csv or .json
[project]_SHOTS_[version]_[status].csv
[project]_AUDIO_CUES_[version]_[status].csv
[project]_OPERATOR_[version]_[status].md or .pdf
[project]_EVIDENCE_[version]_[status].md or .pdf
manifest.json
[project]_PACKAGE_[version]_[status].zip
```

Rules:

1. Export only latest approved artifacts.
2. Keep IDs stable across human-readable and machine-readable files.
3. Quote CSV safely and use UTF-8.
4. Generate hashes after final writes.
5. Open/parse each output and test archive integrity.
6. Do not claim an export when the host cannot create files.
7. Export creation never increases release maturity without inspection evidence.
