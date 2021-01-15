ENV_ACTIVATE=$(grep ENV_ACTIVATE .env | cut -d '=' -f2)
source $ENV_ACTIVATE && python  -m pytest --cov=accounts --ignore=data company --cache-clear

#source $ENV_ACTIVATE && python -m pytest --cov=namesgames --ignore=data company --cache-clear
