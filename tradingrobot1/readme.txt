docker build -t rmqsetup .
docker login -u dockeruser -p 19042006 http://192.168.1.198:8123/repository/segrouprepo/ 
docker tag rmqsetup 192.168.1.198:8123/repository/segrouprepo/tradingrobot1:1.0.0-20251608 
docker push 192.168.1.198:8123/repository/segrouprepo/tradingrobot1:1.0.0-20251608

docker search 192.168.1.198:8123/repository/segrouprepo/tradingrobot1
docker pull 192.168.1.198:8123/repository/segrouprepo/tradingrobot1:1.0.0-20251608
docker run 192.168.1.198:8123/repository/segrouprepo/tradingrobot1:1.0.0-20251608