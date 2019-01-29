import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score


# 建模型
if __name__ == '__main__':
    df = pd.read_csv('stdev_complete.csv', encoding='utf-8')

    # 移除時間與資料編號欄位
    df = df.drop(['time', 'data_no.'], axis=1)
    # 切分訓練樣本/測試樣本
    data_train, data_test, target_train, target_test = train_test_split(
                                    df.drop(['tag'], axis=1), df['tag'], test_size=0.3)
    print(df.drop(['tag'], axis=1))
    clf = DecisionTreeClassifier(max_depth=4)
    clf = clf.fit(data_train, target_train)

    predict = clf.predict(data_test)
    print('預測:', predict)
    print('答案:', list(target_test))
    print('準確率:', accuracy_score(target_test, predict) * 100, '%')
