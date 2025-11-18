If the preview size needs to be changed also edit files in layouts/partials
If the theme is updated also update these files accordingly



# BUILD
hugo --minify 
hugo server



# SERVER BUILD AND PUBLISH

docker-compose up -d --build

# Check if it's running
docker-compose ps
docker-compose logs -f
