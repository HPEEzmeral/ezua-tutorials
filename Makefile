TOPDIR	  := $(shell git rev-parse --show-toplevel)
BASE_VER  ?= v1.2.0
BUILD_ID  ?= $(shell git describe --always --dirty)
VERSION	  := $(BASE_VER)-$(BUILD_ID)


export REPO    := ezkf
REGISTRY       ?= lr1-bd-harbor-registry.mip.storage.hpecorp.net/develop
EZKF_REGISTRY  ?= $(REGISTRY)/$(REPO)

docker-build:
	@echo "Building the images for the Question-Answering demo..."
	$(foreach target, app llm transformer vectorstore, \
		docker build \
			-t $(EZKF_REGISTRY)/qna-$(target):$(VERSION) \
			-f $(TOPDIR)/demos/question-answering/dockerfiles/$(target)/Dockerfile \
			$(TOPDIR)/demos/question-answering/dockerfiles/$(target); \
	)

	@echo "Building the images for the Fraud Detection demo..."
	docker build \
		-t $(EZKF_REGISTRY)/fraud-detection-app:$(VERSION) \
		-f $(TOPDIR)/demos/fraud-detection/dockerfiles/app/Dockerfile \
		$(TOPDIR)/demos/fraud-detection/dockerfiles/app

docker-push:
	@echo "Pushing the images for the Question-Answering demo..."
	$(foreach target, app llm transformer vectorstore, \
		docker push $(EZKF_REGISTRY)/qna-$(target):$(VERSION); \
	)

	@echo "Pushing the images for the Fraud Detection demo..."
	docker push $(EZKF_REGISTRY)/fraud-detection-app:$(VERSION)

################################################################################
# Pipeline API                                                                 #
################################################################################

version:
	@echo $(VERSION)

deliverables:
	@echo

dependencies:
	@echo

test:
	@echo

.PHONY: images
images:
	@echo $(EZKF_REGISTRY)/qna-app:$(VERSION)
	@echo $(EZKF_REGISTRY)/qna-llm:$(VERSION)
	@echo $(EZKF_REGISTRY)/qna-transformer:$(VERSION)
	@echo $(EZKF_REGISTRY)/qna-vectorstore:$(VERSION)
	@echo $(EZKF_REGISTRY)/fraud-detection-app:$(VERSION)

release: docker-build docker-push
