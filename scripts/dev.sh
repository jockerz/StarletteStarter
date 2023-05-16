if [[ $# -ge 1 ]]
then
  port=$1
else
  port=8001
fi

uvicorn main:application \
  --host 127.0.0.1 --port $port \
  --reload --reload-dir apps \
  --log-level debug
