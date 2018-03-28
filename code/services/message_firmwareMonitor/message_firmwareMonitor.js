function message_firmwareMonitor(req, resp){
    ClearBlade.init({request:req});
    var msg = ClearBlade.Messaging();
    g_deleteMessages(FIRMWARETOPIC);
    
    var query = ClearBlade.Query({collectionName: TABLENAME_FILES});
	query.columns(["item_id", "filename", "description", "fileversion", "os","architecture"]);
	query.ascending("filename");
	
	query.fetch(function(err, data){
	if (err)
	    resp.error(data);
	else
	     msg.publish(FIRMWARETOPIC, JSON.stringify(data.DATA));
	     log(data);
	     resp.success(true);
    });
}