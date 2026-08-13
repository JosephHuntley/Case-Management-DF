# Place this file at: frontend/Dockerfile

FROM node:22-slim

WORKDIR /app

COPY package*.json ./
RUN npm install

COPY . .

EXPOSE 5173

# --host 0.0.0.0 is required so the dev server is reachable
# from outside the container (Vite binds to localhost by default)
CMD ["npm", "run", "dev", "--", "--host", "0.0.0.0"]
