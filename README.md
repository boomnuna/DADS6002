# Hadoop & Spark Assignment - DADS6002

โปรเจกต์นี้สาธิตการคำนวณ **รายได้เฉลี่ยต่อเขต (Average Income per District)**  
โดยใช้ 3 วิธี ได้แก่ Hadoop MapReduce, Spark RDD และ Spark SQL  
รันทั้งหมดผ่าน Docker บนเครื่องตัวเอง ไม่ต้องติดตั้ง Hadoop/Spark โดยตรง

---

## 📁 โครงสร้างไฟล์

```
├── mapper.py          # ตัวแยก (Map) ข้อมูล input ออกเป็น key-value
├── reducer.py         # ตัวรวม (Reduce) และคำนวณค่าเฉลี่ย
├── spark_rdd.py       # คำนวณด้วย Spark แบบ RDD
├── spark_sql.py       # คำนวณด้วย Spark แบบ SQL
├── execute.sh         # Script สำหรับรัน MapReduce ทั้งหมด
├── spark.sh           # Script สำหรับรัน Spark ทั้งหมด
├── input.txt          # ข้อมูล input (person_id, district_id, income)
├── hadoop.env         # Config ของ Hadoop
├── hue.ini            # Config ของ Hue (Web UI)
└── docker-compose.yml # กำหนด services ทั้งหมดที่จะรันใน Docker
```

---

## 📊 ข้อมูล Input

**Format:** `person_id, district_id, income`

```
10001,1,86000
10002,3,45000
10003,2,67000
...
```

---

## 🚀 วิธีรัน

> ⚠️ ต้องติดตั้ง [Docker Desktop](https://www.docker.com/products/docker-desktop/) ก่อน  

---

### ขั้นที่ 1: Clone โปรเจกต์ลงเครื่อง

```bash
git clone https://github.com/YOUR_USERNAME/hadoop-bigdata-assignment.git
cd hadoop-bigdata-assignment
```

> เพื่อดาวน์โหลดโค้ดทั้งหมดจาก GitHub มาไว้ในเครื่องเรา

---

### ขั้นที่ 2: เปิด Docker containers ทั้งหมด

```bash
docker compose up -d
```

> คำสั่งนี้จะสร้างและเปิด "เครื่องเสมือน" หลายตัวพร้อมกัน ได้แก่  
> - **namenode** = หัวใจของ Hadoop ทำหน้าที่จัดการไฟล์ใน HDFS  
> - **datanode** = ตัวเก็บข้อมูลจริง ๆ  
> - **resourcemanager** = จัดการ resource สำหรับรัน job  
> - **spark-master** = ตัวควบคุม Spark  
> - **spark-worker** = ตัวลงมือประมวลผล Spark  
> 
> `-d` = รันในพื้นหลัง (ไม่ต้องเปิด terminal ค้างไว้)  
> รอประมาณ 1-2 นาทีให้ทุกตัวพร้อม

---

### ขั้นที่ 3: รัน MapReduce Job

```bash
MSYS_NO_PATHCONV=1 ./execute.sh
```
  
> - `MSYS_NO_PATHCONV=1` = บอก Git Bash บน Windows ว่าอย่าแปลง path เช่น `/user/root` ให้เป็น `C:\user\root` โดยอัตโนมัติ  
> - `./execute.sh` = รัน script ที่ทำสิ่งเหล่านี้ตามลำดับ:
>   1. copy `mapper.py`, `reducer.py`, `input.txt` เข้าไปใน container
>   2. upload `input.txt` ขึ้น HDFS (ระบบไฟล์ของ Hadoop)
>   3. รัน Hadoop Streaming ซึ่งจะใช้ mapper → reducer ประมวลผล
>   4. เก็บผลลัพธ์ไว้ที่ `/user/root/output`

---

### ขั้นที่ 4: ดูผลลัพธ์ MapReduce

```bash
MSYS_NO_PATHCONV=1 docker exec -it namenode hdfs dfs -cat /user/root/output/part-00000
```

> - `docker exec -it namenode` = เข้าไปรันคำสั่งภายใน container ชื่อ `namenode`  
> - `hdfs dfs -cat` = อ่านไฟล์จาก HDFS (คล้าย `cat` ใน Linux)  
> - `/user/root/output/part-00000` = path ของไฟล์ผลลัพธ์ใน HDFS

---

### ขั้นที่ 5: รัน Spark Job

```bash
MSYS_NO_PATHCONV=1 ./spark.sh
```
  
> - รัน script ที่ส่ง `spark_rdd.py` และ `spark_sql.py` เข้าไปรันใน spark-master container  
> - ทั้งสองไฟล์ทำงานเดียวกับ MapReduce แต่ใช้ Spark API แทน  
> - ผลลัพธ์จะแสดงออกมาใน terminal เลย

---

## ✅ ผลลัพธ์ที่ได้

### MapReduce Output
```
1    163214.29
2    103600.00
3    59300.00
4    30571.43
5    20888.89
```

### Spark RDD Output
```
District 1: Average Income = 163214.29
District 2: Average Income = 103600.00
District 3: Average Income = 59300.00
District 4: Average Income = 30571.43
District 5: Average Income = 20888.89
```

### Spark SQL Output
```
+-----------+--------------+
|district_id|average_income|
+-----------+--------------+
|          1|     163214.29|
|          2|     103600.00|
|          3|      59300.00|
|          4|      30571.43|
|          5|      20888.89|
+-----------+--------------+
```

> ทั้ง 3 วิธีให้ผลลัพธ์เดียวกัน ✅  
> District ที่ใกล้เมืองมากกว่า มีรายได้เฉลี่ยสูงกว่าชัดเจน

---


## 🛑 ปิด Docker เมื่อใช้งานเสร็จ

```bash
docker compose down
```

> เพื่อหยุด containers ทั้งหมดและคืน RAM กลับให้เครื่อง  
> ถ้าไม่ปิด Docker จะกิน RAM ค้างไว้ตลอด

---

## 💡 Tech Stack

| เทคโนโลยี | บทบาท |
|-----------|-------|
| Docker | รัน Hadoop/Spark บนเครื่องตัวเองโดยไม่ต้องติดตั้งตรง ๆ |
| Hadoop HDFS | ระบบไฟล์แบบกระจาย (Distributed File System) |
| Hadoop MapReduce | รูปแบบการประมวลผลข้อมูลขนาดใหญ่ |
| Apache Spark | เครื่องมือประมวลผลข้อมูลที่เร็วกว่า MapReduce |
| Python 3 | ภาษาที่ใช้เขียน mapper, reducer และ Spark jobs |
