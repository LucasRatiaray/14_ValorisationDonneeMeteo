FROM node:24-alpine AS build

WORKDIR /app

# nuxt build depasse la heap on relève ce plafond à 4 Go
ENV NODE_OPTIONS=--max-old-space-size=4096

COPY package*.json .

RUN npm ci

COPY . .

RUN npm run build

FROM node:24-alpine AS prod

WORKDIR /app

COPY --from=build /app/.output /app/.output

ENV NODE_ENV=production \
    TZ=Europe/Paris

EXPOSE 3000

CMD [ "node", ".output/server/index.mjs" ]
