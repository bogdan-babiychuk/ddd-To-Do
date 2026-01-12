.PHONY: run

run:
	cd ToDo && poetry run uvicorn main:create_app --factory --reload
