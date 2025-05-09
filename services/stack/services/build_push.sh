#/bin/bash

set -e

default_version="1"
version=${1:-"$default_version"}


docker build -t slyven/woodytoys:api-"$version" api/main
docker build -t slyven/woodytoys:api_products-"$version" api/products
docker build -t slyven/woodytoys:api_orders-"$version" api/orders
docker build -t slyven/woodytoys:api_misc-"$version" api/misc
docker build -t slyven/woodytoys:rp-"$version" reverse-proxy
docker build -t slyven/woodytoys:database-"$version" database
docker build -t slyven/woodytoys:front-"$version" front

docker push slyven/woodytoys:api-"$version"
docker push slyven/woodytoys:api_products-"$version"
docker push slyven/woodytoys:api_orders-"$version"
docker push slyven/woodytoys:api_misc-"$version"
docker push slyven/woodytoys:rp-"$version"
docker push slyven/woodytoys:database-"$version"
docker push slyven/woodytoys:front-"$version"
