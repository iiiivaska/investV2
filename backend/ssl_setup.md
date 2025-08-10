# 🔒 Настройка SSL/HTTPS для InvestV2

## 📋 Требования

- Домен, указывающий на ваш сервер
- Root доступ к серверу
- Nginx установлен и настроен

## 🚀 Быстрая настройка SSL с Let's Encrypt

### 1. Установка Certbot

```bash
# Ubuntu/Debian
sudo apt update
sudo apt install certbot python3-certbot-nginx

# CentOS/RHEL
sudo yum install certbot python3-certbot-nginx

# или с snap
sudo snap install --classic certbot
sudo ln -s /snap/bin/certbot /usr/bin/certbot
```

### 2. Получение SSL сертификата

```bash
# Замените yourdomain.com на ваш домен
sudo certbot --nginx -d yourdomain.com -d www.yourdomain.com
```

### 3. Автоматическое обновление

```bash
# Проверяем автообновление
sudo certbot renew --dry-run

# Добавляем в cron для автоматического обновления
echo "0 12 * * * /usr/bin/certbot renew --quiet" | sudo crontab -
```

## 🔧 Ручная настройка SSL

### 1. Генерация самоподписанного сертификата (для тестирования)

```bash
# Создаем директорию для сертификатов
sudo mkdir -p /etc/ssl/investv2

# Генерируем сертификат
sudo openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
    -keyout /etc/ssl/investv2/private.key \
    -out /etc/ssl/investv2/certificate.crt \
    -subj "/C=RU/ST=State/L=City/O=Organization/CN=yourdomain.com"
```

### 2. Настройка Nginx с SSL

Отредактируйте конфигурацию Nginx (`nginx.conf.example`):

```nginx
server {
    listen 443 ssl http2;
    server_name yourdomain.com;

    ssl_certificate /etc/ssl/investv2/certificate.crt;
    ssl_certificate_key /etc/ssl/investv2/private.key;
    
    # ... остальная конфигурация
}
```

## 🛡️ Дополнительные настройки безопасности

### 1. Настройка SSL параметров

```nginx
# Современные SSL настройки
ssl_protocols TLSv1.2 TLSv1.3;
ssl_ciphers ECDHE-RSA-AES256-GCM-SHA512:DHE-RSA-AES256-GCM-SHA512:ECDHE-RSA-AES256-GCM-SHA384:DHE-RSA-AES256-GCM-SHA384;
ssl_prefer_server_ciphers off;
ssl_session_cache shared:SSL:10m;
ssl_session_timeout 10m;
```

### 2. HSTS (HTTP Strict Transport Security)

```nginx
add_header Strict-Transport-Security "max-age=31536000; includeSubDomains" always;
```

### 3. Безопасные заголовки

```nginx
add_header X-Frame-Options "SAMEORIGIN" always;
add_header X-XSS-Protection "1; mode=block" always;
add_header X-Content-Type-Options "nosniff" always;
add_header Referrer-Policy "no-referrer-when-downgrade" always;
```

## 🔍 Проверка SSL

### 1. Проверка конфигурации Nginx

```bash
sudo nginx -t
```

### 2. Проверка SSL сертификата

```bash
# Проверяем сертификат
openssl s_client -connect yourdomain.com:443 -servername yourdomain.com

# Проверяем с помощью curl
curl -I https://yourdomain.com
```

### 3. Онлайн проверки

- [SSL Labs](https://www.ssllabs.com/ssltest/)
- [Mozilla Observatory](https://observatory.mozilla.org/)

## 🔄 Обновление сертификатов

### Let's Encrypt (автоматически)

```bash
# Проверяем статус
sudo certbot certificates

# Обновляем вручную
sudo certbot renew

# Проверяем автообновление
sudo certbot renew --dry-run
```

### Ручное обновление

```bash
# Останавливаем Nginx
sudo systemctl stop nginx

# Обновляем сертификаты
sudo certbot renew

# Запускаем Nginx
sudo systemctl start nginx
```

## 🆘 Устранение неполадок

### Сертификат не обновляется

```bash
# Проверяем логи
sudo journalctl -u certbot

# Проверяем права доступа
sudo ls -la /etc/letsencrypt/live/yourdomain.com/
```

### Nginx не запускается

```bash
# Проверяем конфигурацию
sudo nginx -t

# Проверяем логи
sudo journalctl -u nginx
```

### SSL ошибки в браузере

1. Проверьте дату на сервере
2. Проверьте правильность домена в сертификате
3. Проверьте цепочку сертификатов

## 📞 Поддержка

При проблемах с SSL:

1. Проверьте логи: `sudo journalctl -u nginx`
2. Проверьте конфигурацию: `sudo nginx -t`
3. Проверьте сертификат: `sudo certbot certificates`
4. Создайте issue в GitHub с подробным описанием проблемы
