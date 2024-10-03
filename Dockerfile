# docker build . --build-arg USER_ID=$(id -u) --build-arg GROUP_ID=$(id -g) --build-arg PHP_VERSION=8.1 --build-arg PHP_CODESNIFFER_VERSION="3.8.1" -t any-php:8.1
# docker run --rm -it -v $(pwd):/home/www-data any-php:8.1

ARG PHP_VERSION=8.1

FROM php:${PHP_VERSION}-alpine

ARG USER_ID=1000
ARG GROUP_ID=1000
ARG PHP_CODESNIFFER_VERSION="3.8.1"

RUN apk update && \
    apk add --no-cache \
        php-simplexml \
        php-bcmath\
    shadow && \
    php -r "copy('https://getcomposer.org/installer', 'composer-setup.php');" && \
    php -r "if (hash_file('sha384', 'composer-setup.php') === 'dac665fdc30fdd8ec78b38b9800061b4150413ff2e3b6f88543c636f7cd84f6db9189d43a81e5503cda447da73c7e5b6') { echo 'Installer verified'; } else { echo 'Installer corrupt'; unlink('composer-setup.php'); } echo PHP_EOL;" && \
    php composer-setup.php && \
    php -r "unlink('composer-setup.php');" && \
    mv composer.phar /usr/local/bin/composer && \
    composer --version && \
    wget -c "https://github.com/PHPCSStandards/PHP_CodeSniffer/releases/download/${PHP_CODESNIFFER_VERSION}/phpcs.phar" -O /usr/local/bin/phpcs && \
    chmod +x /usr/local/bin/phpcs && \
    wget -c "https://github.com/PHPCSStandards/PHP_CodeSniffer/releases/download/${PHP_CODESNIFFER_VERSION}/phpcbf.phar" -O /usr/local/bin/phpcbf && \
    chmod +x /usr/local/bin/phpcbf && \
    usermod -u ${USER_ID} www-data && groupmod -g ${GROUP_ID} www-data

USER www-data
WORKDIR /home/www-data
