import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score
from xgboost import XGBClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.externals import joblib
from sklearn.model_selection import KFold

# Modeling.py --> 建模型

if __name__ == '__main__':
    input_filename = 'data/Total_training_data_0211.csv'
    output_filename = 'data/even_for_modeling.csv'
    df = pd.read_csv(input_filename, encoding='utf-8')

    # 狀態0/1/2數量比3多 --> 要隨機抽樣選出跟3一樣數量的data來建模
    df_0 = df[df['tag'] == 0]
    df_1 = df[df['tag'] == 1]
    df_2 = df[df['tag'] == 2]
    df_3 = df[df['tag'] == 3]

    num = len(df_3)

    df = pd.concat([df_0.sample(n=num), df_1.sample(n=num), df_2.sample(n=num), df_3],
                   axis=0, ignore_index=True)
    df.to_csv(output_filename, encoding='utf-8', index=False)
    # 移除不用的欄位

    df = df.drop(['time', 'data_no.', 'g_x_scaled', 'g_y_scaled', 'g_z_scaled',
                  'a_x_scaled', 'a_y_scaled', 'a_z_scaled'], axis=1)
    '''
    df = df.drop(['time', 'data_no.', 'g_x_scaled', 'g_y_scaled', 'g_z_scaled',
                  'a_x_scaled', 'a_y_scaled', 'a_z_scaled', 'gyro_x_stdev',
                  'gyro_y_stdev', 'gyro_z_stdev', 'accel_x_stdev', 'accel_y_stdev',
                  'accel_z_stdev', 'rotation_x_stdev', 'rotation_y_stdev'], axis=1)
    '''
    # 切分訓練樣本/測試樣本
    data_train, data_test, target_train, target_test = train_test_split(
                                    df.drop(['tag'], axis=1), df['tag'], test_size=0.3)
    print(df.drop(['tag'], axis=1))
    df.drop(['tag'], axis=1).to_csv('data/model_example.csv', encoding='utf-8', index=False)
    '''
    # 決策樹
    clf = DecisionTreeClassifier(max_depth=4)
    clf = clf.fit(data_train, target_train)

    predict_train = clf.predict(data_train)
    predict_test = clf.predict(data_test)
    print('預測:', predict_test)
    print('答案:', list(target_test))
    print('決策樹訓練樣本準確率:', accuracy_score(target_train, predict_train) * 100, '%')
    print('決策樹驗證樣本準確率:', accuracy_score(target_test, predict_test) * 100, '%')

    # XGBoost
    xgb = XGBClassifier()
    xgb = xgb.fit(data_train, target_train)

    pred_xg_train = xgb.predict(data_train)
    pred_xg_test = xgb.predict(data_test)
    print('預測:', pred_xg_test)
    print('答案:', list(target_test))
    print('XGBoost訓練樣本準確率:', accuracy_score(target_train, pred_xg_train) * 100, '%')
    print('XGBoost驗證樣本準確率:', accuracy_score(target_test, pred_xg_test) * 100, '%')
    '''
    # KNN
    knn = KNeighborsClassifier(n_neighbors=5)
    knn = knn.fit(data_train, target_train)

    pred_kn_train = knn.predict(data_train)
    pred_kn_test = knn.predict(data_test)
    print('預測:', pred_kn_test)
    print('答案:', list(target_test))
    print('KNN訓練樣本準確率:', accuracy_score(target_train, pred_kn_train) * 100, '%')
    print('KNN驗證樣本準確率:', accuracy_score(target_test, pred_kn_test) * 100, '%')

    # save model
    # joblib.dump(clf, 'ClassificationTree.pkl')
    # joblib.dump(xgb, 'XGBoost.pkl')
    joblib.dump(knn, 'KNN.pkl')