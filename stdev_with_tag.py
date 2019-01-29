import pandas as pd
import numpy as np

'''
定義函式: 傳入list, time(幾筆算一次標準差), 傳回連續序列標準差的list
e.g. 若5筆算一次標準差, index = 0開始, 0-4/1-5/2-6/3-7...  (中繼list:target, 算出標準差放在ans)
'''


def stdev_cal(lis, time):
    # Default time=10 : 10筆資料算一次標準差, index = 0開始, 0-9/1-10/2-11/3-12...
    target = []
    ans = []
    # 前面幾筆沒 Data, 填入空格
    for n in range(time - 1):
        ans.append('')
        # 中繼 list:target, 算出標準差放在ans
    for i in range(len(lis) - (time - 1)):
        if len(target) == time:
            target = []
        for j in range(time):
            target.append(lis[j + i])
        ans.append(np.std(np.array(target)))

    return ans


'''
定義函式: 傳入df, list(裡面寫要要算標準差的欄位), 傳回增加完畢的df
'''


def transfer(df, lis):
    for column in lis:
        before = list(np.array(df[column]))
        after = stdev_cal(before, 10)
        dic = {column + '_stdev': after}
        df.index = range(len(df.index))
        df = pd.concat([df, pd.DataFrame(dic)], axis=1)

    # 把標準差為空值的資料移除
    df = df[df[lis[0] + '_stdev'] != '']

    return df


if __name__ == '__main__':
    df = pd.read_csv('tag_testing.csv', encoding='utf-8')

    # 定義要算標準差的欄位
    ls = ['gyro_x', 'gyro_y', 'gyro_z', 'accel_x', 'accel_y', 'accel_z', 'rotation_x', 'rotation_y']

    df_0 = df[df['tag'] == 0]
    df_1 = df[df['tag'] == 1]
    df_2 = df[df['tag'] == 2]
    df_3 = df[df['tag'] == 3]

    df_0_trans = transfer(df_0, ls)
    df_1_trans = transfer(df_1, ls)
    df_2_trans = transfer(df_2, ls)
    df_3_trans = transfer(df_3, ls)

    df_total = pd.concat([df_0_trans, df_1_trans, df_2_trans, df_3_trans], axis=0, ignore_index=True)
    df_total.to_csv('stdev_complete.csv', encoding='utf-8', index=False)