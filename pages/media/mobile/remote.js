function getRemoteData(url, data, callback) {
	$.ajax({
	    type: 'POST',
/*	    jsonp: 'jqback',*/
	    url: url,
	    data: data,
	    success: callback,
/*	    success: function(response) {
	        callback($.parseJSON(response));
	    },*/
	    dataType: "json",
	});       
};

var paymentTypes = []
var categoryList = []

function retrieveCategories() {
    data = {dir: 'ASC', sort: 'category'};
    url = dutils.urls.resolve('subcategory_list');;
    getRemoteData(url, data, function(resp) {
        categoryList = resp;
    });
}
function retrievePaymentType() {
    data = {dir: 'ASC', sort: 'name'};
    url = dutils.urls.resolve('payment_type_list');;
    getRemoteData(url, data, function(resp) {
    	console.log(resp);
        paymentTypes = resp;
    });
}

