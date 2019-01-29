import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score
from sklearn.externals import joblib
import csv
import mysql.connector
import sys

from stdev_with_tag import transfer
from tag import dic_generate
from tag import tag


if __name__ == '__main__':
    # filename = str(sys.argv[1])
    df = pd.read_csv('data/2019-01-28_20_51.csv', encoding='utf-8')

    # Step.1 => 貼標
    # 輸入標籤/開始/結束時間, 集合成字典
    dic1 = dic_generate('0', '2019-01-28 21:00', '2019-01-28 21:10')
    dic2 = dic_generate('1', '2019-01-28 21:14', '2019-01-28 21:24')
    dic3 = dic_generate('2', '2019-01-28 21:25', '2019-01-28 21:35')
    dic4 = dic_generate('3', '2019-01-28 21:37', '2019-01-28 21:39')

    dic_sum = {}
    for d in (dic1, dic2, dic3, dic4):
        dic_sum.update(d)

    # df.apply(), 移除沒有標籤的資料
    df['tag'] = df['time'].apply(tag, args=(dic_sum,))
    df = df[['tag', 'time', 'data_no.', 'gyro_x', 'gyro_y', 'gyro_z', 'g_x_scaled',
             'g_y_scaled', 'g_z_scaled', 'accel_x', 'accel_y', 'accel_z', 'a_x_scaled',
             'a_y_scaled', 'a_z_scaled', 'rotation_x', 'rotation_y']]
    df = df[df['tag'] != '']

    # Step.2 => 增加衍生變數: 標準差
    # 定義要算標準差的欄位
    ls = ['gyro_x', 'gyro_y', 'gyro_z', 'accel_x',
          'accel_y', 'accel_z', 'rotation_x', 'rotation_y']

    df_0 = df[df['tag'] == '0']
    df_1 = df[df['tag'] == '1']
    df_2 = df[df['tag'] == '2']
    df_3 = df[df['tag'] == '3']

    df_0_trans = transfer(df_0, ls)
    df_1_trans = transfer(df_1, ls)
    df_2_trans = transfer(df_2, ls)
    df_3_trans = transfer(df_3, ls)

    df = pd.concat([df_0_trans, df_1_trans, df_2_trans, df_3_trans], axis=0, ignore_index=True)
    df.to_csv('data/2019-01-28_20_51_trans.csv', encoding='utf-8', index=False)

    # Step.3 => 建模型
    # 移除時間與資料編號欄位
    df = df.drop(['time', 'data_no.'], axis=1)
    # 切分訓練樣本/測試樣本
    data_train, data_test, target_train, target_test = train_test_split(
        df.drop(['tag'], axis=1), df['tag'], test_size=0.3)

    clf = DecisionTreeClassifier(max_depth=4)
    clf = clf.fit(data_train, target_train)

    predict = clf.predict(data_test)
    print('預測:', predict)
    print('答案:', list(target_test))
    print('準確率:', accuracy_score(target_test, predict) * 100, '%')

    # save model
    joblib.dump(clf, 'clf.pkl')

    # 讀取整理完的檔案, 存入SQL
    usercode = '00'
    records = []

    # 讀檔案
    with open('data/2019-01-28_20_51_trans.csv', newline='', encoding='utf-8')as csvfile:
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