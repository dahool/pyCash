/* --- MENU --- */
var systemMenu = new Ext.menu.Menu({
	items : [{
		text : _('Categories'),
		iconCls : 'menu-item',
		handler : function() {
			loadPage('category', 'category-panel');
		}
	},
	{
		text : _('Payment Types'),
		iconCls : 'menu-item',
		handler : function() {
			loadPage('paymentType','paymentType-grid');
		}
	},
	{
		text : _('Cards'),
		iconCls : 'menu-item',
		handler : function() {
			loadPage('card','card-panel');
		}
	},
	{
		text : _('Authentication Token'),
		iconCls : 'menu-item',
		handler : function() {
			loadPage('token','token-grid');
		}
	},    
    {
		text: _('Syncronize'),
		iconCls: 'menu-sync',
		menu: {
			items: [
			     {
					text: _('Expenses'),
					iconCls: 'menu-item',
					handler: function() {
						s = new SyncManager();
						s.syncExpenses();
					}
				},{
					text: _('Category'),
					iconCls: 'menu-item',
					handler: function() {
						s = new SyncManager();
						s.syncCategory();
					}
				},{
					text: _('Payment Type'),
					iconCls: 'menu-item',
					handler: function() {
						s = new SyncManager();
						s.syncPaymentType();
				}
			},			
			]
		}
	},
	{
		text : _('Logout'),
		iconCls : 'menu-logout',
		handler : function() {
			window.location="/logout";
		}
	}	
	]
});

var taxMenu = new Ext.menu.Menu({
	items : [{
		text : _('Upcoming'),
		iconCls : 'menu-upcoming',
		handler : function() {
			loadPage('tax/upcoming',
					'upcoming-panel');
		}
	},{
		text : _('Taxes'),
		iconCls : 'menu-tax-list',
		handler : function() {
			loadPage('tax', 'tax-grid');
		}
	}]
});

var mainTBar = new Ext.Toolbar({
	items : [{
		text : _('System'),
		iconCls : 'menu-system',
		menu : systemMenu
	}, {
		text : _('Stats'),
		iconCls : 'menu-stats',
		handler : function() {
			loadPage('stats',
					'stats-panel');
		}
	}, {
		text : _('Taxes'),
		iconCls : 'menu-tax',
		menu : taxMenu
	},{
		text : _('Incomes'),
		iconCls : 'menu-income',
		handler : function() {
			loadPage('income', 'income-panel');
		}
	}, {
		text : _('Loans'),
		iconCls : 'menu-loan',
		handler : function() {
			loadPage('loan', 'loan-panel');
		}
	},/* {
		text : _('Card Expenses'),
		iconCls : 'menu-cards',
		handler : function() {
			loadPage('cardExpense', 'cardExpense-panel');
		}
	}*/
	 {
		text : _('Debits'),
		iconCls : 'menu-debits',
		handler : function() {
			loadPage('debits', 'debits-panel');
		}
	}	
	,{
		text : _('Expenses'),
		iconCls : 'menu-expense',
		handler : function() {
			loadPage('expense', 'expense-panel');
		}
	}]
});

/* -- BARS -- */
var mainStatusBar = new Ext.StatusBar({
	id : 'status-bar',
	defaultText : _('Ready'),
	defaultIconCls : ''
});

mainTabPanel = new ExtTabPanel({
	id : 'main-tab',
	activeTab : 0,
	resizeTabs : true,
	tabWidth : 150,
	minTabWidth : 120,
	enableTabScroll : true,
	items : [{
		title : '-'
	}],
	plugins : new Ext.ux.TabCloseMenu()
});

var containerPanel = {
	header : false,
	title : 'Menu',
	tbar : mainTBar,
	bbar : mainStatusBar,
	border : false,
	layout : 'fit',
	items : mainTabPanel
}
