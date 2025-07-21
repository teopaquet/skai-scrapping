# Dockerfile for React + Vite (auth-material-ui interface)
FROM node:20-alpine AS builder
WORKDIR /app
COPY src/interface/auth-material-ui/ .
RUN npm install --legacy-peer-deps && npm run build

FROM nginx:alpine
COPY --from=builder /app/dist /usr/share/nginx/html
COPY src/interface/auth-material-ui/nginx.conf /etc/nginx/conf.d/default.conf
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
