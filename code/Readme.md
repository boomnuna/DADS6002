# Run Hadoop in docker

### Install docker & docker compose
macos: https://docs.docker.com/desktop/setup/install/mac-install/

windows: https://docs.docker.com/desktop/setup/install/windows-install/

### Run Hadoop on docker compose

start container
```
docker compose up -d
```

# Project Structure

```text
.
├── Readme.md
├── docker-compose.yml
├── execute.sh # HDFS execution shell script
├── hadoop.env
├── hue.ini
├── input.txt
├── mapper.py # HDFS mapper
├── reducer.py # HDFS reducer
├── spark.sh # Spark execution shell script
├── spark_rdd.py # Spark RDD
└── spark_sql.py # Spark SQL
```

# MapReduce

modify file `./mapper.py` and `./reducer.py`

modify file `./input.txt` for test data

# Create output file via HDFS

run `execute.sh`
```
./execute.sh
```
> Note: if no permission to execute try `chmod +x ./execute.sh`

output file will be store in `/user/root/output`

checking result of output file using this command
```
docker exec -it namenode hdfs dfs -cat /user/root/output/part-00000
```

# Apache Spark

The project also includes Apache Spark for data processing, using RDD and Spark SQL APIs.

modify `spark_rdd.py` and `spark_sql.py`

run `spark.sh` to submit Spark jobs to the `spark-master` container
```
./spark.sh
```
> Note: if no permission to execute try `chmod +x ./spark.sh`
