# Makefile

# Define variables
IMG_NAME := gcr.io/mapr-252711/ezua-tutorials
GIT_HASH := $(shell git log -n1 --pretty=%h)
IMG_TAG ?= ezua-1.4.0-$(GIT_HASH)

# Build Docker image
docker-build:
	docker build --platform linux/amd64 -t $(IMG_NAME):$(IMG_TAG) .

# Push Docker image to registry
docker-push:
	docker push $(IMG_NAME):$(IMG_TAG)

