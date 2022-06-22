import typing
from kafka import KafkaProducer, KafkaConsumer, TopicPartition
from setup_logger import producer_log
import json
from MessageData import MessageData
import datetime

# TODO might be a class with only static methods so that the host is always the same

def _last_message_topic(which_topic: TopicPartition) -> typing.Tuple[str, int]:
    """
    TODO
    """
    producer_log.debug("Initialising Kafka consumer")
    consumer = KafkaConsumer(
        bootstrap_servers='localhost:9092',
        auto_offset_reset='latest'#,
        #group_id = "piro"
    )
    consumer.assign([which_topic])

    last_offset = consumer.position(which_topic)
    last_mex = None

    if last_offset > 1:
        last_mex = _get_last_message(consumer, which_topic, last_offset)
    
    consumer.close()
    return last_mex, last_offset

def _get_last_message(k_consumer: KafkaConsumer, which_topic: TopicPartition, last_offset: int) -> str:
    """
    TODO 

    Args:

    Returns:
    """
    # obtain last message
    k_consumer.seek( which_topic, last_offset - 1 ) 

    last_mex = None
    for message in k_consumer:
        last_mex = dict(json.loads(message.value)) #Trend.from_repr(dict(json.loads(message.value)))

        if message.offset == last_offset - 1:
            #exit the loop after obtaining the message
            break

    producer_log.debug(f"last message in topic: {last_mex}")

    return last_mex

def _write_list_in_queue(topic: str, obj_list: list) -> None:
    """
    TODO

    Args:
        obj_list: a list sorted from the most recent element to the oldest.
    """
    producer_log.debug("Initialising Kafka producer")
    producer = KafkaProducer(
        bootstrap_servers = ['localhost:9092'],
        value_serializer = lambda x: json.dumps(x, indent=2).encode('utf-8')
    )

    try:
        for element in reversed(obj_list):
            kafka_ts = int((element.datetime - datetime.datetime(1970, 1, 1)).total_seconds() * 1000)
            producer_log.debug(f"sending in \"{topic}\" ts {kafka_ts} message: {element.to_repr()}")
            producer.send(topic, element.to_repr(), timestamp_ms = kafka_ts ) 
    
    except AttributeError:
        producer_log.warning("The list of elements fed to the producer has no \"datetime\" attribute, writing no timestamp")
        for element in reversed(obj_list):
            producer_log.debug(f"sending in \"{topic}\" message: {element.to_repr()}")
            producer.send(topic, element.to_repr() )

    producer_log.info(f"Flushing and closing producer")
    producer.flush()
    producer.close()

def _filter_duplicates(message: str, objType: MessageData, from_list: list, skip_latest: bool = True ) -> list:
    """
    TODO
    """
    last_queued_message = objType.from_repr(message)
    found_idx = None
    from_idx = None

    if skip_latest:
        from_idx = 1
    else:
        from_idx = 0


    for idx, elem in enumerate(from_list):
        if elem == last_queued_message:
            producer_log.info(f"last message found in API call at index {idx}: {elem.to_repr()}")
            found_idx = idx
            break

    if found_idx is not None:
        producer_log.info(f"writing the rest of missing messages")
        missing_elem = from_list[from_idx:found_idx] # skip most recent as it is still updating
    else:
        producer_log.info(f"No fetched message equals the last in the queue, writing all the elements")
        missing_elem = from_list[from_idx:] # skip most recent as it is still updating

    return missing_elem

def write_unique(topic: str, read_partition = int, list_elem = typing.Type[list], list_elem_type = MessageData, skip_latest = True ) -> None:
    """ Writes messages in a Kafka topic, avoiding duplicates by looking at the last message in the queue.

    Args:
        topic: in which queue the new messages will be appended.
        read_partition: from which partition the consumer will detect the last message. TODO can be omitted if raising the ACK?
        list_elem: a list of elements that goes from the latest to the oldest.
        list_elem_type: of which instance are the Objects in 'list_elem'.
        skip_latest: should the first message in 'list_elem' be skipped? Default True
    """
    which_topic = TopicPartition(topic = topic, partition = read_partition)

    message, offset = _last_message_topic(which_topic)

    list_elem = list_elem

    if offset > 1:
        # Go back in market trends until it is found the trend equal the one in the queue

        missing_messages = _filter_duplicates(message, list_elem_type, list_elem, skip_latest = skip_latest)

                
    else: # no message in the topic's partition
        producer_log.info("No offset present, proceeding writing all the data")
        missing_messages = list_elem[1:] # skip most recent as it is still updating
        
    _write_list_in_queue(topic, missing_messages)