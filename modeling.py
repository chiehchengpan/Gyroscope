import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score
from sklearn.externals import joblib

# Modeling.py --> 建模型

if __name__ == '__main__':
    filename = 'data/Total_training_data_0211.csv'

    df = pd.read_csv(filename, encoding='utf-8')

    # 移除不用的欄位
    df = df.drop(['time', 'data_no.', 'g_x_scaled', 'g_y_scaled', 'g_z_scaled',
                  'a_x_scaled', 'a_y_scaled', 'a_z_scaled'], axis=1)
    # 切分訓練樣本/測試樣本
    data_train, data_test, target_train, target_test = train_test_split(
                                    df.drop(['tag'], axis=1), df['tag'], test_size=0.3)
    print(df.drop(['tag'], axis=1))
    clf = DecisionTreeClassifier(max_depth=4)
    clf = clf.fit(data_train, target_train)

    predict_train = clf.predict(data_train)
    predict_test = clf.predict(data_test)
    print('預測:', predict_test)
    print('答案:', list(target_test))
    print('訓練樣本準確率:', accuracy_score(target_train, predict_train) * 100, '%')
    print('驗證樣本準確率:', accuracy_score(target_test, predict_test) * 100, '%')

    # save model
    joblib.dump(clf, 'clf.pkl')