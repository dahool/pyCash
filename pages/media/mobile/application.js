/*
$(function() {
	retrievePaymentType();
	retrieveCategories();
});

$(document).live("pageinit", function( event, data ){
    if ($("#ptype").length > 0 && $("#ptype > option").size() == 0) {
    	console.log("1");
        if (paymentTypes.rows) {
        	console.log("2");
            var ptype = "";
            $.each(paymentTypes.rows, function(index, value) { 
                ptype += "<option value='"+value.id+"'>"+value.name+"</option>";
            });
            $("#ptype").html(ptype);
        }
    }
    if ($("#category").length > 0 && $("#category > option").size() == 0) {
        if (categoryList.rows) {
            var clist = "<option data-placeholder='true'>Categor&iacute;a</option>";
            var l = 0;
            $.each(categoryList.rows, function(index, value) { 
                if (l != value.categoryId) {
                    clist += "<optgroup label='"+value.category+"'>";
                    if (l == 0) l = value.categoryId;
                }
                clist += "<option value='"+value.id+"'>"+value.name+"</option>";
                if (l != value.categoryId) {
                    clist += "</optgroup>";
                    l = value.categoryId;
                }
            });
            $("#category").html(clist);
        }
    }    
});
*/
