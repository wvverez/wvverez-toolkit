#!/usr/bin/env bash

set -euo pipefail
export DEBIAN_FRONTEND=noninteractive

ROOT_PASS='abc123.'
DB_NAME='wordpress_ud1'; DB_USER='wpuser'; DB_PASS='wp1234'
WP_DIR='/var/www/html/wordpress'
SITE_TITLE='Mi sitio WordPress'; ADMIN_USER='admin'; ADMIN_PASS='Admin123.'; ADMIN_EMAIL='admin@example.com'

msg() { echo "[+] $*"; }
[[ $EUID -eq 0 ]] || { echo "[!] Ejecuta como root (sudo)"; exit 1; }

msg "Actualizando la máquina..."
apt-get update -qq && apt-get full-upgrade -y -qq

msg "Instalando Apache..."
apt-get install -y -qq apache2 wget curl openssl

msg "Instalando MariaDB..."
apt-get install -y -qq mariadb-server

msg "Asegurando MariaDB (equivalente a mariadb-secure-installation)..."
mariadb -u root <<SQL || mariadb -u root -p"$ROOT_PASS" -e "SELECT 1" >/dev/null
ALTER USER 'root'@'localhost' IDENTIFIED BY '$ROOT_PASS';
DROP USER IF EXISTS ''@'localhost';
DROP USER IF EXISTS ''@'$(hostname)';
DELETE FROM mysql.user WHERE User='root' AND Host NOT IN ('localhost','127.0.0.1','::1');
DROP DATABASE IF EXISTS test;
FLUSH PRIVILEGES;
SQL

msg "Creando base de datos y usuario de WordPress..."
mariadb -u root -p"$ROOT_PASS" <<SQL
CREATE DATABASE IF NOT EXISTS $DB_NAME DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
CREATE USER IF NOT EXISTS '$DB_USER'@'localhost' IDENTIFIED BY '$DB_PASS';
GRANT ALL PRIVILEGES ON $DB_NAME.* TO '$DB_USER'@'localhost';
FLUSH PRIVILEGES;
SQL

msg "Instalando PHP y módulos..."
apt-get install -y -qq php php-mysql php-xml php-gd php-curl php-zip php-mbstring php-cli php-json php-intl php-imagick
systemctl restart apache2

msg "Descargando WordPress (español)..."
cd /tmp
wget -q -O latest.tar.gz https://es.wordpress.org/latest-es_ES.tar.gz
tar -xzf latest.tar.gz

msg "Copiando WordPress a $WP_DIR..."
[[ -d $WP_DIR ]] || cp -r wordpress /var/www/html/

msg "Generando wp-config.php..."
cp -n "$WP_DIR/wp-config-sample.php" "$WP_DIR/wp-config.php"
sed -i "s/database_name_here/$DB_NAME/; s/username_here/$DB_USER/; s/password_here/$DB_PASS/" "$WP_DIR/wp-config.php"
for k in AUTH_KEY SECURE_AUTH_KEY LOGGED_IN_KEY NONCE_KEY AUTH_SALT SECURE_AUTH_SALT LOGGED_IN_SALT NONCE_SALT; do
  sed -i "s/'$k', *'put your unique phrase here'/'$k', '$(openssl rand -hex 32)'/" "$WP_DIR/wp-config.php"
done

msg "Ajustando permisos..."
chown -R www-data:www-data "$WP_DIR"
chmod -R 755 "$WP_DIR"

msg "Ejecutando el asistente de instalación..."
curl -s -o /dev/null -L \
  --data-urlencode "weblog_title=$SITE_TITLE" --data-urlencode "user_name=$ADMIN_USER" \
  --data-urlencode "admin_password=$ADMIN_PASS" --data-urlencode "admin_password2=$ADMIN_PASS" \
  --data-urlencode "pw_weak=1" --data-urlencode "admin_email=$ADMIN_EMAIL" \
  --data-urlencode "blog_public=0" --data-urlencode "language=es_ES" \
  "http://localhost/wordpress/wp-admin/install.php?step=2"

msg "Listo: http://localhost/wordpress  |  Panel: /wp-admin  ($ADMIN_USER / $ADMIN_PASS)"
