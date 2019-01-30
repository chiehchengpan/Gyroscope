from kafka import KafkaConsumer, TopicPartition
import sys
from datetime import datetime

if __name__ == "__main__":

    # 步驟0.開一個本地檔案, 寫入欄位名稱
    file_name = datetime.now().strftime('%Y-%m-%d:%H:%M') + ".csv"
    f = open(file_name, "w", encoding='utf-8')
    f.write("time,data_no.,gyro_x,gyro_y,gyro_z,g_x_scaled,g_y_scaled,g_z_scaled,"
            "accel_x,accel_y,accel_z,a_x_scaled,a_y_scaled,a_z_scaled,rotation_x,rotation_y\n")
    f.close()

    # 步驟1.設定要連線到Kafka集群的相關設定, 產生一個Kafka的Consumer的實例
    consumer = KafkaConsumer(
        bootstrap_servers=["10.120.14.124:9092"],
        api_version=(0, 10),
        group_id="my_id_006",
        # 指定msgKey的反序列化器, 若Key為None, 無法反序列化
        # key_deserializer=bytes.decode,
        # 指定msgValue的反序列化器
        value_deserializer=bytes.decode,
        # 是否從這個ConsumerGroup尚未讀取的partition / offset開始讀
        auto_offset_reset="earliest",
    )
    # 步驟2.指定想要訂閱訊息的topic名稱
    topic_name = "ccp"
    # 步驟3.讓Consumer向Kafka集群訂閱指定的topic
    consumer.subscribe(topics=topic_name)

    # 手動將offset歸零, assign開啟時需將subscribe關閉
    # consumer.assign([TopicPartition(topic_name, 0)])
    # for part in consumer.partitions_for_topic(topic_name):
    # consumer.seek(TopicPartition(topic_name, part), 0)

    # 步驟4.持續的拉取Kafka有進來的訊息
    try:
        print("Start listen incoming messages ...")
        content = ''
        num = 0
        # 持續監控是否有新的record進來 - 方法一
        for record in consumer:
            topic = record.topic
            partition = record.partition
            offset = record.offset
            timestamp = record.timestamp
            # 取出msgKey與msgValue
            msgKey = record.key
            msgValue = record.value
            # 秀出metadata與msgKey & msgValue訊息
            print('==========================================')
            print("topic=%s, partition=%s, offset=%s : (key=%s, value=%s)" % (record.topic, record.partition,
                                                                              record.offset, record.key, record.value))
            num = num + 1
            data = msgValue + '\n'
            content = content + data
            if num % 1200 == 0:
                f = open(file_name, "a", encoding='utf-8')
                f.write(content)
                f.close()
                content = ''
    except Exception:
        # 錯誤處理
        e_type, e_value, e_traceback = sys.exc_info()
        print("type ==> %s" % e_type)
        print("value ==> %s" % e_value)
        print("traceback ==> file name: %s" % e_traceback.tb_frame.f_code.co_filename)
        print("traceback ==> line no: %s" % e_traceback.tb_lineno)
        print("traceback ==> function name: %s" % e_traceback.tb_frame.f_code.co_name)
    finally:
        consumer.close()