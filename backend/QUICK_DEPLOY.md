# ⚡ Быстрое развертывание InvestV2 на сервере

## 🚀 5 минут до запуска

### 1. Подготовка сервера
```bash
# Установка Docker (если не установлен)
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
sudo usermod -aG docker $USER

# Установка Docker Compose
sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose
```

### 2. Клонирование и настройка
```bash
# Клонируем репозиторий
git clone https://github.com/ваш-username/investV2.git
cd investV2/backend

# Настраиваем продакшн переменные
cp env.production .env

# Генерируем секретный ключ
SECRET_KEY=$(python3 -c "import secrets; print(secrets.token_urlsafe(32))")
sed -i "s/your-super-secret-production-key-change-this-immediately/$SECRET_KEY/" .env
```

### 3. Запуск
```bash
# Делаем скрипты исполняемыми
chmod +x deploy.sh migrate_production.sh

# Применяем миграции к внешней БД
./migrate_production.sh

# Запускаем приложение
./deploy.sh
```

### 4. Проверка
```bash
# Проверяем статус
docker-compose ps

# Проверяем health check
curl http://localhost:8000/health

# Открываем документацию
curl http://localhost:8000/docs
```

## 🔧 Настройка домена (опционально)

### 1. Установка Nginx
```bash
sudo apt update
sudo apt install nginx
```

### 2. Настройка конфигурации
```bash
# Копируем конфигурацию
sudo cp nginx.conf.example /etc/nginx/sites-available/investv2

# Редактируем домен
sudo nano /etc/nginx/sites-available/investv2

# Активируем
sudo ln -s /etc/nginx/sites-available/investv2 /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx
```

### 3. SSL сертификат
```bash
# Устанавливаем Certbot
sudo apt install certbot python3-certbot-nginx

# Получаем сертификат
sudo certbot --nginx -d yourdomain.com
```

## 📊 Управление

### Просмотр логов
```bash
# Все сервисы
docker-compose logs -f

# Только API
docker-compose logs -f api
```

### Обновление
```bash
./update.sh
```

### Остановка
```bash
docker-compose down
```

## 🔍 Проверка работы

### API endpoints
```bash
# Основной endpoint
curl http://localhost:8000/

# Health check
curl http://localhost:8000/health

# Документация
curl http://localhost:8000/docs
```

### База данных
```bash
# Проверка подключения
docker run --rm postgres:15-alpine psql "postgresql://gen_user:%1umkt{~ZFy#m4@192.168.0.4:5432/investv2" -c "SELECT 1;"
```

## 🆘 Если что-то не работает

1. **Проверьте логи**: `docker-compose logs api`
2. **Проверьте статус**: `docker-compose ps`
3. **Проверьте БД**: `./migrate_production.sh`
4. **Перезапустите**: `docker-compose restart api`

## 📞 Поддержка

- 📖 **Подробное руководство**: [DEPLOYMENT.md](DEPLOYMENT.md)
- 🔒 **SSL настройка**: [ssl_setup.md](ssl_setup.md)
- 🗄️ **Миграции БД**: [migrations/README.md](migrations/README.md)

---

**🎉 Готово!** Ваше приложение доступно по адресу: `http://localhost:8000`
