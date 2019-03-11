import pandas as pd

from sklearn.neighbors import KNeighborsClassifier
from sklearn.externals import joblib
# Modeling.py --> 建模型

if __name__ == '__main__':
    '''
    input_filename = 'data/Total_training_data_0211.csv'
    output_filename = 'data/even_for_modeling.csv'
    df = pd.read_csv(input_filename, encoding='utf-8')

    # 狀態0/1/2數量比3多 --> 要隨機抽樣選出跟3一樣數量的data來建模
    df_0 = df[df['tag'] == 0]
    df_1 = df[df['tag'] == 1]
    df_2 = df[df['tag'] == 2]
    df_3 = df[df['tag'] == 3]

    num = len(df_3)

    df = pd.concat([df_0.sample(n=num), df_1.sample(n=num),
                    df_2.sample(n=num), df_3.sample(frac=1).reset_index(drop=True)],
                   axis=0, ignore_index=True)
    df.to_csv(output_filename, encoding='utf-8', index=False)
    '''

    output_filename = 'data/even_for_modeling_0217_exclude_outlier.csv'
    df = pd.read_csv(output_filename, encoding='utf-8')

    # 移除不用的欄位
    '''
    df = df.drop(['time', 'data_no.', 'g_x_scaled', 'g_y_scaled', 'g_z_scaled',
                  'a_x_scaled', 'a_y_scaled', 'a_z_scaled'], axis=1)
    '''
    df = df.drop(['time', 'data_no.', 'g_x_scaled', 'g_y_scaled', 'g_z_scaled',
                  'a_x_scaled', 'a_y_scaled', 'a_z_scaled', 'gyro_x_stdev',
                  'gyro_y_stdev', 'gyro_z_stdev', 'accel_x_stdev', 'accel_y_stdev',
                  'accel_z_stdev', 'rotation_x_stdev', 'rotation_y_stdev'], axis=1)



    # modeling_compare 決定哪一個演算法最好, 用那個演算法模型對所有樣本作訓練
    # 目前最好的:KNN, n_neighbors=3
    X = df.drop(['tag'], axis=1)
    y = df['tag']

    knn = KNeighborsClassifier(n_neighbors=3)
    knn = knn.fit(X, y)

    # save model
    joblib.dump(knn, 'KNN_8.pkl')
