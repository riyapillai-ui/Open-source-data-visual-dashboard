---
name: Streamlit Replit setup
description: Environment constraints and startup flags for running Streamlit dashboards in this workspace.
---

Imported Python projects may have a Python interpreter but no pip-enabled development toolchain. Install the Replit Python Tools module before installing project packages. Streamlit workflows should include `--server.headless=true` and `--browser.gatherUsageStats=false` so first-run onboarding cannot block port detection.

**Why:** Without the Python tools module, package installation fails; without the headless and usage flags, Streamlit can pause for an interactive email prompt and the workflow never opens its preview port.

**How to apply:** For future Streamlit projects, verify pip-backed Python tooling first and include both startup flags in the configured web workflow.

Large Plotly scatter charts can auto-select WebGL, which may be unavailable in
the preview renderer. Use SVG rendering for these charts when broad preview
compatibility matters.

**Why:** The dashboard preview showed a blank chart area with a WebGL warning
even though the Streamlit server and data were healthy.

**How to apply:** Set `render_mode="svg"` on large `plotly.express.scatter`
charts used in Streamlit previews.