# Worked reminder: joined evidence and a task-wide maximum

Development example from [QR-C1/2/3](../evaluation/quality-preview-reader-v1/REPORT.md), not a fresh confirmation test or a validated behavioral repair.

## A missing field in one record need not be missing evidence

An acquisition ledger identifies the task object, all task samples OS and physical channel OK-6. A separate calibration table assigns the OK-6 correction and error bound. That table deliberately contains no object assignment: the ledger supplies it. The complete claim uses the join, not either record alone.

Before reporting a missing link, name the exact premise and check whether the delivered records establish it together. A table's local limitation does not erase the ledger's applicable assignment. Keep genuine uncertainty: the resulting maximum interval [7.85,8.85] still straddles the8.6threshold. Removing an unsupported scope doubt does not make the task resolved or the favorable claim reusable.

Conversely, joining merely similar names or incompatible versions does not establish a premise. This reminder assumes the fixture's exact-key, coverage and accepted measurement contracts; it does not authenticate real sources.

## The greatest raw reading need not determine the physical maximum

With physical value = raw + .55 + residual and |residual|<=.45 bounded for each sample (no cancellation assumption), the supplied readings give:

| Raw sample | Allowed physical interval |
|---:|---:|
|14.4|[14.5,15.4]|
|15.1|[15.2,16.1]|
|14.8|[14.9,15.8]|

For a task requiring every physical sample<=15.7, the current maximum is bounded by [15.2,16.1]. Even learning that the15.1rawsample has physical value exactly15.65 would leave the third sample's upper bound15.8above the task limit. For example, physical samples [14.95,15.65,15.35] comply, while [14.95,15.65,15.75] violate; both fit the original per-sample bounds and that same exact middle value.

A single sample's lower bound above the limit can establish a violation. Establishing compliance requires bounding every remaining candidate for a violation; already settled samples need no redundant measurement. A proposed check may distinguish some outcomes without guaranteeing complete resolution. Say which it can settle rather than promising a task-wide certificate from one component.

The observed reader contrast and explanation defects are preserved in the study. This logical reminder is usable optional guidance; its behavioral benefit has not been tested.
