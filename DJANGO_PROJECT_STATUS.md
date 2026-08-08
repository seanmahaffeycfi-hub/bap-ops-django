# BAP Ops Django — Project Status / Handoff Notes

Last updated: August 8, 2026

This file exists so a future Claude session can pick up exactly where this one left off. Keep this file at the root of `bap-ops-django` and update it as work progresses. This is the companion file to `PROJECT_STATUS.md` in the `bap-ops-android` repo — that file covers the Android app's status separately.

## ✅ CURRENT STATE: FULL WEB DASHBOARD BUILT AND WORKING LOCALLY

All four dashboard sections (Expenses, Donations, Inventory, Mileage) are built, styled per the Bloom Again brand guide (with an intentional typography deviation — see below), and running locally via `python manage.py runserver`. Backend uses local SQLite, not Supabase/Postgres (deliberate decision, see below). Nothing has been deployed anywhere yet — this all currently only runs on the user's own dev machine, not the dedicated Windows 11 "unused machine" that's the eventual target (that machine is not yet set up/accessible).

## What this project is

The Django backend + web dashboard half of the BAP Ops system (the Android app half lives in the separate `bap-ops-android` repo). Tracks a 1099 business + the Bloom Again Project (BAP) nonprofit's operations across four domains: Expenses, Donations, Vase Inventory, and Auto Mileage.

## Key decisions made this session

- **Database: local SQLite, not Supabase/Postgres.** This app is intended to run entirely on a dedicated local Windows 11 machine, reachable only over home Wi-Fi (matching the Android app's Wi-Fi-gated sync design) — never exposed to the public internet. Given single-household usage and low write volume, SQLite's single-writer limitation is a non-issue, and it avoids all the complexity of managing a remote DB connection (secrets, SSL, network access) for a system that's local-only by design. This is a deliberate departure from CFE (which does use Supabase) — the two projects have different deployment models and that's fine.
- **Four Django apps**, one per domain: `expenses`, `donations`, `inventory` (holds both `VaseReceived` and `VaseReturned`), `auto` (holds `MileageEntry`). Models mirror the Android Room entities field-for-field where practical, using the exact same string values (`TAX_1099`, `NONPROFIT_501`) for the 1099/501 tag so the eventual sync payload needs no translation layer. Shared choices live in `bap_ops_django/choices.py`.
- **`django-axes`** wired in for login rate-limiting, same pattern as CFE.
- **Whitenoise** handles static files — no separate CDN/S3 needed for a local-only deployment.
- **Typography intentionally deviates from the Bloom Again brand guide.** The guide specifies Cormorant Garamond (display) + DM Sans (body) + Playlist Script (accent, licensed/unavailable). This app was deemed to serve more than just BAP's public-facing brand — it's equally a 1099 business tool — so the user chose **League Spartan** (headings) + **Elms Sans** (body) instead, both free via Google Fonts. Everything else from the brand guide (all 6 colors, the 8-point spacing scale, card/button/form component specs) is applied faithfully and unchanged. `static/css/style.css` is the single source of truth for all of this — new templates automatically inherit correct styling by extending `templates/base.html`, no per-page theming work needed.
- **User wants full copy-paste-ready code for entire files, not fragments** (except genuine 1-2 line changes) — same working style as the Android side.

## Known gap, intentionally deferred, not a bug

**"Lost or broken vases"** was specified in the original requirements (`a. total vases | vases out | vases in | lost or broken vases`) but **no field exists anywhere — Android or Django — to track vase condition or loss.** The Inventory dashboard currently shows this stat as an explicit "Not tracked yet" placeholder (`inventory/views.py` has a `lost_or_broken_tracked = False` flag and a code comment explaining this). Fixing this properly requires: a new field on `VaseReturned` (or a new model) on both the Android Room side and here, a migration on both, and an Android UI update to `VaseReturnedEntryActivity`/its layout — a real cross-repo change, not just a Django-side fix. Do this deliberately when both sides can be updated together, not piecemeal.

## Current file inventory

**Project root:** `requirements.txt`, `.gitignore`, `.env.example` (template only, no real secrets — real secrets live in `.env`, which is git-ignored and must be created locally per-machine).

**Settings:** `bap_ops_django/settings.py` — env-driven via `python-decouple`, local SQLite database, `django-axes` + `whitenoise` wired in, `STATICFILES_DIRS` pointing at the project-root `static/` folder. `bap_ops_django/choices.py` holds the shared `RECORD_TYPE_CHOICES`. `bap_ops_django/urls.py` routes `/`, `/expenses/`, `/donations/`, `/inventory/`, `/auto/`, `/admin/`. `bap_ops_django/views.py` has the `home` view.

**Models** (all registered in Django admin):
- `expenses/models.py` — `Expense` (date, description, amount, record_type, is_car_expense, receipt_image_url, ocr_raw_text, created_at)
- `donations/models.py` — `Donation` (date, description, value, donor_name, receipt_generated, created_at)
- `inventory/models.py` — `VaseReceived` (date_received, quantity, poc_name, poc_facility_name, poc_phone, poc_email, recipient, created_at) and `VaseReturned` (date_returned, quantity, returned_from, created_at)
- `auto/models.py` — `MileageEntry` (date, start_mileage, end_mileage, record_type, start_lat/lng, end_lat/lng, created_at; has a `miles_driven` property)

**Views/templates — all four fully built:**
- **Expenses** (`expenses/views.py` + `templates/expenses/expense_list.html`) — filterable by tag (1099/501) and car-expense-only, sortable by date/amount, shows totals for 1099, 501, and car expenses.
- **Donations** (`donations/views.py` + `templates/donations/donation_list.html`) — sortable by date/value, shows total donation value.
- **Inventory** (`inventory/views.py` + `templates/inventory/inventory_dashboard.html`) — total received / vases out / vases in (returned) / lost-or-broken (placeholder), plus a per-recipient "who's currently holding how many, oldest delivery first" breakdown (computed by matching `VaseReceived.recipient` against `VaseReturned.returned_from`).
- **Mileage** (`auto/views.py` + `templates/auto/mileage_dashboard.html`) — year-selector dropdown, yearly mileage totals split by 1099/501, full entry table (date/start/end/miles/tag).

**Styling:** `static/css/style.css` (brand-guide colors/spacing/components, League Spartan + Elms Sans fonts), `templates/base.html` (shared nav + font/CSS loading, all four dashboard templates extend this).

## Not started yet

- No API layer (Django REST Framework or similar) for the Android app to sync to — this is the next real dependency for the Wi-Fi-gated sync feature on the Android side.
- No receipt image storage — the `receipt_image_url` field exists on `Expense` but nothing populates or serves it yet. Originally planned as a Supabase Storage bucket, but that decision predates the SQLite-not-Supabase pivot — **needs revisiting.** Likely candidate now: just store images as local files on the same machine this Django app runs on, served via a Django media directory, consistent with the "everything local" architecture. Not yet decided for certain.
- Donor receipt generation for the Donations flow.
- The dedicated Windows 11 machine this is meant to ultimately run on is not yet set up or accessible — everything so far has been tested on the user's own dev machine only.
- Deployment/production settings (currently `DEBUG=True` for local dev) — will need real hardening (`DEBUG=False`, real `ALLOWED_HOSTS` for the LAN machine's IP/hostname, etc.) once that machine is available.
- `PROJECT_STATUS.md` in the `bap-ops-android` repo has not yet been updated to reflect that Django backend work has started — worth syncing that file too next time either repo is touched, so both status files stay consistent with each other.

## Suggested next steps

1. Build the Django REST Framework API layer that the Android app will sync to (this unblocks the Wi-Fi-gated sync work on the Android side).
2. Decide the receipt image storage approach now that Supabase is out of the picture for this project (likely: local media directory on the same machine).
3. Once the dedicated Windows 11 machine is available: get Django actually running on it, confirm it's reachable over the home network, and test the Android app's sync against a real target for the first time.