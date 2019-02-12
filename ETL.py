import pandas as pd

from stdev_with_tag import transfer
from tag import dic_generate
from tag import tag

# ETL.py --> 把ETL後的檔案寫進資料庫

if __name__ == '__main__':
    # filename = str(sys.argv[1])
    filename = 'data/2019-02-11_20_58.csv'
    transfilename = filename.split('.')[0] + '_trans.csv'
    df = pd.read_csv(filename, encoding='utf-8')

    # Step.1 => 貼標
    # 輸入標籤/開始/結束時間, 集合成字典
    dic1 = dic_generate('0', '2019-02-11 21:10', '2019-02-11 21:19')
    dic2 = dic_generate('1', '2019-02-11 21:23', '2019-02-11 21:32')
    dic3 = dic_generate('2', '2019-02-11 21:33', '2019-02-11 21:42')
    dic4 = dic_generate('3', '2019-02-11 21:45', '2019-02-11 21:47')

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
    df.to_csv(transfilename, encoding='utf-8', index=False)

    # Step.3 新data需要concat到原本全部的data
    f1name = 'data/Total_training_data_0130.csv'
    f2name = transfilename

    df = pd.read_csv(f1name, encoding='utf-8')
    df1 = pd.read_csv(f2name, encoding='utf-8')

    df = pd.concat([df, df1], axis=0, ignore_index=True)

    df.to_csv('data/Total_training_data_0211.csv', encoding='utf-8', index=False)