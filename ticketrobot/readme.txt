docker build -t ticketrobot .
docker login -u dockeruser -p 19042006 http://192.168.1.198:8123/repository/segrouprepo/ 
docker tag ticketrobot 192.168.1.198:8123/repository/segrouprepo/ticketrobot:1.0.0-20251808 
docker push 192.168.1.198:8123/repository/segrouprepo/ticketrobot:1.0.0-20251808

docker search 192.168.1.198:8123/repository/segrouprepo/ticketrobot
docker pull 192.168.1.198:8123/repository/segrouprepo/ticketrobot:1.0.0-20251608
docker run 192.168.1.198:8123/repository/segrouprepo/ticketrobot:1.0.0-20251608