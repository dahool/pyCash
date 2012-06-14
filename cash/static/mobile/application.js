$(function() {
        // catch forms
/*    $(document).on("pageload", function() {
        $('a[data-cache=false]').on('click', function() {
            var $this = $(this);
            $.mobile.changePage($this.attr('href'),{reloadPage: true, transition: "fade"});
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
    });*/
    $(document).on("mobileinit", function(){
        $.mobile.loadingMessage = "Cargando...";
    });
    
    $(document).on("pageinit", function(){
        $('a[data-cache=false]').unbind('click').on('click', function() {
            var $this = $(this);
            var href = $this.attr('href');
            if (href == '#') {
                href = $.mobile.path.get();
            }
            $.mobile.changePage(href,{reloadPage: true, transition: "fade"});
        });
        $('[form-submit]').unbind('click').on("click",function() {
            var frm = $(this).attr('form-submit');
            var rte = false;
            if ($(this).attr('return')) {
            	rte = $(this).attr('return');
            }
            doPostAction($(frm).attr('action'), $(frm).serialize(), frm, rte);
            return false;
        });
    });     

// force certain pages to be refreshed every time. mark such pages with
// 'data-cache="never"'
//
    jQuery('div').live('pagehide', function(event, ui){
      var page = jQuery(event.target);

      if(page.attr('data-cache') == 'never'){
        page.remove();
      };
    });

// for pages marked with 'data-cache="never"' manually add a back button since
// JQM doesn't. this is *okay* because we know the browswer history stack is
// intact and goes to the correct 'back' location.
// specified back button - however!
//
    jQuery('div').live('pagebeforecreate', function(event, ui){
      var page = jQuery(event.target);

      if(page.attr('data-cache') == 'never'){
        var header = page.find('[data-role="header"]');

        if(header.find('[data-rel="back"]').size() == 0){
          var back = jQuery('<a href="#" data-icon="back" data-rel="back">Back</a>');
          header.prepend(back);
        };
      };
    });
            
});

function doPostAction(url, data, elem, rte) {
    $.ajax({
        type: 'POST',
        url: url,
        data: data,
        beforeSend: function(r,s) {
            $.mobile.showPageLoadingMsg();
        },
        complete: function(r,s) {
            $.mobile.hidePageLoadingMsg();
        },
        success: function(data) {
        	if (data.success) {
            	if (data.msg) {
                    $(elem).simpledialog({
                        'mode' : 'bool',
                        'prompt' : data.msg,
                        'useModal': true,
                        'buttons' : {
                          'OK': {
                            click: function() {
                            	afterSubmit(elem, rte)
                            }
                        }
                    }
                    });
            	}  else {
                    afterSubmit(elem, rte)
                }
        	} else {
            	if (data.msg) {
                    $(elem).simpledialog({
                        'mode' : 'bool',
                        'prompt' : data.msg,
                        'useModal': true,
                        'buttons' : {
                          'OK': {
                            click: function() {
                            	// do nothing
                    		}
                            }
                        }
                    });
            	}        		
        	}
        },
        dataType: "json"
    });
}

function afterSubmit(elem, rte) {
    if (rte) {
        if (rte == 'back') {
            history.back();
        } else {
            $.mobile.changePage(rte, {reloadPage: true});
        }
    } else {
        if ($(elem).attr('after-submit-clean')) {
            var values = $(elem).attr('after-submit-clean').split(",");
            $.each(values, function(idx, value) {
                $("#"+value).val("");
            });
            $("#"+values[0]).focus();
        }
    }    
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
