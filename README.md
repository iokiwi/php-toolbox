# PHP Toolbox

A personal collection of coping mechanisms for working with PHP for someone who's bread and butter is not PHP development but works with a php tech stack.

These tools are not necessarily written with php, they are whatever for working with php and other tools in the php ecosystem.

## parse_phpcs_report.py

A script for helping sift through reports from PHP_CodeSniffer.

Specifically, it groups findings by sniff and then lets us filter by sniff with
varying levels of detail.

```bash
phpcs -d memory_limit=512M -s . --report=json | parse_phpcs_report
# or
phpcs -d memory_limit=512M -s . --report=json > out.json
parse_phpcs_report -f out.json
```
Filter
```
parse_phpcs_report -f out.json -s Squiz.Strings.ConcatenationSpacing.PaddingFound Squiz.PHP.NonExecutableCode.Unreachable
1305  Squiz.Strings.ConcatenationSpacing.PaddingFound
10    Squiz.PHP.NonExecutableCode.Unreachable
```
Optionally, add the script to your path
```bash
sudo ln -s $(pwd)/parse_phpcs_report.py /usr/bin/parse_phpcs_report
```

## Dockerfile

A docker container for doing things with various versions of php  without having
to install php on my machine or screwing up host machine file permissions.

```bash
docker run --rm -it -v $(pwd):/home/www-data any-php:8.1 composer install
docker run --rm -it -v $(pwd):/home/www-data any-php:8.1 phpcs
docker run --rm -it -v $(pwd):/home/www-data any-php:8.1 phpcbf
```

Build the container image

```bash
docker build . \
    --build-arg PHP_VERSION=8.1 \
    --build-arg USER_ID=$(id -u) \
    --build-arg GROUP_ID=$(id -g) \
    -t any-php:8.1
```
