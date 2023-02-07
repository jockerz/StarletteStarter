uvicorn main:application --reload --reload-dir apps \
  --host 0.0.0.0 --port 8002 \
  --log-level debug
