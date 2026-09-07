# Localization Production Owner

## Trigger

Load for `LOCALIZATION`, alongside the base production mode and `MULTILINGUAL` audience overlay.

## Required controls

- Register locale, language, script direction, market, channel, legal variant, voice/caption owner, and reviewer.
- Preserve meaning, claims, names, units, dates, cultural context, and brand constraints.
- Measure text expansion, reading speed, caption duration, safe areas, line breaks, and voice timing.
- Treat machine translation as a draft unless the approved workflow says otherwise.
- Create RTL, accessibility, and multi-ratio adaptations where triggered.

## Required artifacts

1. Locale matrix and source-of-truth copy
2. Terminology and do-not-translate glossary
3. Translation/adaptation record
4. Caption and voice timing sheet
5. Layout expansion and RTL plan
6. Cultural, legal, and linguistic review record
7. Locale-specific package manifest

## Fail conditions

Reject silent claim changes, text clipping, wrong directionality, unreviewed regulated copy, mismatched voice/caption meaning, false native-review claims, or one export presented as all locales.
