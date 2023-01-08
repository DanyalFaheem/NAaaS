## Deployment of Spark Cluster
To Deploy the spark cluster you need to first create the image from the Dockerfile.
This image can be created by using the following command in docker
```
docker build -t my-spark-image .
```
After building the image you just need to deploy the ```docker-compose.yml``` using the following command
```
docker-compose up -d
```
This docker-compose.yml file will deploy a standalone spark cluster with 2 worker nodes.
You can also access the Web UI by going to the ```localhost:9090``` 

To stop the cluster, you just have to write the following command
```
docker-compose down
```