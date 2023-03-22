BASE_PATH="$(dirname ${BASH_SOURCE[0]})/.."

# Log files
if [[ ! -d ./files/logs ]]; then mkdir ./files/logs; fi
# PID files
if [[ ! -d ./files/pids ]]; then mkdir ./files/pids; fi

PID_FILE="./files/pids/web_app.pid"
PORT=8006

if [ -f ${PID_FILE} ];
then
  PID_NUM=`cat ${PID_FILE}`
  CHECK_WORKER=$(ps -p $PID_NUM -o comm=)
  if [[ ${CHECK_WORKER} && ${CHECK_WORKER} -eq "gunicorn" ]];
  then
    echo "The service has already been running: ${PID_NUM}"
    echo "Exiting: $(date)"
    exit
  fi
fi

venv/bin/gunicorn main:application -k uvicorn.workers.UvicornWorker \
  --workers=4 --reload \
  --pid ${PID_FILE} \
  --bind 127.0.0.1:${PORT} \
  --capture-output \
  --log-config configs/logging_gunicorn.conf
