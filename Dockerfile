# Build the static site, then serve it with unprivileged nginx on :8080.
FROM python:3.12-slim AS build
WORKDIR /src
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
# pytest runs `zensical build --strict` into ./site
RUN pytest -q

FROM nginxinc/nginx-unprivileged:1.27-alpine
COPY nginx.conf /etc/nginx/conf.d/default.conf
COPY --from=build /src/site /usr/share/nginx/html
EXPOSE 8080
