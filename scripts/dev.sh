if [[ $# -ge 1 ]]
then
  echo "$1"
  port=$1
else
  port=8001
fi

uvicorn main:application \
  --host 0.0.0.0 --port $port \
  --reload --reload-dir apps \
  --log-level debug
