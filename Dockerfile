FROM hugomods/hugo:exts as builder

WORKDIR /src
COPY . .

# Initialize Hugo modules and build
#RUN git submodule update --init --recursive
RUN hugo --minify

FROM nginx:alpine
COPY --from=builder /src/public /usr/share/nginx/html
COPY nginx.conf /etc/nginx/conf.d/default.conf
EXPOSE 80