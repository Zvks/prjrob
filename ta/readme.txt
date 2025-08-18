docker build -t ta .
docker login -u dockeruser -p 19042006 http://192.168.1.198:8123/repository/segrouprepo/ 
docker tag ta 192.168.1.198:8123/repository/segrouprepo/ta:1.0.0-20251608 
docker push 192.168.1.198:8123/repository/segrouprepo/ta:1.0.0-20251608

docker search 192.168.1.198:8123/repository/segrouprepo/ta
docker pull 192.168.1.198:8123/repository/segrouprepo/ta:1.0.0-20251608
docker run 192.168.1.198:8123/repository/segrouprepo/ta:1.0.0-20251608