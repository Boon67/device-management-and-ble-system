TABLE="device_ThunderBoard";
function portal_DeviceList(req, resp) {
    ClearBlade.init({request: req});
	var query = ClearBlade.Query({collectionName: TABLE});
    query.fetch(function(err, result) {
        if (err) {
            resp.error(err);
        } else {
            resp.success(result.DATA);
        }
    });
}