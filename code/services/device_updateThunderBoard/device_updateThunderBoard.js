var TABLE="device_ThunderBoard";
var HISTORIANTABLE="device_ThunderBoard_Historian";
var _resp;
/**
 * Manages the thundeboard record
 * If the device exists it updates, the data
 * If the device does not exist, it creates a new record
 */
function device_updateThunderBoard(req, resp){
    ClearBlade.init({request:req});
    _resp=resp;
    var d=req.params.body;
    d=JSON.parse(d);

    data={};
    data.deviceid=d.deviceid;
    data.deviceaddress=d.deviceid;
    data.device_name=d.devicename;
    data.gateway=d.edgename;
    data.sound=d.sound;
    data.temperature=d.temperature;
    data.co2=d.co2;
    data.humidity=d.humidity;
    data.light=d.ambientLight;
    data.pressure=d.pressure;
    data.powersource=d.powersource;
    data.uvindex=d.uvIndex;
    data.voc=d.voc;
    data.rssi=d.rssi;
    data.timestamp=new Date();
    log(req.params.topic);
    deleteMessages(req.params.topic);
    var searchFilter={ deviceid: data.deviceid };
    findRecord(searchFilter)
    .then(function(result){
        if (result.length===0) {
            createRecord(TABLE, data);
            createRecord(HISTORIANTABLE, data);
        }
        else {
            updateRecord(result[0].item_id, data);
            createRecord(HISTORIANTABLE, data); 
        }

    })
    .catch(function(e){_resp.err("Search failed")});
}




/**
 * Creates a record with the define payload
 * Note: assumes the payload matches the table structure
 * 
 */
function createRecord(tablename, payload) {
    var col = ClearBlade.Collection( {collectionName: tablename } );
    col.create(payload, function(err, result) {
        if (err) {
            d.reject(err);
        } else {
            d.resolve(result);
        }
    });
    return d.promise;
}

/**
 * Updates a record with a given itemID and values
 * @param {string} itemID The itemID to be updated
 * @param {object} values properites to query
 */
function updateRecord(itemID, values) {
    var query = ClearBlade.Query({collectionName:TABLE});
    query.equalTo('item_id', itemID);
    d = Q.defer();
    query.update(values, function(err, result) {
        if (err) {
            d.reject(err);
        } else {
            d.resolve(result);
        }
    });
    return d.promise;
}

/**
 * Locates a record in the database
 * @param {object} values list of property and values to match
 */
function findRecord(values) {
    var query = ClearBlade.Query({collectionName: TABLE});
    //breakout the key/values to equalTo query
    for (var key in values) {
        if (values.hasOwnProperty(key)) {
            console.log(key + " = " + values[key]);
            query.equalTo(key, values[key]);
        }
    }   
    d = Q.defer();
	query.fetch(function(err, result) {
        if (err) {
            d.reject(new Error(err));
        } else {
            d.resolve(result.DATA);
        }
    });
    return d.promise;
}


function deleteMessages(topic) {
    return;
    var msg = ClearBlade.Messaging();
    d = Q.defer();
    msg.getAndDeleteMessageHistory(topic, 0, null, null, null, function(err, result) {
        if (err) {
            d.reject(err);
        } else {
            d.resolve(result);
        }
    });
    return d.promise;
}




