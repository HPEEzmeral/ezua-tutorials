# Makefile

# Define variables
REGISTRY := lr1-bd-harbor-registry.mip.storage.hpecorp.net/develop
IMG_NAME := gcr.io/mapr-252711/ezua-tutorials
GIT_HASH := $(shell git log -n1 --pretty=%h)
IMG_TAG ?= fy24-q2-$(GIT_HASH)$(IS_DIRTY)
FULL_ADDON_IMG ?= $(REGISTRY)/$(IMG_NAME)

# Build Docker image
docker-build:
	docker build . -t $(FULL_ADDON_IMG):$(IMG_TAG)

# Push Docker image to registry
docker-push:
	docker push $(FULL_ADDON_IMG):$(IMG_TAG)

