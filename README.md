# Drawmate

## Announcement

Drawmate is being rewritten in C# with a new architecture focused on generalized, schema-driven diagram generation for draw.io.

This repository currently contains the legacy implementation and historical artifacts. The rewrite will replace the matrix-first engine with a more extensible Diagram as Code model.

## New Core Library: Check it out!

The rewrite is built on DrawmateLib:

- <https://github.com/lando-tech/DrawmateLib>

DrawmateLib is the XML/draw.io generation foundation for the next version of Drawmate.

## Roadmap

1. Move from matrix-specific generation to a generalized, predictable JSON schema.
2. Keep draw.io XML as the output target while improving composability and complexity support.
3. Evolve Drawmate into a Diagram as Code workflow.
4. Add transpiler workflows (for example, Terraform to Drawmate JSON schema to draw.io output).

## Product Direction Note

The core Diagram as Code capabilities will continue to be developed openly.

## Current Repository Status

- This repository reflects the current/legacy generation approach.
- Existing examples and docs are being retained temporarily for reference during migration.
- A migration guide and updated schema documentation will be added as the C# rewrite matures.

## Author

- Aaron Newman
