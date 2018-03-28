TABLE="device_ThunderBoard_Historian";
function portal_DeviceHistory(req, resp){
    ClearBlade.init({request: req});
	var query = ClearBlade.Query({collectionName: TABLE});
	if (req.params.deviceid)
	    query.equalTo("deviceid", req.params.deviceid);
	else 
	    resp.error("Invalid Parameter Expected: {deviceid:<DEVICEID>}");
	log(req.params);
    //d = Q.defer();
    //query.setPage(10, 1);
    query.setPage(2000, 1);
    query.descending("timestamp");
    query.fetch(function(err, result) {
        if (err) {
            resp.error(err);
        } else {
            resp.success(result);
        }
    });
}