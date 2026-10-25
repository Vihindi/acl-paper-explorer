# ACL Paper Explorer

A dependency-free GitHub Pages website. Filters all ACL Anthology paper metadata by comma-separated keywords (all/any), year, and venue checkboxes, including workshops. Exports every matched paper title and Anthology link, across all pages.

## Publish on GitHub
1. Create a GitHub repository and upload this folder's contents, including `.github`.
2. Use `main` as the default branch.
3. In Settings → Pages → Build and deployment, select **GitHub Actions**.
4. In Actions, run **Refresh anthology and deploy** (or push a commit).
5. Open the URL shown by the deployment.

The workflow downloads current metadata directly from acl-org/acl-anthology on every build and deploys daily at 00:17 UTC (05:47 Sri Lanka time). Updates depend on successful GitHub Actions runs; schedules can be delayed, and GitHub may disable schedules in inactive repositories. Run the workflow manually to refresh immediately. No API keys or paid services are required. PDFs stay on the official Anthology site.

## Local preview
Clone https://github.com/acl-org/acl-anthology into a separate `anthology` folder, then run:

    python scripts/build.py anthology
    python -m http.server 8000 --directory site

Visit http://localhost:8000. The generated index is not committed; production always rebuilds from upstream. Search covers titles, abstracts, and author names. Venue IDs come from volume metadata, with collection fallback for unclassified volumes. Front matter is excluded.

