SyncManager = function(config) {
	Ext.apply(this, config);
	SyncManager.superclass.constructor.call(this);
};

Ext.extend(SyncManager, Ext.util.Observable, {
	syncExpenses: function() {
		$.postJSON('sync/expenses',{},
				function(response){
					if (response.success) {
						Ext.Msg.info(String.format(_('{0} records received.'),response.value));
					} else {
						Ext.Msg.error('An error ocurred during sync.');
					}
				},_('Retrieving expenses...')
		)
	},
	syncCategory: function() {
		$.postJSON('sync/category',{},
				function(response){
					if (response.success) {
						Ext.Msg.info(String.format(_('Done.')));
					} else {
						Ext.Msg.error('An error ocurred during sync.');
					}
				},_('Sending categories...')
		)
	},
	syncPaymentType: function() {
		$.postJSON('sync/paymenttype',{},
				function(response){
					if (response.success) {
						Ext.Msg.info(String.format(_('Done.')));
					} else {
						Ext.Msg.error('An error ocurred during sync.');
					}
				},_('Sending payment types...')
		)		
	}	
});
