#!/bin/bash

# Nombre : AutoWP
# Creador : wvverez
# Github : https://github.com/wvverez
# Instalación LAMP + Wordpress Kubuntu/ Ubuntu 24


# Paleta Colores

RED='\e[1;31m'
GREEN='\e[1;32m'
YELLOW='\e[1;33m'
BLUE='\e[1;34m'
MAGENTA='\e[1;35m'
CYAN='\e[1;36m'
RESET='\e[0m'

cleanup() {
    printf "\n${RED}[+] Abandonando el script ...${RESET}\n"
    exit 1
}

trap cleanup INT

printf "\n${BLUE}----------------------------------------------${RESET}\n"
printf "\n${BLUE}[+] Author: wvverez...${RESET}\n"
printf "\n${BLUE}[+] https://github.com/wvverez${RESET}\n"
printf "\n${BLUE}----------------------------------------------${RESET}\n"

# Variables

WP_DIR="MiWordpress"
DB_NAME="MiWordpress"
DB_USER="wpuser"
DB_PASS="Con_seña_2025!"
PHP_VERSION="8.3"

# Mirar si es root

if [ "$EUID" -ne 0 ]; then
    echo -e "${RED}[+] Este script debe ejecutarse como root pedazo de chorvo...${RESET}"
    exit 1
fi
echo ""
echo -e "${CYAN}[+] Iniciando instalación LAMP + WordPress...${RESET}\n"

# Paso 1 Actualización sistema upgradeos y instalar repos

echo -e "${BLUE}[1/9] Actualizando sistema y repositorios...${RESET}"
add-apt-repository ppa:ondrej/php -y 2>&1
apt update && apt upgrade -y 2>&1
echo -e "${GREEN}[+] Sistema actualizado && upgradeado ${RESET}\n"

# Paso 2 Instalación apache

echo -e "${BLUE}[2/9] Instalando Apache...${RESET}"
apt install apache2 -y >/dev/null 2>&1
systemctl start apache2 -y >/dev/null 2>&1
ufw allow http >/dev/null 2>&1
ufw allow https >/dev/null 2>&1
systemctl enable apache2 >/dev/null 2>&1
systemctl restart apache2 >/dev/null 2>&1
echo -e "${GREEN}[+] Apache operativo${RESET}\n"

# Paso 3 Instalación MYSQL

echo -e "${BLUE}[3/9] Instalando MySQL...${RESET}"
apt install mysql-server -y >/dev/null 2>&1
systemctl enable mysql >/dev/null 2>&1
systemctl start mysql >/dev/null 2>&1
echo -e "${GREEN}[+] MySQL en ejecución${RESET}\n"

# Paso 4 Instalación del PHP y dependencias

echo -e "${BLUE}[4/9] Instalando PHP ${PHP_VERSION} y extensiones...${RESET}"
apt install -y \
php${PHP_VERSION} \
libapache2-mod-php${PHP_VERSION} \
php${PHP_VERSION}-mysql \
php${PHP_VERSION}-cli \
php${PHP_VERSION}-common \
php${PHP_VERSION}-curl \
php${PHP_VERSION}-xml \
php${PHP_VERSION}-mbstring \
php${PHP_VERSION}-zip \
php${PHP_VERSION}-gd \
php${PHP_VERSION}-soap \
php${PHP_VERSION}-intl >/dev/null 2>&1
systemctl restart apache2 >/dev/null 2>&1
echo -e "${GREEN}[+] PHP listo${RESET}\n"

# Paso 5 Configuración DB

echo -e "${BLUE}[5/9] Configurando base de datos WordPress...${RESET}"
mysql <<EOF
CREATE DATABASE IF NOT EXISTS ${DB_NAME} DEFAULT CHARACTER SET utf8 COLLATE utf8_unicode_ci;
CREATE USER IF NOT EXISTS '${DB_USER}'@'localhost' IDENTIFIED BY '${DB_PASS}';
GRANT ALL PRIVILEGES ON ${DB_NAME}.* TO '${DB_USER}'@'localhost';
FLUSH PRIVILEGES;
EOF
echo -e "${GREEN}[+] Base de datos creada${RESET}\n"

# Paso 6 Instalación WP

echo -e "${BLUE}[6/9] Descargando WordPress...${RESET}"
apt install curl -y >/dev/null 2>&1
cd /tmp || exit
curl -O https://wordpress.org/latest.tar.gz >/dev/null 2>&1
tar -xvzf latest.tar.gz >/dev/null 2>&1
mv wordpress /var/www/html/${WP_DIR}
rm latest.tar.gz
echo -e "${GREEN}[+] WordPress descargado${RESET}\n"

# Paso 7 Asignación permisos usuario por defecto Apache 

echo -e "${BLUE}[7/9] Asignando permisos...${RESET}"
chown -R www-data:www-data /var/www/html/${WP_DIR}
chmod -R 755 /var/www/html/${WP_DIR}
echo -e "${GREEN}[+] Permisos aplicados${RESET}\n"

# Paso 8 VH apache

echo -e "${BLUE}[8/9] Configurando Apache VirtualHost...${RESET}"
cat <<EOF > /etc/apache2/sites-available/${WP_DIR}.conf
<VirtualHost *:80>
    ServerAdmin webmaster@localhost
    DocumentRoot /var/www/html/${WP_DIR}
    ServerName localhost
    <Directory /var/www/html/${WP_DIR}>
        AllowOverride All
        Require all granted
    </Directory>
</VirtualHost>
EOF
a2ensite ${WP_DIR}.conf >/dev/null 2>&1
a2enmod rewrite >/dev/null 2>&1

# Para recargar Apache 
systemctl reload apache2 >/dev/null 2>&1

# Verificar si el comando 'ss' está instalado (usado para ver puertos)
if ! command -v ss &> /dev/null
then
    echo -e "${YELLOW}[+] 'ss' no está instalado. Instalando 'iproute2'...${RESET}"
    sudo apt update -y
    sudo apt install -y iproute2
else
    echo -e "${GREEN}[+] 'ss' ya está instalado.${RESET}"
fi

# Verificar si el comando netstat está instalado (opcional)
if ! command -v netstat &> /dev/null
then
    echo -e "${YELLOW}[+] 'netstat' no está instalado. Instalando 'net-tools'...${RESET}"
    sudo apt update -y
    sudo apt install -y net-tools
else
    echo -e "${GREEN}[+] 'netstat' ya está instalado.${RESET}"
fi

# Verificar si Apache está funcionando corriendo

echo -e "${BLUE}[+] Verificando estado de Apache...${RESET}"
systemctl status apache2 | grep "Active:"

# Verificar si Apache está escuchando en el puerto 80 con ss o netstat
echo -e "${BLUE}[+] Verificando puerto 80...${RESET}"
if command -v ss &> /dev/null; then
    sudo ss -tuln | grep :80
else
    sudo netstat -tulnp | grep :80
fi

echo -e "${GREEN}[+] VH Apache configurado${RESET}\n"


# Paso 9 Configuración WP

echo -e "${BLUE}[9/9] Configurando WordPress...${RESET}"
cd /var/www/html/${WP_DIR}
cp wp-config-sample.php wp-config.php
sudo chown -R www-data:www-data /var/www/html/${WP_DIR}
sudo chmod -R 755 /var/www/html/${WP_DIR}
sed -i "s/database_name_here/${DB_NAME}/" wp-config.php
sed -i "s/username_here/${DB_USER}/" wp-config.php
sed -i "s/password_here/${DB_PASS}/" wp-config.php
echo -e "${GREEN}[+] WordPress configurado${RESET}\n"

echo -e "${RED}=============================================${RESET}"
echo -e "${GREEN}[+] Instalación completada${RESET}"
echo -e "${YELLOW}[+] Accede a WordPress:${RESET}"
echo -e "${YELLOW}    http://localhost/wp-admin/install.php${RESET}"
echo -e "${RED}=============================================${RESET}"
