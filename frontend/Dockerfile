# Простой single-stage Dockerfile для Frontend (dev режим)
FROM node:20-alpine

# Рабочая директория
WORKDIR /app

# Установка pnpm глобально
RUN npm install -g pnpm

# Копирование файлов зависимостей
COPY package.json pnpm-lock.yaml ./

# Установка зависимостей
RUN pnpm install

# Копирование конфигов сначала
COPY next.config.ts ./
COPY tsconfig.json ./
COPY postcss.config.mjs ./
COPY components.json ./
COPY eslint.config.mjs ./

# Копирование исходного кода (весь src со всеми подпапками)
COPY src ./src

# Копирование публичных файлов
COPY public ./public

# Порт для Next.js dev server
EXPOSE 3000

# Запуск dev сервера
CMD ["pnpm", "dev"]

