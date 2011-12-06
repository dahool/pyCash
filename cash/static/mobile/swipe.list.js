$(function(){
	// expsenses
	$('div').live('pageshow',function(event, ui){
		createSwipeMenu(event, 'swipemenu_expenses', 'swipeleft');
		createSwipeMenu(event, 'swipemenu_payments', 'swipeleft');
	});
})

function createSwipeMenu(event, id, direction) {
	if ( event.target.id.indexOf(id) >= 0) {
		$('.divSwipe').remove();
		// add swipe event to the list item, removing it first (if it exists)
		$('ul li').unbind(direction).bind(direction, function(e){
			// reference the just swiped list item
			var $li = $(this);
			// remove all swipe divs first
			$('.divSwipe').remove();
			// create buttons and div container
			var options = $li.attr("swipe-options");
			var opts = $.parseJSON(options);
			var $divSwipe = $('<div class="divSwipe"></div>');
			$li.prepend($divSwipe);
			$.each(opts.buttons, function(index, obj) {
				var $b = $('<a>'+obj.value+'</a>').attr({
					'class': 'aSwipeBtn ui-btn-up-'+obj.style,
					'href': obj.href
				});
				$divSwipe.prepend($b);	
			});
			// insert buttons into divSwipe
			$divSwipe.show(100);
			// add escape route for swipe menu
			$('body').bind('tap', function(e){
				// if the triggering object is a button, fire it's tap event
				if (e.target.className.indexOf('aSwipeBtn') >= 0) $(e.target).trigger('click'); 
				// remove any existing cancel buttons
				$('.divSwipe').remove();
				// remove the event
				$('body').unbind('tap');
			});
		});
	}		
}