# AGENTS.md — contract for AI agents using this repo

Read this before you use anything in `component.html` or `css/styles.css`.

## What this repo is

A **prototyping reference** for RLP (Regulatory Licensing and Permitting), a Tyler
Technologies government licensing platform. It is a catalog of UX patterns extracted
from ~20 clickable HTML prototypes, maintained by the design side.

It is **not** a production component library. It has never been built, tested, or
shipped. Nothing here is generated from production source.

## The precedence rule

**The live RLP application is the source of truth for component styling. This repo is not.**

When this repo and the live app disagree about colour, size, spacing, border,
class name, or markup structure — **the live app wins**. Go look at the real app
and match it. Do not "fix" the app to match this repo.

## What this repo *is* authoritative for

Composition and page-level patterns, which are written down nowhere else:

- Which components combine to form a page, and in what order
- Icon Key accordion sits above the table controls bar
- Action bars are left-aligned, primary action first — **except** step/wizard
  pages, which use `justify-content: space-between` (Back left, Next right)
- Add-item forms sit *above* the table they grow
- Save/Cancel sit outside `profile-content`, directly in `<main>`
- Naming conventions: "Create New [Thing]", "All [Things]", "Please Select"
- Error-message wording and tone (see the Error Messaging foundations page)

**Use this repo for how RLP puts things together. Use the live app for how
individual components look.**

## Check the `fidelity` field on every entry

Every object in the `COMPONENTS` array in `component.html` carries a `fidelity` key.
It is not decoration. Read it before you copy anything.

| Value | Meaning | What you do |
|---|---|---|
| `verified` | Computed styles were read off the live app (qa.lnpweb.com, 2026-09-18) and match this markup. | Copy as-is. |
| `unverified` | Came from a prototype. **Never checked against the live app.** | Confirm against RLP before shipping. Treat the markup as a starting point, not a spec. |
| `proposed` | A design proposal that **deliberately differs** from the live app. | **Does not exist in the product yet.** Never build it as though it already ships. Raise it with the design owner first. |

As of 2026-09-18: **11 verified, 23 unverified, 1 proposed.** Most of this library
is unverified. Assume unverified unless the badge says otherwise.

## Hard prohibitions

1. **Never copy `css/styles.css` over the application's stylesheet.** It is a
   hand-maintained, prototype-grown approximation. It is genuinely derived from
   production in places (`#112e51` header, `#102f52` nav, `simple-card`) and
   genuinely wrong in others. It is not a production artifact and must not be
   treated as a drop-in replacement.

2. **Never introduce a class from this repo into production code without first
   confirming the live app defines it.** These classes are prototype-only and do
   **not** exist in RLP — shipping them produces unstyled output:

   | Prototype-only class | What RLP actually uses |
   |---|---|
   | `.section-heading` | `<h2 class="font-family-sans text-bold margin-top-0 margin-bottom-1">` |
   | `.field-required` | `<span class="required"><em>Required</em></span>` |
   | `.task-container` | `.simple-card bg-base-lightest padding-2 height-full` |
   | `.usa-table--striped` | RLP list tables are not striped |

3. **Never treat a `proposed` entry as an existing feature.**

4. **Do not add a style that conflicts with USWDS.** RLP is built on USWDS
   (US Web Design System). Check `css/styles.css` before inventing anything.

5. **There is no Tyler Forge in RLP.** Do not introduce `<forge-*>` components or
   `@tylertech/forge` packages. Confirmed with the design owner, 2026-09-18.

## Known-good production values

Verified by reading computed styles off the live agency pages on 2026-09-18.
Use these numbers over anything in `css/styles.css` that contradicts them.

```
html base font-size   10px          (so 1.6rem = 16px)
body colour           #444
font stack            "Public Sans Web", -apple-system, system-ui, "Segoe UI", …
main                  17px
p                     16px / #4c4c4c / line-height 25.6px
h2 (section heading)  24px / 700 / #4c4c4c / no border
.page-title           30px / 700 / #4c4c4c  (+ .page-title--underlined)
header bar            #112e51
primary nav bar       #102f52
nav item              14px / 700 / #fff / padding 15px
primary button        #005ea2, 16px, 700, #fff, padding 12px 24px, radius 4px
button hover          #1a4480          <-- navy is HOVER, not the base colour
button disabled       #c9c9c9
outline button        inset 0 0 0 2px #005ea2
breadcrumb            16px, links #005ea2
.usa-input            padding 8px, 1px border #565c65
accordion button      #f0f0f0, 16px, 700, padding 16px 24px
table th              16px / 700 / bg #f0f0f0 / padding 8px 16px
table td              16px / padding 20px 5px 20px 10px
table row border      1px #aeb0b5
data grid empty state <h2 class="h3">No data found</h2>  (20px / 400)
page container        .grid-container, max-width none, padding 0 32px
                      (.grid-container-rlp at 1100px is login/landing ONLY)
```

## Verifying something yourself

The live app inlines ~2.5 MB of CSS in a single `<style>` tag with no external
stylesheet, so there is no CSS file to diff. The way to check a component is to
open the page in a browser and read **computed styles** off the real element:

```js
const c = getComputedStyle(document.querySelector('.usa-button'));
[c.fontSize, c.fontWeight, c.color, c.backgroundColor, c.padding, c.borderRadius];
```

QA agency pages used for the 2026-09-18 pass:

```
/management/dashboard                  header, nav, page title, tiles
/management/license-type/view-all      data table, Icon Key accordion, controls bar
/management/cases/open                 breadcrumb, segmented filter tabs, form fields
```

Tables on both list pages returned zero rows, so row-level styling and the
Controls-column icon buttons are still unverified.

## If you find a discrepancy

Do not silently change either side. Add a note to the entry in `component.html`
recording what the live app actually does, set `fidelity` appropriately, and flag
it to the design owner. Silent edits are how the two sides drifted in the first
place.
