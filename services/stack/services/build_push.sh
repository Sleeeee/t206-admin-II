#/bin/bash

set -e

default_version="1"
version=${1:-"$default_version"}


docker build -t slyven/woodytoys:api-"$version" api 
docker build -t slyven/woodytoys:rp-"$version" reverse-proxy
docker build -t slyven/woodytoys:database-"$version" database
docker build -t slyven/woodytoys:front-"$version" front

docker push slyven/woodytoys:api-"$version"
docker push slyven/woodytoys:rp-"$version"
docker push slyven/woodytoys:database-"$version"
docker push slyven/woodytoys:front-"$version"
