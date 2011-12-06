Local.Person = function(config) {
	Ext.apply(this, config);
	Local.Person.superclass.constructor.call(this);
};

Ext.extend(Local.Person, Ext.util.Observable, {
	reload: function(params) {
		this.ds.reload(params);
		loadStore(personStore, true);
	},
	
	remove: function () {
		var parent = this;
		var record = parent.grid.selModel.getSelected().data;
		Ext.Msg.confirm(
			_('Sure?'),
			String.format(_('Do you really want do delete {0}?'),record.name),
			function(response) {
				if('yes' == response) {
					var rid = record.id;
					$.postJSON('person/delete'
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
		    	xtype : "textfield",
		    	fieldLabel: _('Name'),
		    	name : "name",
		    	id: "name",
		    	value: record.name,
			}
		];

		
		var ed = new EditWindow({
			id: 'personEd',
			url: 'person/update',
			title: _('Editing...'),
            width: 330,
            height: 120,
            iconCls: 'icon-edit',	
            focus: 'name',
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
		    	fieldLabel: _('Name'), 
		    	xtype : "textfield",
		    	name : "name",
		    	id: "name",
		  	}];
		
		var ed = new EditWindow({
			id: 'personAdd',
			url: 'person/save',
			title: _('Add Person'),
            width: 330,
            height: 120,
            iconCls: 'icon-add',	
            focus: 'name',
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
		
		this.ds = new Ext.data.JsonStore({
		    url: 'person/list',
		    root: 'rows',
		    totalProperty:'total',
		    id:'id',
		    fields: ['id','name'],
		    sortInfo: {field: 'name', direction: 'ASC'},
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
	    	id: 'person-grid',
			store: this.ds,
			region: "west",
			collapsible: true,
			collapsed: true,
			width: 300,			
			title: _('Persons'),
	        columns: [
	        	this.actionsColumn,
	        	{header: _('Name'), width: 50, sortable: true, dataIndex: 'name'}
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
		this.ds.load({params:{start:0, limit: this.pagingBar.pageSize}});
	},
});