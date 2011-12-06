Local.LoanPayment = function(config) {
	Ext.apply(this, config);
    this.addEvents(
        'update'
    );
	Local.Person.superclass.constructor.call(this);
};

Ext.extend(Local.LoanPayment, Ext.util.Observable, {
	reload: function(params) {
		this.ds.reload(params);
	},
	
	remove: function () {
		var parent = this;
		var record = parent.grid.selModel.getSelected().data;
		Ext.Msg.confirm(
			_('Sure?'),
			String.format(_('Do you really want do delete {0}?'),Ext.util.Format.date(record.date,'d/m/Y')),
			function(response) {
				if('yes' == response) {
					var rid = record.id;
					$.postJSON('payment/delete'
						,{ id: rid }
						,function(response){
							if (response.success) {
								parent.reload();
								parent.fireEvent('update', parent);
							} else {
								Ext.Msg.error(response.msg);
							}
						},
						String.format(_('Deleting {0}...'),Ext.util.Format.date(record.date,'d/m/Y'))
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
	    		name : "loan.id",
				value: parent.loanId,
		  	}, 					
		    {
				xtype : "textfield",
				cls : "x-hide-display",
				hideLabel: true,
	    		name : "id",
				value: record.id,
		  	},    
		    {
		    	xtype : "datefield",
		    	fieldLabel: _('Date'),
		    	name : "date",
		    	value: record.date,
		  	},
		    {
		    	xtype : "numberfield",
		    	fieldLabel: _('Amount'),
		    	id: "payment.amount",
		    	name : "amount",
		    	value: record.amount,
		  	},
		];

		
		var ed = new EditWindow({
			id: 'paymentEd',
			url: 'payment/update',
			title: _('Editing...'),
            width: 330,
            height: 120,
            iconCls: 'icon-edit',	
            focus: 'payment.amount',
            items: items,
            listeners: {
            	'success': function() {
            		parent.reload();
            		parent.fireEvent('update', parent);
            	}
            }								
		});
		ed.show();
	},
	
	add: function() {
		var parent = this;
		if (this.loanId == undefined) {
			var loanStore = new Ext.data.JsonStore({
				url : 'loan/list',
				root : 'rows',
				totalProperty : 'total',
				id : 'id',
				fields : ['id', 'reason'],
				baseParams : {
					sort : 'reason',
					dir : 'ASC'
				}
			});
			
			var loanCombo = new Ext.form.ComboBox({
		    	fieldLabel: _('Loan'),
		    	hiddenName : "loan.id",
		    	id: "loanId",
		    	store: loanStore,
				displayField:'reason',
				valueField:'id',
		    	triggerAction:'all',
		    	forceSelection:true,
		    	mode: 'local',
		    	triggerClass: 'load-combo-trigger'
			});
			
			loanStore.on({
				'load': function() {
					loanCombo.enable();
				}
			});
			
			var personCombo = new Ext.form.ComboBox({
		    	fieldLabel: _('Person'),
		    	hiddenName : "person.id",
		    	store: personStore,
				displayField:'name',
				valueField:'id',
		    	triggerAction:'all',
		    	mode:'local',
		    	forceSelection:true,
		    	listeners: {
		    		'select': function(combo,record,index) {
		    		 	loanCombo.clearValue();
		    		 	loanCombo.clearInvalid();
		    		 	loanCombo.disable();
		    			loanStore.load({params:{'person.id': record.id}});
		    		}
		    	}
			});
		
			var items = [
				personCombo,
				loanCombo
			]
			
			var ed = new EditWindow({
				id: 'loanSelect',
				title: _('Select Loan'),
	            width: 330,
	            height: 120,
	            iconCls: 'icon-select',
	            submitText: _('Ok'),
	            submitIcon: 'icon-apply',
	            items: items,
	            listeners: {
	            	'afterSubmit': function(elem) {
	            		parent.loanId = elem.values['loan.id'];
	            		parent.add(); 
	            	}
	            },
			});
			ed.show();	
		} else {
			var items = [
			    {
					xtype : "textfield",
					cls : "x-hide-display",
					hideLabel: true,
		    		name : "loan.id",
					value: parent.loanId,
			  	}, 					
			    {
			    	xtype : "datefield",
			    	fieldLabel: _('Date'),
			    	id: "payment.date",
			    	name : "date",
			  	},
			    {
			    	xtype : "numberfield",
			    	fieldLabel: _('Amount'),
			    	name : "amount",
			  	}];
    		
			var ed = new EditWindow({
				id: 'paymentAdd',
				url: 'payment/save',
				title: _('Add Payment'),
	            width: 330,
	            height: 120,
	            iconCls: 'icon-add-payment',	
	            focus: 'payment.date',
	            items: items,
	            listeners: {
	            	'success': function() {
	            		parent.reload();
	            		parent.fireEvent('update', parent);
	            	}
	            },
			});
			ed.show();		    		
		}
	},
	
	init: function() {
		var parent = this;
		
		this.ds = new Ext.data.JsonStore({
		    url: 'payment/list',
		    root: 'rows',
		    totalProperty:'total',
		    id:'id',
		    fields: ['id','loan_id','amount','date'],
		    sortInfo: {field: 'date', direction: 'DESC'},
		    remoteSort: true,
		});
	
	    this.pagingBar = new Ext.PagingToolbar({
	        pageSize: 50,
	        store: this.ds,
	        displayInfo: false,
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
	    	id: 'loan-payment-grid',
			store: this.ds,
			title: _('Payments'),
			region: 'east',
			collapsible: true,
			collapsed: true,
			width: 300,
	        columns: [
	        	this.actionsColumn
	        	,{header: _('Date'), sortable: true,renderer: Ext.util.Format.dateRenderer('d/m/Y'),dataIndex: 'date',align: 'right'}
	        	,{header: _('Amount'), sortable: true, dataIndex: 'amount',renderer: Ext.util.Format.usMoney, align: 'right'}
	        ],
	        bbar: this.pagingBar,
	        tbar: new Ext.Toolbar({
				items:[{
						text: _('Add Payment'),
						iconCls: 'icon-add-payment',
						handler: function() {
							parent.add();
						}
					}]					        
	        }),
		    viewConfig: {
		        forceFit: true
		    },
		    plugins: [this.actionsColumn],
            listeners: {
/*			            	'expand': function() {
			            		parent.grid.el.mask(_('Select a Loan from the loans list'),'ext-el-mask-msg');
			            	},
			            	'load': function() {
			            		if (parent.grid.el.isMasked()) parent.grid.el.unmask();
			            	},*/
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
				    			iconCls: 'icon-add-payment',
				    			text: _('Add Payment'),
				    			handler: function() {
									parent.add();
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
				    			iconCls: 'icon-add-payment',
				    			text: _('Add Payment'),
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
	
	load: function(record) {
		this.loanId = record.id;
		this.grid.setTitle(String.format(_('Payments - {0} ({1}) '),record.data.person,record.data.reason));
		this.ds.baseParams = {'loan.id': this.loanId};
		this.ds.load({params:{start:0, limit: this.pagingBar.pageSize}});
	},
});		