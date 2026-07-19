.PHONY: build run stop logs index tag push pull-run

REGISTRY   ?= <region>.ocir.io
NAMESPACE  ?= <tenancy-namespace>
IMAGE_NAME ?= mini-rag
IMAGE_TAG  ?= latest
FULL_IMAGE  = $(REGISTRY)/$(NAMESPACE)/$(IMAGE_NAME):$(IMAGE_TAG)

DOCKER  := $(shell command -v podman 2>/dev/null || command -v docker 2>/dev/null)
COMPOSE := $(DOCKER) compose

build:
	$(COMPOSE) -f compose.yml build

run:
	$(COMPOSE) -f compose.yml up -d

stop:
	$(COMPOSE) -f compose.yml down

logs:
	$(COMPOSE) -f compose.yml logs -f mini-rag

index:
	$(COMPOSE) -f compose.yml run --rm build-index

tag:
	$(DOCKER) tag mini-rag:latest $(FULL_IMAGE)

push: tag
	$(DOCKER) push $(FULL_IMAGE)

pull-run:
	$(DOCKER) pull $(FULL_IMAGE)
	$(DOCKER) run -d --name mini-rag -p 8501:8501 --env-file .env --restart unless-stopped $(FULL_IMAGE)