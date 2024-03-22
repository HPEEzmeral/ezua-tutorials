#!/bin/bash

APP_IMAGE_NAME=${APP_IMAGE_NAME:-"gcr.io/mapr-252711/ezua-tutorials"}
GIT_HASH=$(git log -n1 --pretty=%h)
APP_IMAGE_TAG="ezua-1.4-$GIT_HASH"

function build() {
  echo "Building the ${APP_IMAGE_NAME}:${APP_IMAGE_TAG} image"
  docker build --platform linux/amd64 -t "${APP_IMAGE_NAME}":"${APP_IMAGE_TAG}" .

  if [ $? -ne 0 ]; then
    echo "[ERROR]---: Build failed. Exiting ..."
    exit 1
  fi
  echo "[INFO]----: Build completed."
}

function push() {
  docker push "${APP_IMAGE_NAME}":"${APP_IMAGE_TAG}"

  if [ $? -ne 0 ]; then
    echo "[ERROR]---: Push failed. Exiting ..."
    exit 1
  fi
  echo "[INFO]----: Push completed."
}

build
push
