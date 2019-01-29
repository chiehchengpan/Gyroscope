import pandas as pd

'''
定義函式: input ->標籤/開始時間/結束時間  output ->字典

    dic = {'0':['2019-01-10 21:00','2019-01-10 21:01','2019-01-10 21:02','2019-01-10 21:03'],
           '1':['2019-01-10 21:15','2019-01-10 21:16','2019-01-10 21:17','2019-01-10 21:18']}
'''


def dic_generate(state, start_time, end_time):
    # 傳回字典 : key=state & value=list
    dic = {}
    dic[state] = []
    basic_string = start_time.split(' ')[0]

    # 產生開始與結束時間區間內的字串: list.append
    s1 = int(start_time.split(' ')[-1].split(':')[-1])
    s2 = int(end_time.split(' ')[-1].split(':')[-1])
    s3 = (s2 - s1) % 60
    for i in range(s3 + 1):
        num = int(s1) + i
        s4 = start_time.split(' ')[-1].split(':')[0]
        if num >= 60:
            num = num % 60
            s4 = str(int(start_time.split(' ')[-1].split(':')[0]) + 1)
        num_str = str(num)
        if num < 10:
            num_str = '0' + str(num)
        total = basic_string + ' ' + s4 + ":" + num_str
        dic[state].append(total)

    return dic


'''
定義函式: 抓出字典中的每個時間字串, 比對dataframe中欄位, 貼標tag
    for df.apply()
'''


def tag(s, dic):
    index = ""
    for key in dic:
        for item in dic[key]:
            if item in s:
                index = key
                break
    return index


if __name__ == '__main__':
    df = pd.read_csv('basic_test_csv_data.csv', encoding='utf-8')

    # 輸入標籤/開始/結束時間, 集合成字典
    dic1 = dic_generate('0', '2019-01-10 21:00', '2019-01-10 21:09')
    dic2 = dic_generate('1', '2019-01-10 21:15', '2019-01-10 21:29')
    dic3 = dic_generate('2', '2019-01-10 21:33', '2019-01-10 21:47')
    dic4 = dic_generate('3', '2019-01-10 21:53', '2019-01-10 21:57')

    dic_sum = {}
    for d in (dic1, dic2, dic3, dic4):
        dic_sum.update(d)

    # df.apply(), 移除沒有tag的資料
    df['tag'] = df['time'].apply(tag, args=(dic_sum,))
    df = df[['tag', 'time', 'data_no.', 'gyro_x', 'gyro_y', 'gyro_z', 'g_x_scaled',
             'g_y_scaled', 'g_z_scaled', 'accel_x', 'accel_y', 'accel_z', 'a_x_scaled',
             'a_y_scaled', 'a_z_scaled', 'rotation_x', 'rotation_y']]
    df1 = df[df['tag'] != '']

    df1.to_csv('tag_testing.csv', encoding='utf-8', index=False)