---
#description: 
#lastmod: 2023-07-05
title: "Ádám Kovács"
description: Image Gallery

resources:
  - src: xxx.jpg
    params:
      cover: true # cover of the home page is used for OpenGraph cards, etc. --> social media
menus:
  main:
    name: Home
    weight: -1
# sub-galleries on list pages are sorted by date and weight (descending)
cascade:
  build:
    publishResources: false # do not include full images. Also disable download


---
