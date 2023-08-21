FROM node:16-alpine as builder
WORKDIR /app
ARG NODE_ENV=development
COPY strapi_app/package.json strapi_app/yarn.lock ./
RUN yarn install
COPY strapi_app/. .
COPY .env .


from builder as development
RUN yarn build
CMD ["yarn", "develop"]
# CMD ["tail", "-f", "/dev/null"]

from builder as production
RUN NODE_ENV=production
RUN yarn build
CMD ["yarn", "start"]


