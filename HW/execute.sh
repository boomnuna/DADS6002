docker cp mapper.py namenode:/mapper.py
docker cp reducer.py namenode:/reducer.py
docker cp input.txt namenode:/input.txt

# inside docker
# docker exec -it namenode /bin/bash
docker exec -it namenode bash -c "chmod +x /mapper.py /reducer.py"
docker exec -it namenode bash -c "mkdir job_files"
docker exec -it namenode bash -c "mv /mapper.py /reducer.py /job_files/"
docker exec -it namenode bash -c "hdfs dfs -mkdir -p /user/root/input"
docker exec -it namenode bash -c "hdfs dfs -put -f /input.txt /user/root/input/"
docker exec -it namenode bash -c "if hdfs dfs -test -e /user/root/output; then hdfs dfs -rm -r -skipTrash /user/root/output; fi"
docker exec -it namenode bash -c "cd /job_files && hadoop jar /opt/hadoop-3.2.1/share/hadoop/tools/lib/hadoop-streaming-3.2.1.jar \
-file mapper.py -mapper mapper.py \
-file reducer.py -reducer reducer.py \
-input /user/root/input/input.txt \
-output /user/root/output"
