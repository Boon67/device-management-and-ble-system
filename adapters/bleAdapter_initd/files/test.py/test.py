#!/usr/bin/python
import argparse, sys, logging, os, json, socket, logging, struct, time, datetime
from bluepy.btle import *
from clearblade.ClearBladeCore import System, Query, Developer
from clearblade.ClearBladeCore import cbLogs

ADAPTER_NAME = "ble-client"
CB_CONFIG = {}
SCANTIMEPERIOD = 60
CB_MQTT = {}
SCOPE_VARS = {
    'MQTT_CONNECTED': False,
    'EXIT_APP': False
}

#########################
#STARTUP ARGUMENT CONFIG
#########################
def parse_args(argv):
    """Parse the command line arguments"""

    parser = argparse.ArgumentParser(description='Start ClearBlade Adapter')
    parser.add_argument('--systemKey', required=True, help='The System Key of the ClearBlade \
                        Plaform "System" the adapter will connect to.')

    parser.add_argument('--systemSecret', required=True, help='The System Secret of the \
                        ClearBlade Plaform "System" the adapter will connect to.')

    parser.add_argument('--deviceID', required=False, \
                        help='The id/name of the device that will be used for device \
                        authentication against the ClearBlade Platform or Edge, defined \
                        within the devices table of the ClearBlade platform.')
    
    parser.add_argument('--mqttUserID', required=False, \
                        help='The active key of the device that will be used for device \
                        authentication against the ClearBlade Platform or Edge, defined within \
                        the devices table of the ClearBlade platform.')

    parser.add_argument('--mqttPassword', required=False, \
                        help='The active key of the device that will be used for device \
                        authentication against the ClearBlade Platform or Edge, defined within \
                        the devices table of the ClearBlade platform.')

    parser.add_argument('--activeKey', required=False, \
                        help='The active key of the device that will be used for device \
                        authentication against the ClearBlade Platform or Edge, defined within \
                        the devices table of the ClearBlade platform.')

    parser.add_argument('--platformURL', dest="platformURL", default="http://localhost", \
                        help='The HTTP URL of the ClearBlade Platform or Edge the adapter will \
                        connect to. The default is https://localhost.')

    parser.add_argument('--httpPort', dest="httpPort", default="443", \
                        help='The HTTP Port of the ClearBlade Platform or Edge the adapter will \
                        connect to. The default is 443.')

    parser.add_argument('--messagingUrl', dest="messagingURL", default="localhost", \
                        help='The MQTT URL of the ClearBlade Platform or Edge the adapter will \
                        connect to. The default is https://localhost.')

    parser.add_argument('--messagingPort', dest="messagingPort", default="1883", \
                        help='The MQTT Port of the ClearBlade Platform or Edge the adapter will \
                        connect to. The default is 1883.')

    parser.add_argument('--topicRoot', dest="topicRoot", default="bleAdapter", \
                        help='The root of MQTT topics this adapter will subscribe and publish to. \
                        The default is "".')

    parser.add_argument('--requestSubtopic', dest="requestSubtopic", default="request", \
                        help='The root of MQTT topics this adapter will subscribe and publish to. \
                        The default is "request".')

    parser.add_argument('--logLevel', dest="logLevel", default="INFO", choices=['CRITICAL', \
                        'ERROR', 'WARNING', 'INFO', 'DEBUG'], help='The level of logging that \
                        should be utilized by the adapter. The default is "INFO".')

    parser.add_argument('--logCB', dest="logCB", default=False, action='store_true',\
                        help='Flag presence indicates logging information should be printed for \
                        ClearBlade libraries.')

    parser.add_argument('--logMQTT', dest="logMQTT", default=False, action='store_true',\
                        help='Flag presence indicates MQTT logs should be printed.')

    return vars(parser.parse_args(args=argv[1:]))

#########################
#LOGGING CONFIGURATION
#########################
def setup_custom_logger(name):
    """Create a custom logger"""

    formatter = logging.Formatter(fmt='%(asctime)s %(levelname)-8s %(message)s', \
                                  datefmt='%m-%d-%Y %H:%M:%S %p')
    handler = logging.StreamHandler(stream=sys.stdout)
    handler.setFormatter(formatter)
    logger = logging.getLogger(name)
    logging.basicConfig(level=os.environ.get("LOGLEVEL", CB_CONFIG['logLevel']))
    logger.addHandler(handler)
    return logger

def on_connect(mqtt_client, userdata, flags, result_code):
    # When we connect to the broker, subscribe to the southernplayalisticadillacmuzik channel
    topic=CB_CONFIG['topicRoot'] + CB_CONFIG['requestSubtopic'] + "/#"
    logging.info('Subscribing ' + topic )
    mqtt_client.subscribe(topic)
    logging.info('Subscribing Complete')
    logging.info('Waiting for Messages.......')

def on_message(client, userdata, message):
    #Methods are scan/read/stream
    topic=CB_CONFIG['topicRoot'] + CB_CONFIG['requestSubtopic']
    logging.info("Received message '" + message.payload + "' on topic '" + message.topic + "'")

    if message.topic == topic + "/scan":
        logging.info("scan")
        payload=json.loads(message.payload)

    elif message.topic == topic + "/read":
        logging.info("read")
        payload=json.loads(message.payload)

    elif message.topic == topic + "/stream":
        logging.info("stream")
 
########MAIN LOOP#######
if __name__ == '__main__':
    CB_CONFIG = parse_args(sys.argv)
    LOGGER = setup_custom_logger(ADAPTER_NAME)

    if not CB_CONFIG['logCB']:
        logging.debug("Setting cbLogs.DEBUG to False")
        cbLogs.DEBUG = False

    if not CB_CONFIG['logMQTT']:
        logging.debug("Setting cbLogs.MQTT_DEBUG to False")
        cbLogs.MQTT_DEBUG = False

    EXITAPP = False
logging.info(json.dumps(CB_CONFIG))
CB_SYSTEM = System(CB_CONFIG['systemKey'], CB_CONFIG['systemSecret'], CB_CONFIG['platformURL'] + ":" + CB_CONFIG['httpPort'])
logging.info("Authenticating")
CBAUTH = CB_SYSTEM.User(CB_CONFIG['mqttUserID'], CB_CONFIG['mqttPassword'])
logging.info("Auth Complete")
CB_MQTT = CB_SYSTEM.Messaging(CBAUTH)
CB_MQTT.on_connect = on_connect
CB_MQTT.on_message = on_message
CB_MQTT.connect()

while not SCOPE_VARS['EXIT_APP']:
    try:
        pass
    except KeyboardInterrupt:
        SCOPE_VARS['EXIT_APP'] = True
        CB_MQTT.disconnect()
        sys.exit(0)
    except Exception as e:
        logging.info("EXCEPTION:: %s", str(e))
