If the preview size needs to be changed also edit files in layouts/partials
If the theme is updated also update these files accordingly

# BUILD Locally
```bash
git clone https://github.com/adamkovacs2000/adamk-gallery
git submodule update --init --recursive
hugo --minify 
hugo server
hugo server --bind 0.0.0.0 --baseURL http://10.1.0.xxx
```

# Build on server
```bash
git clone https://github.com/adamkovacs2000/adamk-gallery
git submodule update --init --recursive
docker compose up -d --build
configure reverse proxy
```


# Sorting images in an album
Images are sorted by filename (ascending) by default. Set `params.sort_by` and
`params.sort_order` (`asc` / `desc`) in the album's `index.md` to change this.

## Custom weight-based order
This is a local extension in `layouts/partials/gallery.html` (not part of the
upstream theme). If the theme's `gallery.html` is updated, re-apply it.

Set `sort_by: Params.weight` and give the images you want on top a `weight`:

```yaml
params:
  sort_by: Params.weight
  sort_order: desc        # applies to images WITHOUT a weight only
resources:
  - src: first.jpg
    params:
      weight: 1
  - src: second.jpg
    params:
      weight: 2
```

- Images with a weight come first, **always ascending** (lowest weight first),
  regardless of `sort_order`. Images with the same weight are ordered by filename.
- Images without a weight follow, sorted by filename using `sort_order`.
- Albums that do not use `sort_by: Params.weight` behave as before.
- The `weight` here is per image (under `resources[].params`). The album's own
  top-level `weight` only controls its position on the homepage.
