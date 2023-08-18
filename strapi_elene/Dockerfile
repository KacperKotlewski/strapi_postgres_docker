FROM node:16-alpine as builder
WORKDIR /app
ARG NODE_ENV=development
COPY strapi_elene/package.json strapi_elene/yarn.lock ./
COPY .env .
RUN yarn install
COPY strapi_elene/. .


from builder as development
CMD ["yarn", "develop"]
# CMD ["tail", "-f", "/dev/null"]

from builder as production
RUN NODE_ENV=production
RUN yarn build
CMD ["yarn", "start"]


