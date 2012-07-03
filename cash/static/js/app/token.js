Local.Token = function(config) {
	Ext.apply(this, config);
    this.addEvents(
        'reload'
    );    
	Local.Token.superclass.constructor.call(this);
};

Ext.extend(Local.Token, Ext.util.Observable, {

	reload: function(params) {
		this.ds.reload(params);
	},
	
	remove: function () {
		var parent = this;
		Ext.Msg.confirm(
			_('Sure?'),
			_('Do you really want do delete the current token?'),
			function(response) {
				if('yes' == response) {
                    $.postJSON('token/delete',
                        function(data) {
                            if (data.success) {
                                parent.dataField.setRawValue(_('Token not set'));
                                parent.reload();
                            } else {
                                Ext.Msg.error(data.msg);
                            }
                        },
                        _('Invalidating current Token...')
                    );
				}
			}
		);
	},
	
	create: function() {
        var parent = this;
        $.postJSON('token/create',
            function(data) {
                if (data.success) {
                    parent.dataField.setRawValue(data.response);
                    parent.reload();
                } else {
                    parent.dataField.setRawValue(_('Token not set'));
                    Ext.Msg.error(data.msg);
                }
            },
            _('Generating new Token...')
        );
	},
	
	init: function() {
		var parent = this;
		
		this.ds = new Ext.data.JsonStore({
		    url: 'token/list',
		    root: 'rows',
		    totalProperty:'total',
		    id:'ip',
		    fields: ['ip','date'],
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

        this.dataField = new Ext.form.TextField({
            fieldLabel: _('Token Created'),
            readOnly: true
        });
            
		this.grid = new Ext.grid.GridPanel({
	    	id: 'token-grid',
			store: this.ds,
			region: "center",
			width: 300,			
			title: _('Token Usage History'),
	        columns: [
                {header: _('IP'), width: 50, sortable: true, dataIndex: 'ip'},
	        	{header: _('Last Access'), width: 50, sortable: true, dataIndex: 'date', renderer: Ext.util.Format.dateRenderer('d/m/Y H:i:s')}
	        ],
	        bbar: this.pagingBar,
	        tbar: new Ext.Toolbar({
				items:[ this.dataField,'-',
                        {
						text: _('Create'),
						iconCls: 'icon-add-plus',
						handler: function() {
							parent.create();
						}
					}]					        
	        }),
		    viewConfig: {
		        forceFit: true
		    },
	    });
	    						
	},

    loadCurrent: function() {
        var parent = this;
        $.postJSON('token/get',
            function(data) {
                if (data.created) {
                    parent.dataField.setRawValue(data.created);
                } else {
                    parent.dataField.setRawValue(_('Token not set'));
                }
            }
        );
    },
    
	load: function() {
        this.loadCurrent();
		this.ds.load({params:{start:0, limit: this.pagingBar.pageSize}});
	},
});
