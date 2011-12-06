Local.Debit = function(config) {
	Ext.apply(this, config);
	Local.Debit.superclass.constructor.call(this);
};

Ext.extend(Local.Debit, Ext.util.Observable, {
	reload: function() {
		this.ds.reload();
	},
	
	remove: function() {
		var parent = this;
		var record = parent.grid.selModel.getSelected().data;
		Ext.Msg.confirm(
			_('Sure?'),
			String.format(_('Do you really want to delete "{0}"?'),record.text),
			function(response) {
				if('yes' == response) {
					var rid = record.id;
					$.postJSON('debits/delete'
						,{ id: rid }
						,function(response){
							if (response.success) {
								parent.reload();
							} else {
								Ext.Msg.error(response.msg);
							}
						},
						String.format(_('Deleting "{0}"...'),record.text)
					);											
				}
			}
		);					
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
			    	fieldLabel: _('Name'), 
			    	xtype : "textfield",
			    	name : "text",
			    	value: record.text,
			  	},
			    {
			    	fieldLabel: _('Amount'), 
			    	xtype : "numberfield",
			    	name : "amount",
			    	id: "amount",
			    	value: record.amount,
			  	},						  	
			    {
			    	fieldLabel: _('Day of month'), 
			    	xtype : "numberfield",
			    	name : "day",
			    	value: record.day,
			  	},
			    {
			    	fieldLabel: _('Since'), 
			    	xtype : "datefield",
			    	name : "since",
			    	value: record.since,
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
			id: 'DebitEd',
			url: 'debits/update',
			title: _('Editing...'),
            height: 230,
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
			    	fieldLabel: _('Name'), 
			    	xtype : "textfield",
			    	name : "text",
			    	id: "text",
			  	},
			    {
			    	fieldLabel: _('Amount'), 
			    	xtype : "numberfield",
			    	name : "amount",
			  	},						  	
			    {
			  		fieldLabel: _('Day of month'),  
			    	xtype : "numberfield",
			    	name : "day",
			  	},
			    {
			    	fieldLabel: _('Since'), 
			    	xtype : "datefield",
			    	name : "since",
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
			id: 'DebitAdd',
			url: 'debits/save',
			title: _('New Debit'),
            height: 230,
            iconCls: 'icon-add',	
            focus: 'text',
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
		    url: 'debits/list',
		    root: 'rows',
		    totalProperty:'total',
		    id:'id',
            fields: [
			           	{name: 'id'}
	           			,{name: 'amount'}
	           			,{name: 'since'}
	           			,{name: 'text'}
	           			,{name: 'paymentType', mapping: 'paymentType_name'}
	           			,{name: 'subCategory', mapping: 'subCategory_name'}
	           			,{name: 'paymentTypeId'}
	           			,{name: 'subCategoryId', sortField: 'subCategory'}
	           			,{name: 'day'}
	           			,{name: 'last'}
		            ],		    
		    sortInfo: {field: 'text', direction: 'ASC'},
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
			}
		});

	    this.grid = new Ext.grid.GridPanel({
	    	id: 'debit-grid',
	    	iconCls : 'menu-debits',
			store: this.ds,
			title: _('Debits'),
	        columns: [
	        	this.actionsColumn,
	        	{header: _('Name'), sortable: true, dataIndex: 'text'},
	        	{header: _('Amount'), sortable: true, dataIndex: 'amount',renderer: Ext.util.Format.usMoney, align: 'right'},
	        	{header: _('Day'), sortable: true, dataIndex: 'day', align: 'right'},
	        	{header: _('Since'), sortable: true, dataIndex: 'since',renderer: Ext.util.Format.dateRenderer('d/m/Y'), align: 'right'},
	        	{header: _('Sub Category'), sortable: true, dataIndex: 'subCategory'},
	        	{header: _('Payment Type'), sortable: true, dataIndex: 'paymentType'},
	        	{header: _('Last run'), sortable: true, dataIndex: 'last',renderer: Ext.util.Format.dateRenderer('d/m/Y'), align: 'right'},
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
	    });
					    	    				
	},
	load: function(panel) {
		panel.addActive(this.grid);
		this.ds.load({params:{start:0, limit: this.pagingBar.pageSize}});
	},
});			    	    
