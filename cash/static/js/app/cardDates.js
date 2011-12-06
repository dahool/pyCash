Local.CardDates = function(config) {
		Ext.apply(this, config);
		Local.CardDates.superclass.constructor.call(this);
	};
	
Ext.extend(Local.CardDates, Ext.util.Observable, {
	reload: function(params) {
		this.ds.reload(params);
		loadStore(cardDatesStore, true);
	},
	
	remove: function () {
		var parent = this;
		var record = parent.grid.selModel.getSelected().data;
		Ext.Msg.confirm(
			_('Sure?'),
			String.format(_('Do you really want do delete <b>{0} ({1}-{2})</b>?'),record.card,Ext.util.Format.date(record.closeDate,'d/m/Y'),Ext.util.Format.date(record.expireDate,'d/m/Y')),
			function(response) {
				if('yes' == response) {
					var rid = record.id;
					$.postJSON('cardDates/delete'
						,{ id: rid }
						,function(response){
							if (response.success) {
								parent.reload();
							} else {
								Ext.Msg.error(response.msg);
							}
						},
						String.format(_('Deleting <b>{0} ({1}-{2})</b>...'),record.card,Ext.util.Format.date(record.closeDate,'d/m/Y'),Ext.util.Format.date(record.expireDate,'d/m/Y'))
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
		    	fieldLabel: _('Card'),
		    	hiddenName : "card.id",
		    	store: cardStore,
				displayField: 'name',
				valueField: 'id',
		    	triggerAction:'all',
		    	mode:'local',
		    	forceSelection:true,
		    	value: record.card_id,
		  	},
		  	{
		    	xtype : "datefield",
		    	fieldLabel: _('Close Date'),
		    	name : "closeDate",
		    	value: record.closeDate,
		    	id: "closeDate",
		  	},
		    {
		    	xtype : "datefield",
		    	fieldLabel: _('Expire Date'),
                cmpField: 'closeDate',  	
		    	name : "expireDate",
		    	value: record.expireDate,
		  	},		  	
		];

		
		var ed = new EditWindow({
			id: 'cardDatesEd',
			url: 'cardDates/update',
			title: _('Editing...'),
            width: 330,
            height: 150,
            iconCls: 'icon-edit',	
            focus: 'closeDate',
            items: items,
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
		    	fieldLabel: _('Card'),
		    	hiddenName : "card.id",
		    	store: cardStore,
				displayField: 'name',
				valueField: 'id',
		    	triggerAction:'all',
		    	mode:'local',
		    	forceSelection:true,
		    	id: "card_id",
		  	},
		  	{
		    	xtype : "datefield",
		    	fieldLabel: _('Close Date'),
		    	name : "closeDate",
		    	id: "closeDate",
		  	},
		    {
		    	xtype : "datefield",
		    	fieldLabel: _('Expire Date'),
                vtype: 'range',
                cmpField: 'closeDate',  	
		    	name : "expireDate",
		  	}];
		
		var ed = new EditWindow({
			id: 'cardDatesAdd',
			url: 'cardDates/save',
			title: _('Add'),
            width: 330,
            height: 150,
            iconCls: 'icon-add',	
            focus: 'card_id',
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
		
		this.ds = new Ext.ux.data.JsonGroupingStore({
		    url: 'cardDates/list',
		    root: 'rows',
		    totalProperty:'total',
		    id:'id',
		    fields: ['id','card','card_id','expireDate','closeDate'],
		    sortInfo: {field: 'closeDate', direction: 'DESC'},
		    remoteSort: true,
		    remoteGroup: false,
		    groupField: 'card'
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
	    	id: 'carddate-grid',
	    	region: 'center',
	    	iconCls : 'menu-item',
			store: this.ds,
			title: _('Expires'),
	        columns: [
	        	this.actionsColumn,
	        	{header: _('Card'), width: 50, sortable: true, dataIndex: 'card'},
	        	{header: _('Close Date'), width: 50, sortable: true, renderer: Ext.util.Format.dateRenderer('d/m/Y'), dataIndex: 'closeDate'},
	        	{header: _('Expire Date'), width: 50, sortable: true, renderer: Ext.util.Format.dateRenderer('d/m/Y'), dataIndex: 'expireDate'}
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
	        view: new Ext.grid.GroupingView({
	            forceFit: true,
	            groupTextTpl: '{text} ({[values.rs.length]} {[values.rs.length > 1 ? "'+_('Items')+'" : "'+_('Item')+'"]})'
	        }),
		    plugins: [this.actionsColumn],
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