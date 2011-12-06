$(function(){
	// expsenses
	$('div').live('pageshow',function(event, ui){
		swipeMenuExpenses(event);
		swipeMenuPayments(event);
	});
})

function swipeMenuPayments(event) {
	if ( event.target.id.indexOf('swipemenu_payments') >= 0) {
		$('.divSwipe').remove();
		// add swipe event to the list item, removing it first (if it exists)
		$('ul li').unbind('swipeleft').bind('swipeleft', function(e){
			// reference the just swiped list item
			var $li = $(this);
			// remove all swipe divs first
			$('.divSwipe').remove();
			// create buttons and div container
			var $divSwipe = $('<div class="divSwipe"></div>');
			var $myBtn01 = $('<a>Borrar</a>')
							.attr({
								'class': 'aSwipeBtn ui-btn-up-r',
								'href': 'page.html'
							});
			var $myBtn02 = $('<a>Editar</a>')
							.attr({
								'class': 'aSwipeBtn ui-btn-up-e',
								'href': 'page.html'
							});
			// insert swipe div into list item
			$li.prepend($divSwipe);
			// insert buttons into divSwipe
			$divSwipe.prepend($myBtn02,$myBtn01).show(100);
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

function swipeMenuExpenses(event) {
	if ( event.target.id.indexOf('swipemenu_expenses') >= 0) {
		$('.divSwipe').remove();
		// add swipe event to the list item, removing it first (if it exists)
		$('ul li').unbind('swipeleft').bind('swipeleft', function(e){
			// reference the just swiped list item
			var $li = $(this);
			// remove all swipe divs first
			$('.divSwipe').remove();
			// create buttons and div container
			var $divSwipe = $('<div class="divSwipe"></div>');
			var $myBtn01 = $('<a>Borrar</a>')
							.attr({
								'class': 'aSwipeBtn ui-btn-up-r',
								'href': 'page.html'
							});
			var $myBtn02 = $('<a>Editar</a>')
							.attr({
								'class': 'aSwipeBtn ui-btn-up-e',
								'href': 'page.html'
							});
			// insert swipe div into list item
			$li.prepend($divSwipe);
			// insert buttons into divSwipe
			$divSwipe.prepend($myBtn02,$myBtn01).show(100);
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