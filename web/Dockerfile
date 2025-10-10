# --- build stage ---
FROM node:20-alpine AS build
WORKDIR /app
COPY package.json package-lock.json* ./
RUN npm ci || npm i
COPY . .
# default: proxy-style /api; override with ARG to bake a full URL
ARG VITE_API_BASE=/api
ENV VITE_API_BASE=$VITE_API_BASE
RUN npm run build

# --- serve stage ---
FROM nginx:1.27-alpine
COPY --from=build /app/dist /usr/share/nginx/html
COPY nginx.conf /etc/nginx/conf.d/default.conf
EXPOSE 80
