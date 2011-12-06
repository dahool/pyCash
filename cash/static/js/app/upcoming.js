Local.TaxUpcoming = function(config) {
			Ext.apply(this, config);
			Local.TaxUpcoming.superclass.constructor.call(this);
		};
		
		Ext.extend(Local.TaxUpcoming, Ext.util.Observable, {
			reload: function() {
				this.ds.reload();
			},
			pay: function() {
				var parent = this;
    			var record = this.grid.selModel.getSelected().data;

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
			init: function() {
				var parent = this;
				
				this.ds = new Ext.data.JsonStore({
				    url: 'tax/upcomingList',
				    root: 'rows',
				    totalProperty:'total',
				    id:'id',
				    fields: ['id','service','expire','amount','nextExpire'],
				    listeners: {
				    	'load': function(store, records, opt) {
				    		if (store.getTotalCount()==0) {
				    			parent.panel.setTitle(String.format(_('Upcoming ({0})'),'0'));
				    			if (!parent.grid.el.isMasked())
				    				parent.grid.el.mask(_('Nothing to list'),'ext-el-mask-msg');
				    		} else {
								parent.panel.setTitle(String.format(_('Upcoming ({0})'),store.getTotalCount()));
				    			if (parent.grid.el.isMasked()) parent.grid.el.unmask();
				    		}
				    	}
				    }
				});    					

			 	var actions = new Ext.ux.grid.RowActions({
					actions:[
						{
			    			iconCls: 'icon-pay',
			    			tooltip: _('Pay'),
			    		}
					],
					callbacks: {
						'icon-pay': function() {
							parent.pay();
						}
					}
				});
				
			    this.grid = new Ext.grid.GridPanel({
			    	enableHdMenu: false,
					store: this.ds,
					border: false,
					loadMask: false,
					style: 'margin-left: '+(($(document).width() - 400) / 2)+'px',
					width: 400,
					height: 400,
			        columns: [
			        	actions,
			        	{id: 'service', header: _('Service'), sortable: false, dataIndex: 'service'},
			        	{header: _('Amount'), width: 100, sortable: false, dataIndex: 'amount',renderer: Ext.util.Format.usMoney, align: 'right'},
			        	{header: _('Expire date'), width: 100, sortable: false, dataIndex: 'expire',renderer: Ext.util.Format.dateRenderer('d/m/Y'), align: 'right'},
			        ],
					autoExpandColumn: 'service',
			        tbar: new Ext.ux.RefreshToolbar({
			        	leftItems: ['->'],
			        	store: this.ds
			        }),
			        plugins: [actions],
			        listeners: {
			        	'rowdblclick': function(grid, rowIndex, e) {
			        		parent.pay();
			        	}
			        }
			    });
				this.grid.render('grid-container');
				
				this.panel = new Ext.Panel({
					id: 'upcoming-panel',
					title: _('Upcoming'),
			    	iconCls : 'menu-upcoming',
					contentEl: 'grid-container',
					listeners: {
						'activate': function(p) {
							parent.ds.load();
						} 
					}
				})
			},
			load: function(tab) {
				var parent = this;
				tab.replaceActive(this.panel);
				//this.ds.load();
				/*
				var task = {
				    run: function(){
				        parent.ds.reload();
				    },
				    interval: 5000 
				}
				var runner = new Ext.util.TaskRunner();
				runner.start(task);*/
			}
		});