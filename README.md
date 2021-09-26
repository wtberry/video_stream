# Kafka Experiment Note


## Pi & Laptop Testrun

* laptop: broker, zookeeper, consumer client.
* pi: producer client

Refer to [This stackoverflow question](https://stackoverflow.com/questions/46686690/kafka-simple-consumer-producer-setup-doesnt-work-on-different-machines-but-w) for the commands to make it work.


## Camera streaming from Pi to LocalPC
Now working on writing code to send video frames from pi to laptop.
[Tutorial - flask & kafka](https://medium.com/@kevin.michael.horan/distributed-video-streaming-with-python-and-kafka-551de69fe1dd)
- dir: kafka/video_stream

How to start: 
1. start zookeeper: ```bin/zookeeper-server-start.sh config/zookeeper.properties```
2. start kafka broker server: ```bin/kafka-server-start.sh config/server.properties```

## Camera stream from Pi to EC2
* [kafka cofluent config for ec2](https://www.confluent.io/blog/kafka-listeners-explained/)
struggling to test connect to ec2 kakfa broker. 
* Try [this](https://stackoverflow.com/questions/43565698/connecting-kafka-running-on-ec2-machine-from-my-local-machine)

### Connection Test and Setup
Tested connection between kafka broker and consumer reside in EC2 instance and producer in local PC. 

Setup is following. 

**Local PC**
* Producer Client

**EC2**
* Consumer Client
* Kafka Broeker server
* Zookeeper server: localhost

Based on [This tutorial from confluence about listener](https://www.confluent.io/blog/kafka-listeners-explained/)
2 listeners are set up for internal network and external network. 

* Internal: used for connection between broker and consumer client.(within aws vpc and ec2): port 19092
* External: used for connection between broker in EC2 instance and local PC: port 9092

1. Edit config/server.properties for LISTNERS and ADVERTISED.LISTNERS and few other attributes. 
2. start zookeeper, kafka server (broker) 
3. create and check topic on localhost:9092 (zookeeper's address)
4. start consumer on ec2, at INTERNAL LISTENER's address. 
5. start producer on Local PC specifying ec2's publicIP and EXTERNAL LISTENER's port 

### PI to ec2
Using the setup from connection test above, producer client is setup to Pi, 
and rest on EC2. 

Follow the procedures

**Pi**

1. edit video_steam/produer.py
    * topic name
    * bootstrap_server_ip (external)
    * port # (external)
2. start script (after ec2 setup is done)

**Ec2**

1. [edit config file](https://www.confluent.io/blog/kafka-listeners-explained/)
    1. config/server.propertier -> for both external and internal listners 
2. start servers
    1. zookeeper
    2. kafka
4. edit video_stream/consumer.py
    * bootstrap_server_ip: internal address
    * port # 
    * topic name
5. start the python script for consumer / Flask