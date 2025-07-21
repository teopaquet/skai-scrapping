# Dockerfile for React + Vite (auth-material-ui interface)
FROM node:20-alpine AS builder
WORKDIR /app
COPY src/interface/auth-material-ui/ .
RUN npm install --legacy-peer-deps && npm run build

FROM nginx:alpine
COPY --from=builder /app/dist /usr/share/nginx/html
COPY src/interface/auth-material-ui/nginx.conf /etc/nginx/conf.d/default.conf
EXPOSE 8080
CMD ["/bin/sh", "-c", "sed -i 's/listen [0-9]*;/listen ${PORT};/' /etc/nginx/conf.d/default.conf && nginx -g 'daemon off;'"]
