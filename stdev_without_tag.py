import pandas as pd
import stdev_with_tag as std


if __name__ == '__main__':
    df = pd.read_csv('basic_test_csv_data.csv', encoding='utf-8')

    # 定義要算標準差的欄位
    ls = ['gyro_x', 'gyro_y', 'gyro_z', 'accel_x', 'accel_y', 'accel_z', 'rotation_x', 'rotation_y']

    df_trans = std.transfer(df, ls)
    df_trans.to_csv('stdev_without_tag.csv', encoding='utf-8', index=False)