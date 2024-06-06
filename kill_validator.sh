if [ -z "$1" ]; then
    docker stop $(docker ps -q -f ancestor=nnc_validator)
else
    docker stop $1
fi