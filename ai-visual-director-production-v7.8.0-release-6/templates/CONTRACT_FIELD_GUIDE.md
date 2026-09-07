# Contract field guide

## Character locks

`locks.characters` is an array of objects. Every object requires a non-empty `assetId`. Do not use a bare string.

```json
[{"assetId":"CHAR-MILO-v01","proportions":"locked description"}]
```

## Durable resolution

- `originalProblem`: the persistent story problem.
- `temporaryHelp`: immediate relief that does not permanently close the problem.
- `permanentChange`: the visible change that prevents recurrence.
- `helperCanLeave`: boolean proving the helper is no longer required.
- `recurrencePrevented`: boolean; true only when the ending visibly prevents the same problem.
- `visualProofShot`: stable shot ID showing the permanent change.

## Repair action

`repairAction` is canonical. The legacy `repair` field is accepted only as a deprecated input alias and is normalized before validation.
