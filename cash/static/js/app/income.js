Local.Income = function(config) {
	Ext.apply(this, config);
    this.addEvents(
        'reload'
    );				
	Local.Income.superclass.constructor.call(this);
};

Ext.extend(Local.Income, Ext.util.Observable, {
	reload: function(params) {
		this.ds.reload(params);
	},
	remove: function() {
		var parent = this;
		var record = parent.grid.selModel.getSelected().data;
		Ext.Msg.confirm(
			_('Sure?'),
			String.format(_('Do you really want to delete Income for period {0}?'),Ext.util.Format.date(record.period,'M/Y')),
			function(response) {
				if('yes' == response) {
					var rid = record.id;
					$.postJSON('income/delete'
						,{ id: rid }
						,function(response){
							if (response.success) {
								parent.reload();
							} else {
								Ext.Msg.error(response.msg);
							}
						},
						String.format(_('Deleting {0}...'),Ext.util.Format.date(record.period,'M/Y'))
					);											
				}
			}
		);
	},
	
	edit: function() {
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
                    xtype:'ux.monthfield',
                    fieldLabel: _('Period'),
                    name: 'period',
                    format: 'M/Y',
                    value: record.period,
                    anchor: '90%',
                    readOnly: true,
                    submitFormat: 'd/m/Y'
			  	},
			    {
                    xtype:'numberfield',
                    fieldLabel: _('Amount'),
                    name: 'amount',
                    id: 'income.amount',
                    value: record.amount,
                    anchor: '90%'
			  	}]
	
		var ed = new EditWindow({
			id: 'incomeAdd',
			url: 'income/update',
			title: _('Editing...'),
            height: 120,
            width: 320,
            iconCls: 'icon-edit',	
            focus: 'income.amount',
            items: items,
            listeners: {
            	'success': function() {
            		parent.reload();
            	}
            }				            								
		});
		ed.show();
	},
	
	add: function(){
		var parent = this;
		var today = new Date();
		var initialDt = new Date(today.getFullYear(), today.getMonth()+1, 1);

		var items = [
			    {
                    xtype:'ux.monthfield',
                    fieldLabel: _('Period'),
                    id: 'income.period',
                    name: 'period',
                    format: 'M/Y',
                    value: initialDt,
                    anchor: '90%',
                    readOnly: true,
                    submitFormat: 'd/m/Y'
			  	},
			    {
                    xtype:'numberfield',
                    fieldLabel: _('Amount'),
                    name: 'amount',
                    anchor: '90%'
			  	}]
	
		var ed = new EditWindow({
			id: 'incomeAdd',
			url: 'income/save',
			title: _('Add Income'),
            height: 120,
            width: 320,
            iconCls: 'icon-add',	
            focus: 'income.period',
            items: items,
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

		this.ds = new Ext.ux.data.JsonGroupingStore({
		    url: 'income/list',
		    root: 'rows',
		    totalProperty:'total',
		    id:'id',
		    fields: ['id','period','amount'],
		    sortInfo: {field: 'period', direction: 'DESC'},
		    remoteSort: true,
		    listeners: {
		    	'load': function() {
					parent.fireEvent('reload');
		    	}
		    },
		    groupField: 'period',
		    remoteGroup: false,		    
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
			actions:[{
					iconCls:'icon-edit',
					tooltip: _('Edit')
				},{
				iconCls:'icon-delete',
				tooltip: _('Delete')		
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
	    	id: 'income-grid',
	    	region:'center',
			store: this.ds,
			title: _('Incomes'),
	        columns: [
	        	this.actionsColumn,
	        	{header: _('Period'), width: 30, sortable: true,renderer: Ext.util.Format.dateRenderer('M/Y'),dataIndex: 'period',align: 'right'}
	        	,{header: _('Amount'), width: 30, sortable: true, dataIndex: 'amount',renderer: Ext.util.Format.usMoney, align: 'right',summaryType:'sum'}
	        ],
	        view: new Ext.grid.GroupingView({
	            forceFit: true,
	            groupTextTpl: '{text} ({[values.rs.length]} {[values.rs.length > 1 ? "'+_('Loans')+'" : "'+_('Loan')+'"]})'
	        }),
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
	        plugins: [this.actionsColumn, new Ext.grid.GroupSummary()],
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
				    		},				    						    		
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
		this.ds.load({params:{start:0, limit: this.pagingBar.pageSize}});
	},	    			    											
});

Local.IncomeLeftPanel = function(config) {
	Ext.apply(this, config);
	Local.IncomeLeftPanel.superclass.constructor.call(this);
};

Ext.extend(Local.IncomeLeftPanel, Ext.util.Observable, {
	holder: 'incomeGraphHolder',
	loaded: false,
	init: function() {
		var parent = this;
		
		var h = $.create('div', {'id': this.holder,'style':'margin-left:50px;width:500px;height:200px'}).insertAfter('#body_content');
		
	    this.form = new Ext.FormPanel({
			id: 'income-left-panel',
	    	region:'north',
	    	collapsible: true,
			collapsed: true,				    	
	        labelAlign: 'top',
	        frame:true,
	        title: _('Incomes'),
	        height: 250,
	        items:[{
	        	contentEl: this.holder
	        }],
	        listeners: {
	         	'beforeexpand': function() {
	         		if (!parent.loaded) parent.update();
	         	},
	         	'activate': function() {
	         		if (!parent.loaded) parent.update();
	         	}
	        }
	    });
	},
	update: function() {
		if (this.form.isVisible()) {
			var lMask = new Ext.LoadMask(this.form.el, {msg: _('Processing...'), removeMask: true});
			lMask.show();
		}
		var holder = "#"+this.holder;
		$.getJSON('income/stats'
			,function(response) {
		    	$.plot($(holder), [response], {
		    		lines: { show: true },
		    		points: { show: true },
		    		xaxis:
		    			{
		    				mode: "time" ,
		    			 	timeformat: "%m/%y",
		    			}
		    		});
		    	this.loaded = true;
				if (lMask) lMask.hide();					    		
		});
	}
});