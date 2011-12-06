Local.Tax = function(config) {
	Ext.apply(this, config);
	Local.Tax.superclass.constructor.call(this);
};

Ext.extend(Local.Tax, Ext.util.Observable, {
	reload: function() {
		this.ds.reload();
	},
	
	remove: function() {
		var parent = this;
		var record = parent.grid.selModel.getSelected().data;
		Ext.Msg.confirm(
			_('Sure?'),
			String.format(_('Do you really want to delete Tax for Service {0}?'),record.service),
			function(response) {
				if('yes' == response) {
					var rid = record.id;
					$.postJSON('tax/delete'
						,{ id: rid }
						,function(response){
							if (response.success) {
								parent.reload();
							} else {
								Ext.Msg.error(response.msg);
							}
						},
						String.format(_('Deleting {0}...'),record.service)
					);											
				}
			}
		);					
	},
	
	pay: function() {
		var parent = this;
		var record = parent.grid.selModel.getSelected().data;

		var items = [
			    {
					xtype : "textfield",
					cls : "x-hide-display",
					hideLabel: true,
		    		name : "id",
					value: record.id,
			  	}, 						    
			    {
			    	fieldLabel: _('Service'), 
			    	xtype : "textfield",
			    	name : "service",
			    	width: 180,
			    	readOnly: true,
			    	value: record.service
			  	},
			    {
			    	fieldLabel: _('Amount'), 
			    	xtype : "numberfield",
			    	name : "amount",
			    	id: "amount",
			    	width: 180,
			    	allowBlank: false,
			    	maxLength: 255,
			    	selectOnFocus: true,
			    	value: record.amount
			  	},						  	
			    {
			    	fieldLabel: _('Expire date'), 
			    	xtype : "datefield",
			    	name : "nextExpire",
			    	format: "d/m/Y",
			    	width: 180,
			    	selectOnFocus: true,
			    	value: record.nextExpire
                },
			    {
			    	fieldLabel: _('Next expire date'), 
			    	xtype : "datefield",
			    	name : "nextExpire2",
			    	format: "d/m/Y",
			    	width: 180,
			    	selectOnFocus: true,
			    	allowBlank: true,
                }]
	
		var ed = new EditWindow({
			id: 'TaxPay',
			url: 'tax/pay',
			title: String.format(_('Paying service {0}'),record.service),
            width: 390,
            height: 180,
            labelWidth: 130,
            iconCls: 'icon-pay',	
            focus: 'amount',
            items: items,
            listeners: {
            	'success': function() {
            		parent.reload();
            	}
            }				            								
		});
		ed.show();
	
	},
	
	edit: function() {
		var parent = this;
		var record = parent.grid.selModel.getSelected().data;
		subCategoryStore.clearFilter();
		var items = [
			    {
					xtype : "textfield",
					cls : "x-hide-display",
					hideLabel: true,
		    		name : "id",
					value: record.id,
			  	}, 						    
			    {
			    	fieldLabel: _('Service'), 
			    	xtype : "textfield",
			    	name : "service",
			    	value: record.service,
			  	},
			    {
			    	fieldLabel: _('Amount'), 
			    	xtype : "numberfield",
			    	name : "amount",
			    	id: "amount",
			    	value: record.amount,
			  	},						  	
			    {
			    	fieldLabel: _('Expire date'), 
			    	xtype : "datefield",
			    	name : "expire",
			    	value: record.expire,
			  	},
			    {
			    	fieldLabel: _('Next expire date'), 
			    	xtype : "datefield",
			    	name : "nextExpire",
			    	allowBlank: true,
			    	value: record.nextExpire,
			  	},
			    {
			    	fieldLabel: _('Last pay date'), 
			    	xtype : "datefield",
			    	name : "lastPay",
			    	value: record.lastPay,
			    	allowBlank: true,
			  	},
			  	{
			    	fieldLabel: _('Account'), 
			    	xtype : "textfield",
			    	name : "account",
			    	allowBlank: true,
			    	value: record.account
                },						  	
			    {
			    	xtype : "subCategoryCombo",
			    	fieldLabel: _('Sub Category'),
			    	store: subCategoryStore,
			    	value: record.subCategoryId,
			  	},
			  	{
					xtype: 'combo',
					fieldLabel: _('Payment Type'),
					hiddenName: 'paymentType.id',
					forceSelection: true,
					triggerAction: 'all',
				   	store: paymentTypeStore,
				   	mode: 'local',
				   	value: record.paymentTypeId,
				   	displayField: 'name',
				   	valueField: 'id',								   	
                }]
	
		var ed = new EditWindow({
			id: 'TaxEd',
			url: 'tax/update',
			title: _('Editing...'),
            height: 280,
            iconCls: 'icon-edit',	
            focus: 'amount',
            items: items,
            labelWidth: 130,
            listeners: {
            	'success': function() {
            		parent.reload();
            	}
            }				            								
		});
		ed.show();
	
	},

	add: function() {
		var parent = this;
		var items = [
			    {
			    	fieldLabel: _('Service'), 
			    	xtype : "textfield",
			    	name : "service",
			    	id: "service",
			  	},
			    {
			    	fieldLabel: _('Amount'), 
			    	xtype : "numberfield",
			    	name : "amount",
			  	},						  	
			    {
			    	fieldLabel: _('Expire date'), 
			    	xtype : "datefield",
			    	name : "expire",
			  	},
			    {
			    	fieldLabel: _('Next expire date'), 
			    	xtype : "datefield",
			    	name : "nextExpire",
			    	allowBlank: true,
			  	},
			  	{
			    	fieldLabel: _('Account'), 
			    	xtype : "textfield",
			    	name : "account",
			    	allowBlank: true,
                },
			    {
			    	xtype : "subCategoryCombo",
			    	fieldLabel: _('Sub Category'),
			    	store: subCategoryStore,
			  	},
			  	{
					xtype: 'combo',
					fieldLabel: _('Payment Type'),
					hiddenName: 'paymentType.id',
					forceSelection: true,
					triggerAction: 'all',
				   	store: paymentTypeStore,
				   	mode: 'local',
				   	displayField: 'name',
				   	valueField: 'id',								   	
                }]
	
		var ed = new EditWindow({
			id: 'TaxAdd',
			url: 'tax/save',
			title: _('New Tax'),
            height: 250,
            iconCls: 'icon-add',	
            focus: 'service',
            items: items,
            labelWidth: 130,
            listeners: {
            	'success': function() {
            		parent.reload();
            	}
            }				            								
		});
		ed.show();
	},

	init: function() {
		var parent = this;
		this.ds = new Ext.data.JsonStore({
		    url: 'tax/list',
		    root: 'rows',
		    totalProperty:'total',
		    id:'id',
		    fields: ['id','service','subCategory','subCategoryId','expire','amount','nextExpire','lastPay','paymentType','paymentTypeId','account'],
		    sortInfo: {field: 'service', direction: 'ASC'},
		    remoteSort: true,
		});    	    				
	
	    this.pagingBar = new Ext.PagingToolbar({
	        pageSize: 50,
	        store: this.ds,
	        displayInfo: true,
			items:['-',
					{
					xtype: 'combo',
					editable: false,
					triggerAction: 'all',
				   	store: getPageSizeList(),
				   	width: 50,
				   	value: 50,
				   	listeners: {
				   			select:
				   				function(combo,record,index) {
				   					parent.pagingBar.pageSize = combo.lastSelectionText;
				   					parent.ds.reload({params:{start:0, limit: parent.pagingBar.pageSize}});
				   				}
				   		}
	                }
				]
	    });

	 	this.actionsColumn = new Ext.ux.grid.RowActions({
			actions:[
				{
	    			iconCls: 'icon-pay',
	    			tooltip: _('Pay'),
	    		},{
					iconCls:'icon-edit',
					tooltip: _('Edit'),
				},{
				iconCls:'icon-delete',
				tooltip: _('Delete')
				}
			],
			callbacks: {
				'icon-edit': function(grid, record, action, rowIndex, colIndex) {
							parent.edit();
						},
				'icon-delete': function(grid, record, action, rowIndex, colIndex) {
							parent.remove();
						},
				'icon-pay': function(grid) {
						parent.pay();
					}
			}
		});

	    this.grid = new Ext.grid.GridPanel({
	    	id: 'tax-grid',
	    	iconCls : 'menu-tax',
			store: this.ds,
			title: _('Taxes'),
	        columns: [
	        	this.actionsColumn,
	        	{header: _('Service'), sortable: true, dataIndex: 'service'},
	        	{header: _('Amount'), sortable: true, dataIndex: 'amount',renderer: Ext.util.Format.usMoney, align: 'right'},
	        	{header: _('Expire date'), sortable: true, dataIndex: 'expire',renderer: Ext.util.Format.dateRenderer('d/m/Y'), align: 'right'},
	        	{header: _('Next expire date'), sortable: true, dataIndex: 'nextExpire',renderer: Ext.util.Format.dateRenderer('d/m/Y'), align: 'right'},
	        	{header: _('Last pay date'), sortable: true, dataIndex: 'lastPay',renderer: Ext.util.Format.dateRenderer('d/m/Y'), align: 'right'},
	        	{header: _('Account'), sortable: true, dataIndex: 'account'},
	        	{header: _('Sub Category'), sortable: true, dataIndex: 'subCategory'},
	        	{header: _('Payment Type'), sortable: true, dataIndex: 'paymentType'},
	        ],
	        bbar: this.pagingBar,
    		tbar: new Ext.Toolbar({
				items:[{
						text: _('Add'),
						iconCls: 'icon-add',
						handler: function() {
							parent.add();
						}
					}]
    		}),					       
		    viewConfig: {
		        forceFit: true
		    },
		    plugins: [ this.actionsColumn ],
            listeners: {
                'rowdblclick': function() {
                    	parent.edit();
                },
            	'rowcontextmenu': function (grid, rowIndex, e) {
					    e.stopEvent();
					    grid.selModel.selectRow(rowIndex);
					
					    var listContextMenu = new Ext.menu.Menu({
					    	items: [
					    		{
					    			iconCls: 'icon-pay',
					    			text: _('Pay'),
					    			handler: function() {
					    				parent.pay();
					    			}
					    		},				    	
					    		{
					    			iconCls: 'icon-edit',
					    			text: _('Edit'),
					    			handler: function() {
					    				parent.edit();
					    			}
					    		},
					    		{
					    			iconCls: 'icon-delete',
					    			text: _('Delete'),
					    			handler: function() {
										parent.remove();
					    			}
					    		},
					    		{
					    			iconCls: 'icon-add',
					    			text: _('Add'),
					    			handler: function() {
					    				parent.add();
					    			}
					    		},				    	
					    	]
					    });
					    
					    listContextMenu.showAt(e.getXY());
				},
            	'contextmenu': function onTaxContextMenu(e) {
		    			e.stopEvent();
					    var listContextMenu = new Ext.menu.Menu({
					    	items: [
					    		{
					    			iconCls: 'icon-add',
					    			text: _('Add'),
					    			handler: function() {
					    				parent.add();
					    			}
					    		},				    	
					    	]
					    });
					    listContextMenu.showAt(e.getXY());	    			
	    		},    
            }				    
			/* plugins: [new Ext.ux.grid.Search({
						iconCls:'icon-zoom'
						,autoFocus:true
					})] */				    
	    });
					    	    				
	},
	load: function(panel) {
		panel.addActive(this.grid);
		this.ds.load({params:{start:0, limit: this.pagingBar.pageSize}});
	},
});			    	    
