FROM oven/bun:1-alpine AS builder

WORKDIR /app

COPY package.json /app/package.json
RUN bun install
COPY . /app
RUN bun run build-prod

FROM nginx:alpine

WORKDIR /app

COPY --from=builder /app/dist /app
COPY ./nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 4173
CMD ["nginx", "-g", "daemon off;"]
