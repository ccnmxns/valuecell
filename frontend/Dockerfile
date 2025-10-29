FROM oven/bun:1-alpine

WORKDIR /app

COPY package.json /app/package.json

RUN bun install
RUN npm run build
EXPOSE 4173

CMD [ "npm", "run", "start" ]
