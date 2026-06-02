# Hadoop & Spark Assignment - DADS6002

## Overview
MapReduce and Spark jobs to calculate **average income per district**

## Input Data Format
```
person_id, district_id, personal_income
10021, 1, 120000
```

## Results

### MapReduce Output
```
1    550000.00
2    220000.00
3    150000.00
```

### Spark RDD Output
```
District 1: Average Income = 550000.00
District 2: Average Income = 220000.00
District 3: Average Income = 150000.00
```

### Spark SQL Output
```
+-----------+--------------+
|district_id|average_income|
+-----------+--------------+
|          1|      550000.0|
|          2|      220000.0|
|          3|      150000.0|
+-----------+--------------+
```

## How to Run

### 1. Start Docker
```bash
docker compose up -d
```

### 2. Run MapReduce
```bash
MSYS_NO_PATHCONV=1 ./execute.sh
```

### 3. View MapReduce Output
```bash
MSYS_NO_PATHCONV=1 docker exec -it namenode hdfs dfs -cat /user/root/output/part-00000
```

### 4. Run Spark
```bash
MSYS_NO_PATHCONV=1 ./spark.sh
```

## Project Structure
```
├── mapper.py         # MapReduce Mapper
├── reducer.py        # MapReduce Reducer
├── spark_rdd.py      # Spark RDD
├── spark_sql.py      # Spark SQL
├── execute.sh        # Run MapReduce
├── spark.sh          # Run Spark
├── input.txt         # Input data
└── docker-compose.yml
```
