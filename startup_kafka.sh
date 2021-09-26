# kafka related setup, such as creating topic
IP=$1
topic=$2

#start zookeeper
/home/wataru/Projects/kafka/bin/zookeeper-server-start.sh config/zookeeper.properties

# start kafka server
/home/wataru/Projects/kafka/bin/kafka-server-start.sh config/server.properties

# create topic
/home/wataru/Projects/kafka/bin/kafka-topics.sh \
    --create --zookeeper $IP:2181 --replication-factor 1  --partitions 1 --topic $topic

# test topic
/home/wataru/Projects/kafka/bin/kafka-topics.sh --list --zookeeper $IP:2181

# start consumer
#/home/wataru/Projects/kafka/bin/kafka-console-consumer.sh --bootstrap-server $IP:9092 --topic $topic

