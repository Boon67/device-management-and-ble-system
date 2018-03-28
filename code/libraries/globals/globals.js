var MBFUNCTION = {
    READCOIL:1,
    READINPUT:2,
    READHOLDINGREGISTERS:3,
    READINPUTREGISTERS:4,
    WRITESINGLECOIL:5,
    WRITESINGLEHOLDINGREGISTER:6,
    WRITEMULTIPLECOILS:15,
    WRITEMULTIPLEHOLDINGREGISTERS:16
};

var FIRMWARETOPIC="firmware";
var PORTALUPDATETOPIC="portal";

var MODBUSERRORTOPIC="data/modbus/command/error";
var MODBUSREQUESTTOPIC="data/modbus/command/request";
var MODBUSRESPONSETOPIC="data/modbus/command/response";
var MBHOST="192.168.1.6";
var DEFAULTUNIT=0;
var STARTADDR=0;
var ENDADDR=24;

var TABLENAME_FILES="firmware";


//Should put QLib to ensure execution before
function g_deleteMessages(topic) {
var callback = function (err, data) {
		if(err) {
		    //fail silently
			log("deleteMessages Error: " + JSON.stringify(data));
		} else {
		    return data;
		}
    };

    var msg = ClearBlade.Messaging();
    msg.getAndDeleteMessageHistory(topic, 0, null, null, null, callback); 
}