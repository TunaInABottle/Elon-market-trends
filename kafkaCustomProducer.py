from typing import Type, Tuple, List
from kafka import KafkaProducer, KafkaConsumer, TopicPartition
from config.setup_logger import producer_log
import json
from MessageData import MessageData
import datetime

# TODO might be a class with only static methods so that the host is always the same

def last_message_in_topic(which_topic: TopicPartition) -> Tuple[str, int]:
    """Get the last message of a TopicPartition.

    Args:
        which_topic: from where the last message is searched.

    Returns:
        An integer with the last message offset in the topic and the corresponding message if any, None otherwise.
    """
    producer_log.debug("Initialising Kafka consumer in order to find the last message")
    consumer = KafkaConsumer(
        bootstrap_servers='localhost:9092',
        auto_offset_reset='latest'#,
        #group_id = "piro"
    )
    consumer.assign([which_topic])

    last_offset = consumer.position(which_topic)
    last_mex = None
    producer_log.debug(f"offset found at {last_offset}")
    if last_offset > 1:
        last_mex = _get_message(consumer, which_topic, last_offset)
    
    consumer.close()
    return last_mex#, last_offset

def _get_message(k_consumer: KafkaConsumer, which_topic: TopicPartition, offset: int) -> str:
    """Obtain the `offset` message in a TopicPartition.

    Args:
        k_consumer: a Kafka consumer.
        which_topic: from where to look for the last message.
        offset: at which offset the message was.

    Returns:

    Raises:
        Error if client is not subscribed to `which_topic`
    """

    producer_log.debug(f"seeking message")
    k_consumer.seek( which_topic, offset - 1 ) 
    producer_log.debug(f"seek successful")

    mex = None
    for message in k_consumer:
        mex = dict(json.loads(message.value))
        producer_log.debug(f"{mex}")
        if message.offset == offset - 1:
            #exit the loop after obtaining the message
            break

    producer_log.debug(f"Message looked in topic: {mex}")

    return mex

def _write_list_in_queue(topic: str, obj_list: list) -> None:
    """Writes a list in the desired topic.

    Args:
        topic: where the list should be written.
        obj_list: a list of object sorted from the most recent element to the oldest.
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
        producer_log.warning("The list of elements fed to the producer has no \"datetime\" attribute, writing no timestamp in Kafka")
        for element in reversed(obj_list):
            producer_log.debug(f"sending in \"{topic}\" message: {element.to_repr()}")
            producer.send(topic, element.to_repr() )

    producer_log.info(f"Flushing and closing producer")
    producer.flush()
    producer.close()

def _filter_duplicates(message: str, objType: MessageData, from_list: list, skip_latest: bool = True ) -> list:
    """Removes from the list all the messages that are equal or appear later in `message`.

    Args:
        message: the content that will act as filter.
        objType: object representation of `message`.
        from_list: list to be filtered.
        skip_latest: if True, skip the first element regarless of the filter, default true

    Returns:
        A list with messages more recent than `message`
    """
    last_queued_message = objType.from_repr(message)
    found_idx = None
    from_idx = None

    if skip_latest:
        from_idx = 1 # used for market trends, as the latest one is still updating
    else:
        from_idx = 0


    for idx, elem in enumerate(from_list):
        if elem == last_queued_message:
            producer_log.debug(f"last message found in API call at index {idx}: {elem.to_repr()}")
            found_idx = idx
            break

    if found_idx is not None:
        producer_log.info(f"writing the rest of missing messages")
        missing_elem = from_list[from_idx:found_idx] # from_idx == 1 skip most recent 
    else:
        producer_log.info(f"No fetched message equals \"message\"")
        missing_elem = from_list[from_idx:]

    return missing_elem

def write_unique(topic: str, read_partition = int, list_elem = List[MessageData], list_elem_type = MessageData, skip_latest = True ) -> None:
    """ Writes messages in a Kafka topic, avoiding duplicates by looking at the last message in the queue.

    Args:
        topic: in which queue the new messages will be appended.
        read_partition: from which partition the consumer will detect the last message. TODO can be omitted if raising the ACK?
        list_elem: a list of elements that goes from the latest to the oldest.
        list_elem_type: of which instance are the Objects in 'list_elem'. TODO can be omitted?
        skip_latest: should the first message in 'list_elem' be skipped? Default True
    """
    if True in ( not isinstance( el, MessageData ) for el in list_elem):
        producer_log.error("\"list_elem\" passed has elements that are not instances of MessageData ")
        raise TypeError

    which_topic = TopicPartition(topic = topic, partition = read_partition)

    #message, offset = last_message_in_topic(which_topic)
    message = last_message_in_topic(which_topic)


    #if offset > 1:
    if message is not None:
        # Go back until it is found the trend equal the one in the queue
        missing_messages = _filter_duplicates(message, list_elem_type, list_elem, skip_latest = skip_latest)
    else: # no message in the topic's partition
        producer_log.info("No offset present, proceeding writing all the data")

        start = None
        if skip_latest:
            start = 1
        else:
            start = 0

        missing_messages = list_elem[start:]
        
    _write_list_in_queue(topic, missing_messages)