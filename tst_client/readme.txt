docker build -t tst_client .
docker login -u admin -p 18031978 http://192.168.1.198:8123/repository/segrouprepo/ 
docker tag tst_client 192.168.1.198:8123/repository/segrouprepo/tst_client:1.0.2-20251808 
docker push 192.168.1.198:8123/repository/segrouprepo/tst_client:1.0.2-20251808

docker search 192.168.1.198:8123/repository/segrouprepo/tst_client
docker pull 192.168.1.198:8123/repository/segrouprepo/tst_client:1.0.0-20251608
docker run 192.168.1.198:8123/repository/segrouprepo/tst_client:1.0.0-20251608