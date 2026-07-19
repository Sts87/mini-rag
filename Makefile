.PHONY: build run stop logs index tag push pull run

REGISTRY   ?= <region>.ocir.io
NAMESPACE  ?= <tenancy-namespace>
IMAGE_NAME ?= mini-rag
IMAGE_TAG  ?= latest
FULL_IMAGE  = $(REGISTRY)/$(NAMESPACE)/$(IMAGE_NAME):$(IMAGE_TAG)

build:
	docker compose -f compose.yml build

run:
	docker compose -f compose.yml up -d

stop:
	docker compose -f compose.yml down

logs:
	docker compose -f compose.yml logs -f mini-rag

index:
	docker compose -f compose.yml run --rm build-index

tag:
	docker tag mini-rag:latest $(FULL_IMAGE)

push: tag
	docker push $(FULL_IMAGE)

pull-run:
	docker pull $(FULL_IMAGE)
	docker run -d --name mini-rag -p 8501:8501 --env-file .env --restart unless-stopped $(FULL_IMAGE)