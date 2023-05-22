usage() {
  echo "$0 <commands>"
  echo "commands:"
  echo "  extract: Parse code files for translation strings"
  echo "  update : Update translation file"
  echo "  compile: Compile the translation file"
}

if [[ $# -lt 1 ]];
then
  usage
  exit
fi

case "$1" in
  "extract")
    pybabel extract -F babel.cfg --ignore-dirs="venv tests" -o locales/messages.pot .
    ;;
  "update")
    pybabel update -i locales/messages.pot -d locales
    ;;
  "compile")
    pybabel compile -d locales -l id
    ;;
  *)
    usage
    ;;
esac