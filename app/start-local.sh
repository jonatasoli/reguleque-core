!#/bin/sh

uvicorn main:create_app --factory --host 0.0.0.0 --port 7777 --reload
