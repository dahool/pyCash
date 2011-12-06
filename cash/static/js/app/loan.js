Local.Loan = function(config) {
	Ext.apply(this, config);
    this.addEvents(
        'payment',
        'select',
        'personPayment'
    );				
	Local.Loan.superclass.constructor.call(this);
};

Ext.extend(Local.Loan, Local.LocalPanel, {
	reload: function() {
		this.ds.load({params:{start:0, limit: this.pagingBar.pageSize}});
	},
	addPersonPayment: function() {
		this.fireEvent('personPayment');
	},
	addPayment: function() {
		var record = this.grid.selModel.getSelected().data;
		this.fireEvent('payment', record);
	},
	remove: function () {
		var parent = this;
		var record = parent.grid.selModel.getSelected().data;
		Ext.Msg.confirm(
			_('Sure?'),
			String.format(_('Do you really want do delete {0}?'),record.reason),
			function(response) {
				if('yes' == response) {
					var rid = record.id;
					$.postJSON('loan/delete'
						,{ id: rid }
						,function(response){
							if (response.success) {
								parent.reload();
							} else {
								Ext.Msg.error(response.msg);
							}
						},
						String.format(_('Deleting {0}...'),record.name)
					);											
				}
			}
		);
	},
	
	edit: function () {
		var parent = this;
		var record = parent.grid.selModel.getSelected().data;
		items = [
		    {
				xtype : "textfield",
				cls : "x-hide-display",
				hideLabel: true,
	    		name : "id",
				value: record.id,
		  	},    
		    {
		    	xtype : "combo",
		    	fieldLabel: _('Person'),
		    	hiddenName : "person.id",
		    	store: personStore,
				displayField:'name',
				valueField:'id',
		    	triggerAction:'all',
		    	mode:'local',
		    	forceSelection:true,
		    	value: record.personId,
		  	},
		    {
		    	xtype : "numberfield",
		    	fieldLabel: _('Amount'),
		    	name : "amount",
		    	value: record.amount,
		    },
		    {
		    	xtype : "numberfield",
		    	fieldLabel: _('Instalments'),
		    	name : "instalments",
		    	allowDecimals: false,
		    	allowNegative: false,
		    	value: record.instalments,
		    	minValue: 1
		  	},
		    {
		    	xtype : "textfield",
		    	fieldLabel: _('Reason'),
		    	name : "reason",
		    	value: record.reason,
		  	},					  	
		    {
		    	xtype : "datefield",
		    	fieldLabel: _('Date'),
		    	name : "date",
		    	value: record.date,
		  	},
		];

		var ed = this.newWindow({
			id: 'loanEd',
			url: 'loan/update',
			title: _('Editing...'),
            width: 330,
            height: 120,
            iconCls: 'icon-edit',	
            items: items,
            height: 180,
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
		    	xtype : "combo",
		    	fieldLabel: _('Person'),
		    	hiddenName : "person.id",
		    	id: "loan.person",
		    	store: personStore,
				displayField:'name',
				valueField:'id',
		    	triggerAction:'all',
		    	mode:'local',
		    	forceSelection:true,
		  	},
		    {
		    	xtype : "numberfield",
		    	fieldLabel: _('Amount'),
		    	name : "amount",
		  	},
		    {
		    	xtype : "numberfield",
		    	fieldLabel: _('Instalments'),
		    	name : "instalments",
		    	allowDecimals: false,
		    	allowNegative: false,
		    	value: '1',
		    	minValue: 1
		  	},		  	
		    {
		    	xtype : "textfield",
		    	fieldLabel: _('Reason'),
		    	name : "reason",
		  	},					  	
		    {
		    	xtype : "datefield",
		    	fieldLabel: _('Date'),
		    	name : "date",
		  	}];
		
		var ed = this.newWindow({
			id: 'loanAdd',
			url: 'loan/save',
			title: _('New Loan'),
            width: 330,
            height: 180,
            iconCls: 'icon-add',	
            focus: 'loan.person',
            items: items,
            listeners: {
            	'success': function() {
            		parent.reload();
            	}
            },
		});
		ed.show();
	},
	
	init: function() {
		var parent = this;
		
		//this.ds = new Ext.data.JsonStore({
		 this.ds = new Ext.ux.data.JsonGroupingStore({
		    url: 'loan/list',
		    root: 'rows',
		    totalProperty:'total',
		    id:'id',
		    fields: ['id','reason','date','amount','person','personId','balance', 'partial','instalments'],
		    sortInfo: {field: 'person', direction: 'ASC'},
		    remoteSort: true,
		    groupField: 'person',
		    remoteGroup: false,
		    listeners: {
		    	'beforeload': function(t,opt) {
		    		if (parent.pagingBar.showAll) {
		    			opt.params.all = true;	
		    		}
		    	}
		    }
		});
	
	    this.pagingBar = new Ext.PagingToolbar({
	        pageSize: 50,
	        store: this.ds,
	        displayInfo: true,
	        showAll: false,
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
				   					parent.reload();
				   				}
				   		}
	                },'-',
	                {
	                	xtype: 'checkbox',
	                	boxLabel: _('Hide canceled loans'),
	                	checked: true,
	                	listeners: {
	                		'check': function() {
                				parent.pagingBar.showAll = !this.getValue();
                				parent.reload();
	                		}
	                	}
	                }
				]
	    });

	 	this.actionsColumn = new Ext.ux.grid.RowActions({
			actions:[{
					iconCls:'icon-edit',
					tooltip: _('Edit'),
				},{
				iconCls:'icon-delete',
				tooltip: _('Delete'),		
			}],
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
	    	id: 'loan-grid',
			store: this.ds,
			title: _('Loans'),
			region: 'center',
	        columns: [
	        	this.actionsColumn
	        	,{header: _('Person'), sortable: true, dataIndex: 'person'}
	        	,{header: _('Date'), width: 30, sortable: true,renderer: Ext.util.Format.dateRenderer('d/m/Y'),dataIndex: 'date',align: 'right'}
	        	,{header: _('Reason'), width: 50, sortable: true, dataIndex: 'reason'}
	        	,{header: _('Total'), width: 30, sortable: true, dataIndex: 'amount',renderer: Ext.util.Format.usMoney, align: 'right',summaryType:'sum'}
	        	,{header: _('Monthly Amount'), width: 30, sortable: false, dataIndex: 'partial',renderer: Ext.util.Format.usMoney, align: 'right',summaryType:'sum'}
	        	,{header: _('Remaining balance'), width: 30, sortable: false, dataIndex: 'balance',renderer: Ext.util.Format.usMoney, align: 'right',summaryType:'sum'}
	        ],
	        bbar: this.pagingBar,
	        tbar: new Ext.Toolbar({
				items:[{
						text: _('Add'),
						iconCls: 'icon-add',
						handler: function() {
							parent.add();
						}
		    		},{
		    			iconCls: 'icon-add-payment',
		    			text: _('Add Payment'),
		    			handler: function() {
							parent.addPersonPayment();
		    			}
		    		}]					        
	        }),
	        view: new Ext.grid.GroupingView({
	            forceFit: true,
	            groupTextTpl: '{text} ({[values.rs.length]} {[values.rs.length > 1 ? "'+_('Loans')+'" : "'+_('Loan')+'"]})'
	        }),
		    plugins: [this.actionsColumn, new Ext.grid.GroupSummary()],
		    selModel: new Ext.grid.RowSelectionModel({
		    	 singleSelect: true,
		    	 listeners: {
		    	 	'rowselect': function(model,rowIndex,record) {
		    	 		parent.fireEvent('select', record);
		    	 	}
		    	 }
		    }),
            listeners: {
                'rowdblclick': function() {
                    	parent.edit();
                },
            	'rowcontextmenu': function(grid, rowIndex, e) {
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
				    		},{
				    			iconCls: 'icon-add-payment',
				    			text: _('Add Payment'),
				    			handler: function() {
									parent.addPayment();
				    			}
				    		}				    						    		
				    	]
				    });
				    listContextMenu.showAt(e.getXY());				            	
            	},
            	'contextmenu': function(e) {
				    e.stopEvent();
				    var listContextMenu = new Ext.menu.Menu({
				    	items: [
				    		{
				    			iconCls: 'icon-add',
				    			text: _('Add'),
				    			handler: function() {
									parent.add()
				    			}
				    		},				    		
				    	]
				    });
				    listContextMenu.showAt(e.getXY());
				},
            }				    
	    });
	    						
	},
	
	load: function() {
		this.reload();
	}
});	