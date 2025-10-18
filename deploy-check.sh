#!/bin/bash

# ===========================================
# Deploy Check Script
# ===========================================
# Скрипт для проверки работоспособности развернутых сервисов
# 
# Использование:
#   ./deploy-check.sh [server_ip]
#
# Пример:
#   ./deploy-check.sh 83.147.246.172
#

set -e  # Выход при ошибке

# Цвета для вывода
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Параметры
SERVER_IP=${1:-"83.147.246.172"}
API_PORT=8007
FRONTEND_PORT=3007
API_URL="http://${SERVER_IP}:${API_PORT}"
FRONTEND_URL="http://${SERVER_IP}:${FRONTEND_PORT}"

# Счетчики
PASSED=0
FAILED=0

# Функция для вывода заголовка
print_header() {
    echo ""
    echo -e "${BLUE}========================================${NC}"
    echo -e "${BLUE}$1${NC}"
    echo -e "${BLUE}========================================${NC}"
}

# Функция для проверки с выводом результата
check_test() {
    local test_name=$1
    local test_command=$2
    
    echo -n "Проверка: $test_name... "
    
    if eval "$test_command" > /dev/null 2>&1; then
        echo -e "${GREEN}✓ PASSED${NC}"
        ((PASSED++))
        return 0
    else
        echo -e "${RED}✗ FAILED${NC}"
        ((FAILED++))
        return 1
    fi
}

# Функция для проверки HTTP endpoint
check_http() {
    local name=$1
    local url=$2
    local expected_code=${3:-200}
    
    echo -n "Проверка: $name... "
    
    local response=$(curl -s -o /dev/null -w "%{http_code}" "$url" --connect-timeout 5 --max-time 10)
    
    if [ "$response" = "$expected_code" ]; then
        echo -e "${GREEN}✓ PASSED${NC} (HTTP $response)"
        ((PASSED++))
        return 0
    else
        echo -e "${RED}✗ FAILED${NC} (HTTP $response, ожидалось $expected_code)"
        ((FAILED++))
        return 1
    fi
}

# ===========================================
# 1. Проверка Docker контейнеров
# ===========================================
print_header "1. Docker Контейнеры"

if command -v docker &> /dev/null; then
    echo "Docker установлен: $(docker --version)"
    echo ""
    
    # Проверка запущенных контейнеров
    echo "Запущенные контейнеры:"
    docker ps --filter "name=postgres" --filter "name=bot" --filter "name=api" --filter "name=frontend" --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}"
    echo ""
    
    # Проверка каждого контейнера
    check_test "PostgreSQL контейнер" "docker ps --filter 'name=postgres' --filter 'status=running' | grep -q postgres"
    check_test "Bot контейнер" "docker ps --filter 'name=bot' --filter 'status=running' | grep -q bot"
    check_test "API контейнер" "docker ps --filter 'name=api' --filter 'status=running' | grep -q api"
    check_test "Frontend контейнер" "docker ps --filter 'name=frontend' --filter 'status=running' | grep -q frontend"
else
    echo -e "${YELLOW}⚠ Docker не найден (проверка пропущена)${NC}"
fi

# ===========================================
# 2. Проверка API
# ===========================================
print_header "2. API Сервис"

echo "API URL: $API_URL"
echo ""

# Health endpoint
check_http "API Health Check" "$API_URL/health" 200

# API Documentation
check_http "API Docs" "$API_URL/docs" 200

# Stats endpoint (может быть 200 или другой код в зависимости от реализации)
if curl -s "$API_URL/api/stats/dashboard" --connect-timeout 5 --max-time 10 > /dev/null 2>&1; then
    echo -e "Проверка: API Stats Endpoint... ${GREEN}✓ PASSED${NC}"
    ((PASSED++))
else
    echo -e "Проверка: API Stats Endpoint... ${YELLOW}⚠ WARNING${NC} (endpoint недоступен, но это не критично)"
fi

# ===========================================
# 3. Проверка Frontend
# ===========================================
print_header "3. Frontend Сервис"

echo "Frontend URL: $FRONTEND_URL"
echo ""

check_http "Frontend доступен" "$FRONTEND_URL" 200

# ===========================================
# 4. Проверка логов (если docker доступен)
# ===========================================
if command -v docker &> /dev/null; then
    print_header "4. Логи Сервисов (последние 5 строк)"
    
    for service in postgres bot api frontend; do
        echo ""
        echo -e "${YELLOW}=== $service ===${NC}"
        container=$(docker ps --filter "name=$service" --format "{{.Names}}" | head -1)
        if [ -n "$container" ]; then
            docker logs "$container" --tail 5 2>&1 || echo "Не удалось получить логи"
        else
            echo "Контейнер не найден"
        fi
    done
    
    # Проверка на ошибки в логах API
    echo ""
    echo -n "Проверка: API логи на критичные ошибки... "
    container=$(docker ps --filter "name=api" --format "{{.Names}}" | head -1)
    if [ -n "$container" ]; then
        if docker logs "$container" --tail 50 2>&1 | grep -iE "(error|exception|failed)" | grep -v "404" > /dev/null; then
            echo -e "${YELLOW}⚠ WARNING${NC} (найдены ошибки в логах)"
        else
            echo -e "${GREEN}✓ PASSED${NC}"
            ((PASSED++))
        fi
    fi
fi

# ===========================================
# 5. Итоговый результат
# ===========================================
print_header "Итоговый результат"

TOTAL=$((PASSED + FAILED))
echo "Всего проверок: $TOTAL"
echo -e "Успешно: ${GREEN}$PASSED${NC}"
echo -e "Провалено: ${RED}$FAILED${NC}"
echo ""

if [ $FAILED -eq 0 ]; then
    echo -e "${GREEN}✓ Все проверки пройдены успешно!${NC}"
    echo -e "${GREEN}Приложение развернуто корректно.${NC}"
    exit 0
else
    echo -e "${RED}✗ Некоторые проверки не прошли.${NC}"
    echo -e "${YELLOW}Проверьте логи и конфигурацию сервисов.${NC}"
    exit 1
fi

