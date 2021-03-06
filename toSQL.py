import mysql.connector
import csv

# toSQL.py --> 把ETL後的檔案寫進資料庫

if __name__ == "__main__":
    usercode = '00'
    records = []
    filename = 'data/2019-01-28_20_51_trans.csv'

    # 讀檔案
    with open(filename, newline='', encoding='utf-8')as csvfile:
        rows = csv.reader(csvfile)

        for row in list(rows)[1:]:
            row.insert(0, usercode)
            records.append(row)

    # 連線
    db = mysql.connector.connect(
        user='root',
        password='1234567890',
        host='localhost',
        database='project',
    )
    cursor = db.cursor()
    sql = 'INSERT INTO gyro VALUES' \
          '(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'
    cursor.executemany(sql, records)
    db.commit()
    db.close()