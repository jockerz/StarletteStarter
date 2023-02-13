uvicorn main:application --reload --reload-dir apps \
  --host 0.0.0.0 --port 8001 \
  --log-level debug
