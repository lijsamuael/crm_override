# CRM Apps Architecture & Override Mapping

> Reference guide for understanding how the CRM frontend apps are structured,
> which app serves which sites, and where to make changes.

## Apps Overview

| App | Purpose |
|-----|---------|
| `crm` | Base Frappe CRM — upstream, **do not modify** |
| `crm_override` | CRM frontend overrides for **most sites** (32 sites) |
| `crm_pipeline` | Extended CRM with pipeline features for **NJV/demo sites** (4 sites) |
| `fr8labs_custom_crm` | Backend-only customizations (doctypes, server scripts, API utils) |
| `frappe` | Core Frappe framework |
| `frappe_whatsapp` | WhatsApp integration |
| `insights` | Frappe Insights (analytics/reporting) |

## Site-to-App Mapping (as of 2025)

### Sites with `crm_override` only (32 sites)
These sites get the `crm_override` frontend:

accli, aci, ail, akm, astro, bkl, demoph, dgfbt, dgfid, dgfmy, dgfsg,
ffs, fmw, gltm, goglin, goglsg, jlog, kingsg, ksa, mmsg, ptmm, qil,
qml, qtq, spl, teg, template, tera, test, timl, tsg, tww

### Sites with BOTH `crm_override` + `crm_pipeline` (4 sites)
These sites get the `crm_pipeline` frontend (it wins because it's installed after `crm_override`):

demo, njvmy, njvsg, njvth

### Why `crm_pipeline` wins on dual-install sites

Frappe's `TemplatePage.set_template_path` iterates `reversed(get_installed_apps())`.
The last installed app that provides a `www/crm.html` template wins.
Since `crm_pipeline` is installed after `crm_override` in `apps.txt`, its frontend assets are served.

The backend API from `crm_override` still works on all sites since it's installed everywhere.

## Frontend Override Mechanism

Both `crm_override` and `crm_pipeline` use `custom-build.js`, but with a layered approach:

### crm_override build (2 layers)
```
1. Copy crm/frontend/src/ → crm_override/frontend/src/
2. Overlay crm_override/frontend/src_override/ on top
```

### crm_pipeline build (3 layers)
```
1. Copy crm/frontend/src/ → crm_pipeline/frontend/src/
2. Overlay crm_override/frontend/src_override/ (shared customizations)
3. Overlay crm_pipeline/frontend/src_override/ (pipeline-specific only)
```

This means `crm_pipeline` inherits all shared customizations from `crm_override` automatically.
Shared changes only need to be made once in `crm_override/src_override`.

**`src_override/` is the source of truth.** The `src/` directory is regenerated on every build.
Only edit files in `src_override/`. Changes to `src/` will be lost.

### crm_override overridden files (10 files — shared features)
```
App.vue
components/Layouts/AppSidebar.vue
components/Mobile/MobileSidebar.vue
components/Modals/ConvertToDealModal.vue
pages/Deal.vue
pages/Lead.vue
pages/MobileDeal.vue
pages/MobileLead.vue
pages/Search.vue
router.js
```

### crm_pipeline overridden files (25 files — pipeline-specific only)
```
components/Activities/AllModals.vue
components/Activities/NoteArea.vue
components/Activities/TaskArea.vue
components/Kanban/KanbanView.vue
components/Layouts/AppSidebar.vue
components/ListViews/PipelinesListView.vue
components/Mobile/MobileSidebar.vue
components/Modals/ConvertPipelineToDealModal.vue
components/Modals/NoteModal.vue
components/Modals/OrganizationModal.vue
components/Modals/PipelineModal.vue
components/Modals/TaskModal.vue
components/ViewControls.vue
pages/Lead.vue
pages/MobilePipeline.vue
pages/Pipeline.vue
pages/Pipelines.vue
router.js
stores/statuses.js
utils/callLog.js
utils/dashboard.ts
utils/dialogs.jsx
utils/index.js
utils/numberFormat.js
utils/view.js
```

## Where to Make Changes

### Frontend changes that affect ALL sites
Edit in **both** `src_override/` directories:
1. `crm_override/frontend/src_override/` — for the 32 override-only sites
2. `crm_pipeline/frontend/src_override/` — for the 4 NJV/demo sites

Then build both apps.

### Frontend changes that affect only NJV/demo sites
Edit only in `crm_pipeline/frontend/src_override/`.

### Frontend changes that affect only non-pipeline sites
Edit only in `crm_override/frontend/src_override/`.

### Backend API changes
- `crm_override/crm_override/api.py` — available on all sites (crm_override is installed everywhere)
- `fr8labs_custom_crm` — backend doctypes, server scripts, utilities

## Build Commands

### Build crm_override
```bash
cd frappe-bench
cd apps/crm_override/frontend && yarn build && cd ../../..
bench build --app crm_override
```

### Build crm_pipeline
```bash
cd frappe-bench
cd apps/crm_pipeline/frontend && yarn build && cd ../../..
bench build --app crm_pipeline
```

### After building, clear cache and restart
```bash
bench --site all clear-cache
bench restart
```

### Full rebuild sequence (both apps)
```bash
# crm_override
cd apps/crm_override/frontend && yarn build && cd ../../.. && bench build --app crm_override

# crm_pipeline
cd apps/crm_pipeline/frontend && yarn build && cd ../../.. && bench build --app crm_pipeline

# Finalize
bench --site all clear-cache && bench restart
```

## Key Files Reference

| File | Location | Purpose |
|------|----------|---------|
| Organization Search API | `crm_override/crm_override/api.py` | Backend search endpoint (all sites) |
| Organization Search UI | `*/frontend/src_override/pages/Search.vue` | Frontend search page (both apps) |
| Convert To Deal Modal | `crm_pipeline/frontend/src_override/components/Modals/ConvertToDealModal.vue` | Malaysia state/city fields (pipeline sites only) |
| Custom Build Script | `*/frontend/custom-build.js` | Override mechanism (both apps, identical logic) |
| Installed Apps Order | `sites/apps.txt` | Determines which frontend wins |
