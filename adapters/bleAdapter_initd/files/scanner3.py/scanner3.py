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

#########################
#SCAN DELEGATE FOR BLE
#########################
class ScanDelegate(DefaultDelegate):
    def __init__(self):
        DefaultDelegate.__init__(self)

    def handleDiscovery(self, dev, isNewDev, isNewData):
        if isNewDev:
            logging.info("Discovered device %s", dev.addr)
        elif isNewData:
            logging.debug("Received new data from %s", dev.addr)

    def scanProcess(self):
        scanner = Scanner().withDelegate(ScanDelegate())
        devices = scanner.scan(SCANTIMEPERIOD)
        return devices      

#########################
#BEGIN MQTT CALLBACKS
#########################
def on_connect(mqtt_client, userdata, flags, result_code):
    logging.debug("Begin on_connect")
    if result_code == 0:
        logging.info("Connected to ClearBlade Platform MQTT broker")
        SCOPE_VARS['MQTT_CONNECTED'] = True
        logging.info("Subscribing to MQTT topics")
        mqtt_client.subscribe('bleAdapter/request')

    else:
        logging.error("Error while connecting to ClearBlade Platform message broker: \
            result code = %s", result_code)

        #rc 3 = Server unavailable. If rc = 3, we don't need to do anything.
        #MQTT will keep trying to connect for us
        if result_code != 3:
            logging.fatal("Unable to connect to mqtt. ResultCode = %s", result_code)
            SCOPE_VARS['EXIT_APP'] = True
    logging.debug("End on_connect")

def on_adapterRequest(client, userdata, message):
    # When we receive a message, print it out
    print "Received message '" + message.payload + "' on topic '" + message.topic + "'"

def on_disconnect(mqtt_client, userdata, result_code):
    """MQTT callback invoked when a connection to a broker is lost"""
    logging.debug("Begin on_disconnect")
    SCOPE_VARS['MQTT_CONNECTED'] = False
    if result_code != 0:
        logging.warning("Connection to CB Platform MQTT broker was lost, result code = %s", \
                        result_code)
        #rc 3 = Server unavailable. If rc = 3, we don't need to do anything.
        #MQTT will keep trying to connect for us
        if result_code != 3:
            SCOPE_VARS['EXIT_APP'] = True
    logging.debug("End on_disconnect")

def handle_adapter_request(mqtt_client, userdata, message):
    """Process the adapter request"""
    logging.debug("In handle_adapter_request")
    logging.debug("Payload = %s", message.payload)
    logging.debug("message payload = %s", message.payload)
    payload = json.loads(message.payload.replace("'", '"'))

    if payload["operation"] == "scan":
        #Scan for BLE Devices
        scanner = ScanDelegate();
        devices=scanner.scanProcess()
        publish_devices(devices)

    if payload["operation"] == "read":
        #Read specific Device
        print('hi')

def publish_devices(devices):
    for dev in devices:
        CB_MQTT.publish("ble/devices/" + dev.addr)


########MAIN LOOP#######
if __name__ == '__main__':
    CB_CONFIG = parse_args(sys.argv)
    LOGGER = setup_custom_logger(ADAPTER_NAME)
    logging.debug(json.dumps(CB_CONFIG))

    if not CB_CONFIG['logCB']:
        logging.debug("Setting cbLogs.DEBUG to False")
        cbLogs.DEBUG = False

    if not CB_CONFIG['logMQTT']:
        logging.debug("Setting cbLogs.MQTT_DEBUG to False")
        cbLogs.MQTT_DEBUG = False

    EXITAPP = False

    CB_SYSTEM = System(CB_CONFIG['systemKey'], CB_CONFIG['systemSecret'], CB_CONFIG['platformURL'] + ":" + CB_CONFIG['httpPort'])
    logging.info("Authenticating")
    CBAUTH = CB_SYSTEM.User(CB_CONFIG['mqttUserID'], CB_CONFIG['mqttPassword'])
    logging.info("Auth Complete")
    #Connect to the message broker
    logging.info("Initializing the ClearBlade message broker")
    CB_MQTT = CB_SYSTEM.Messaging(CBAUTH)
    CB_MQTT.on_connect = on_connect
    CB_MQTT.on_message = on_adapterRequest
    CB_MQTT.on_disconnect = on_disconnect
    logging.info("Connecting to the ClearBlade message broker")
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
