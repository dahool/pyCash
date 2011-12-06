$(function() {
        // catch forms
    $(document).on("pageload", function() {
        $('a[data-cache=false]').on('click', function() {
            var $this = $(this);
            $.mobile.changePage($this.attr('href'),{reloadPage: true, transition: "none"});
        });
        $('[form-submit]').on("click",function() {
            var frm = $(this).attr('form-submit');
            var rte = false;
            if ($(this).attr('return')) {
            	rte = $(this).attr('return');
            }
            doPostAction($(frm).attr('action'), $(frm).serialize(), frm, rte);
            return false;
        }); 
    });
});

function doPostAction(url, data, elem, rte) {
    $.ajax({
        type: 'POST',
        url: url,
        data: data,
        success: function(data) {
        	if (data.msg) {
                $(elem).simpledialog({
                    'mode' : 'bool',
                    'prompt' : data.msg,
                    'useModal': true,
                    'buttons' : {
                      'OK': {
                        click: function() {}
                        }
                    }
                });
        	}
        	if (data.success) {
            	if (rte) {
            		$.mobile.changePage(rte, {reloadPage: true});
            	}
        	}
        },
        dataType: "json"
    });
}

function confirmSingleAction(url, id) {
	var $elem = $('div[data-role="content"]:visible');
	var rte = $elem.attr("data-return");
    $elem.simpledialog({
        'mode' : 'bool',
        'prompt' : "¿Confirma eliminación?",
        'useModal': true,
        'buttons' : {
          'Si': {
            click: function() {
            	doPostAction(url, {"id": id}, $elem, rte);
            },
    		icon: "delete",
    		theme: "c"
          },
    	  'No': {
    		click: function() {
    	    },
    	  }
        }
    });	
}
