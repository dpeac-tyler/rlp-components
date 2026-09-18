# RLP Component Library

A cross-project reference catalog of the reusable UX components used in RLP
(Regulatory Licensing and Permitting) prototypes. Open `component.html` in a
browser — no build step, no dependencies.

Three columns per entry: name + live preview, HTML source, and usage notes.
Alphabetical, with an Icon Library and a set of foundations pages (status
colours, icons, error messaging).

## ⚠️ The live RLP application is the source of truth for component styling

**This library is not.** It is a design/prototyping reference, assembled by hand
from ~20 clickable HTML prototypes. Nothing in it has been built, tested, or
shipped, and none of it is generated from production source.

Where this library and the live app disagree on colour, size, spacing, class name
or markup — **match the live app**.

What this library *is* authoritative for is **composition**: which components
combine to form a page and in what order. That's the part that exists nowhere
else in writing — production has no spec saying "the Icon Key accordion sits
above the table controls bar." Use this library for how RLP puts things together,
and the live app for how individual components look.

## Fidelity badges

Every entry carries one of three badges, shown at the top of the entry and as a
coloured dot in the index:

- 🟢 **Verified against RLP** — computed styles were read off the live app
  (qa.lnpweb.com, 2026-09-18) and match. Safe to copy.
- 🟡 **Not verified against RLP** — came from a prototype, never checked against
  the live app. Confirm before shipping.
- 🟣 **Proposed — not in RLP yet** — a design proposal that deliberately differs
  from the live app. Does not exist in the product. Not a spec.

Current state: **32 verified · 7 unverified · 1 proposed** (40 entries).

The remainder is a statement about how much checking has been done, not a
judgement on the components — verification is manual and ongoing.

## For engineers and AI agents

Read **[AGENTS.md](AGENTS.md)** before using anything here. It carries the
precedence rule, the prohibitions, the list of prototype-only classes that must
never be shipped, and a table of known-good production values.

The two things that matter most:

1. **Never copy `css/styles.css` over the application's stylesheet.** It is a
   prototype-grown approximation — faithful to production in places, wrong in
   others. It is not a drop-in replacement.
2. **Never ship a class from here without confirming RLP defines it.**
   `.section-heading`, `.field-required`, `.task-container`, `.icon-button`,
   `.usa-pagination__*`, `.combo-box__*`, `.horizontal-tabs`, `.modal-overlay`
   and `.profile-content` are prototype-only and do not exist in RLP.
   (`.usa-table--striped` is also prototype-only, but keep it — RLP *is*
   striped, just via a different class.) Watch out for `.modal`: this repo's
   legacy one is a centring wrapper, RLP's **is** the dialog box.

## Stack

Static HTML + vanilla JS. Built on **USWDS** (US Web Design System);
`css/styles.css` is the compiled stylesheet. Base font size is 10px, so
`1.6rem = 16px`. There is **no Tyler Forge in RLP** — do not introduce
`<forge-*>` components.

## Verification history

| Date | What was checked | Result |
|---|---|---|
| 2026-09-18 (pass 1) | 14 components against QA (`qa.lnpweb.com`), agency-side | 11 verified identical; 3 real drifts corrected (section heading, required indicator, data-grid empty state); 1 documentation error fixed (primary button is `#005ea2`, navy `#1a4480` is hover) |
| 2026-09-18 (pass 6) | A genuine validation-error state | 32 verified. Inline field errors verified — colour, size and weight were already exact. Three corrections: the error message is a child of the `<label>` (not a sibling), RLP switches the state with `usa-label--error` rather than `usa-form-group--error` (which it doesn't have at all), and the error border is 4px not 3px. **No error summary alert appeared** — RLP showed inline errors only. Also added a **Step Indicator** entry; the CSS was already in the stylesheet but had no catalog entry. |
| 2026-09-18 (pass 5) | The application builder (create-application) | 30 verified, and **three new components added** that the library was missing entirely: the numbered **Step Section** panel (RLP's signature form chrome — orange CSS-triangle corner on a `#f0f0f0` panel), the **Quill rich-text editor** RLP uses in place of every textarea, and the **character counter**. Add-Item List verified — items stack with an accent-warm "Add More" below, no table. |
| 2026-09-18 (pass 4) | Tag, plus three more status values | 26 verified. `.usa-tag` had the right colours but five wrong properties — RLP's is 14px/weight 400/radius 2px/padding 1px 8px/display inline, not the stock-USWDS 12px/700/square. Corrected. All **five** status colours now verified byte-identical to the `.status-*` palette (`#417505`, `#8F5800`, `#A34900`, `#205493`, `#13669A`). |
| 2026-09-18 (pass 3) | 4 more components on the Individual Profile, incl. a live modal | 25 verified total. Horizontal tabs are RLP's `.sub-tabs` (equal-width flex, grey inactive, blue underline on active), not a custom `.horizontal-tabs`. Modals are `.react-confirm-alert-overlay` + `.modal[role=dialog]` + `.alert-heading`, with a **white 90%** scrim, not a dark one — and `.modal` collides with a legacy class in this repo. Alert left border corrected 5px → 8px; added a verified warning variant. `usa-button--unstyled` verified, but RLP uses it as a text link, not for icon-only controls. Noted that `.profile-content` / `.inspection-content` don't exist in RLP. |
| 2026-09-18 (pass 2) | 10 more components, incl. a populated 152-row grid | 21 verified total. Corrected an error from pass 1: RLP list tables **are** striped. Found the largest visual gap yet — row-action icon buttons are filled navy buttons with Font Awesome glyphs, not bare PNG links. Also corrected: `usa-button--secondary` is red `#d83933` (not an outline), pagination uses `.pagination-container` not `usa-pagination__*`, date inputs use a custom wrapper not `<input type="date">`. Status-text colours and the accent-warm button verified byte-identical. |

Production inlines ~2.5 MB of CSS in a single `<style>` tag with no external
stylesheet, so there is no CSS file to diff. Verification is done by reading
computed styles off real elements in the browser — see AGENTS.md for the method
and the pages used.

Still unverified (7): textarea, file input, the error *summary* alert,
document upload panel, both prototype-specific empty-state variants, and the
combobox.

Two are probably **negatives** rather than gaps: RLP's application builder has
no `<textarea>` at all (it uses a Quill rich-text editor), and no file-upload
control was found on the "Document Upload" wizard step — that step configures
document *types*.

The error alert and field-error entries need a form sitting in a validation-error
state — which means deliberately failing a save in QA, so that's a call for the
design owner rather than something to do unprompted.

## Maintaining this library

- Check here before building a component that might already exist; reuse the
  exact markup rather than inventing new HTML.
- Keep entries alphabetical. Include a short usage note and a `SOURCE:` line
  naming the file the markup came from.
- Set `fidelity` honestly. `unverified` is the correct default for anything
  lifted from a prototype without checking the live app.
- Never source components from the `rlp-3.0-*` or `rlp-3.1-*` directories —
  that is an in-progress redesign, not the current standard.
- When you find a discrepancy with production, record it in the entry's notes
  rather than silently changing either side.
