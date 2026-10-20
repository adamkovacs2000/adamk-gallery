If the preview size needs to be changed also edit files in layouts/partials
If the theme is updated also update these files accordingly

# BUILD Locally
hugo --minify 
hugo server
hugo server --bind 0.0.0.0 --baseURL http://10.1.0.xxx

# Build on server
git clone https://github.com/adamkovacs2000/adamk-gallery
git submodule update --init --recursive
docker compose up -d --build
configure reverse proxy