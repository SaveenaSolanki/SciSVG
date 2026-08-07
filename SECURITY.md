# Security Policy

## Reporting a vulnerability

If you discover a security issue in the SciSVG website, tooling, workflows, or
any SVG asset (for example, an embedded script, external resource, or other
malicious content), please **do not open a public issue**.

Report it privately via a GitHub Security Advisory:

<https://github.com/SaveenaSolanki/SciSVG/security/advisories/new>

Please include:
- the affected file or URL,
- a description of the issue,
- steps to reproduce, and
- (if known) a suggested fix.

## SVG safety note

SVG files are XML and can contain scripts, external resources, and other
undesirable content. SciSVG runs automated validation on every contribution
(`scripts/validate_svgs.py`) that rejects scripts, event handlers, external
URLs, and embedded raster images, but distributed SVGs should still be treated
with standard caution: open them with scripting disabled in untrusted contexts,
and inspect any file before opening it in an editor or browser.

## Supported versions

| Version | Supported |
| ------- | --------- |
| main    | yes       |
| 0.1.x   | yes       |
