.PHONY: todo url

todo:
	cd ToDo && poetry run uvicorn main:create_app --factory --reload --port 8000

url:
	cd UrlShortner && poetry run uvicorn main:create_app --factory --reload --port 8001
