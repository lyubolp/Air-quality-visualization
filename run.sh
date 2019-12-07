if [[ "$VIRTUAL_ENV" == "" ]]
then
  source ./venv/bin/activate
fi
cur_dir=$(pwd);
export PYTHONPATH="${PYTHONPATH}:$cur_dir/src"
python3 src/main.py
