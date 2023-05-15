#!/bin/bash

SCRIPTPATH=$(dirname "${0}")

APP_IMAGE_NAME=${APP_IMAGE_NAME:-"gcr.io/mapr-252711/ezaf-spark-demo-example"}
APP_IMAGE_TAG=${APP_IMAGE_TAG:-"fy23-q2"}

DOCKERFILE=${DOCKERFILE:-"${SCRIPTPATH}/../dockerfiles/SparkJarLocal-3.3.1.Dockerfile"}
SPARK_APPLICATION=${SPARK_APPLICATION:-"${SCRIPTPATH}/../k8s/DataProcessTransfer-JarLocal.yaml"}

SRC_SPARK_JAR=${SPARK_JAR:-"${SCRIPTPATH}/../src/DataProcessTransfer/DataProcessTransfer.jar"}
DEST_SPARK_JAR=${DEST_SPARK_JAR:-"/tmp/DataProcessTransfer.jar"}

LDAP_USER=${LDAP_USER:-"user1"}

function build() {
    local colred='\033[0;31m' # Red
    local colwht='\033[0;37m' # White
    local colrst='\033[0m'    # Text Reset

    local SPARK_JAR_FILE
    SPARK_JAR_FILE=$(basename "${SRC_SPARK_JAR}")

    cp "${SRC_SPARK_JAR}" .
    echo "Building the ${APP_IMAGE_NAME}:${APP_IMAGE_TAG} image"

    docker build -t "${APP_IMAGE_NAME}":"${APP_IMAGE_TAG}" \
                --build-arg SPARK_APP_SOURCE="${SPARK_JAR_FILE}" \
                --build-arg SPARK_APP_DEST="${DEST_SPARK_JAR}" \
                -f "${DOCKERFILE}" .

    if [ $? -ne 0 ]; then
      echo -e "-${colred}[ERROR]${colrst}---: Build failed. Exiting ..."
      exit 1
    fi
    echo -e "-${colwht}[INFO]${colrst}----: Build completed."
    rm "${SPARK_JAR_FILE}"
}

function push() {
    local colred='\033[0;31m' # Red
    local colwht='\033[0;37m' # White
    local colrst='\033[0m'    # Text Reset

    docker push "${APP_IMAGE_NAME}":"${APP_IMAGE_TAG}"

    if [ $? -ne 0 ]; then
      echo -e "-${colred}[ERROR]${colrst}---: Push failed. Exiting ..."
      exit 1
    fi
    echo -e "-${colwht}[INFO]${colrst}----: Push completed."
}

function deploy() {
    local colred='\033[0;31m' # Red
    local colwht='\033[0;37m' # White
    local colylw='\033[0;33m' # Yellow
    local colrst='\033[0m'    # Text Reset

    kubectl create -f "${SPARK_APPLICATION}" --as "${LDAP_USER}"

    if [ $? -ne 0 ]; then
      echo -e "-${colylw}[WARNING]${colrst}-: $(basename "${SPARK_APPLICATION}") already exists."
      echo -e "-${colred}[ERROR]${colrst}---: Deploy can not be done. Exiting ..."
      exit 1
    fi
    echo -e "-${colwht}[INFO]----${colrst}: Deploy completed."
}

build
push
deploy
