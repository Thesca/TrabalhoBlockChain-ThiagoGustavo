# docker build ./selector -t nnc_selector
# docker build ./validator -t nnc_validator
# docker build ./manager -t nnc_db
# docker network rm nnc_network
# docker network create --subnet=192.168.1.0/24 nnc_network
docker compose build