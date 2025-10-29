FROM oven/bun:1-alpine

WORKDIR /app

COPY package.json /app/package.json

RUN bun install
RUN bun run build
EXPOSE 4173

CMD [ "bun", "start" ]
