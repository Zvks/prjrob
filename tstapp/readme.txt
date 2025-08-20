docker build -t tst .
docker login -u admin -p 18031978 http://192.168.1.198:8123/repository/segrouprepo/ 
docker tag tst 192.168.1.198:8123/repository/segrouprepo/tst:1.0.2-20251808 
docker push 192.168.1.198:8123/repository/segrouprepo/tst:1.0.2-20251808

docker search 192.168.1.198:8123/repository/segrouprepo/tst
docker pull 192.168.1.198:8123/repository/segrouprepo/tst:1.0.0-20251608
docker run 192.168.1.198:8123/repository/segrouprepo/tst:1.0.0-20251608