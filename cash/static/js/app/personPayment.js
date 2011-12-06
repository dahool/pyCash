function remainingRender(value, meta, record, row, col, store) {
	return Ext.util.Format.usMoney(record.data.balance - record.data.pay);
}

Local.LoanPersonPayment = function(config) {
	Ext.apply(this, config);
    this.addEvents(
        'update'
    );
	Local.LoanPersonPayment.superclass.constructor.call(this);
};

Ext.extend(Local.LoanPersonPayment, Ext.util.Observable, {

	doRefresh: function(s) {
		var p = Ext.getCmp("person_amount");
		var c = Ext.getCmp("person_combo_p");
		if (p.getValue()>0) {
			var sel = s.sm.getSelections();
			exclude = "";
			for (i=0;i<s.sm.getCount();i++) {
				if (exclude!="") exclude = exclude + ";";
				exclude = exclude + sel[i].id 
			}
			var mod = s.store.getModifiedRecords();
			modf = "[";
			for (i=0;i<mod.length;i++) {
				if (!s.sm.isIdSelected(mod[i].id)) {
					if (modf!="[") modf = modf + ","
					modf = modf + "{\"id\": "+ mod[i].id + ",\"value\": "+ mod[i].data.pay +"}";
				}
			}
			modf = modf + "]"
			s.store.load({params:{'exclude': exclude, 'modf': modf,'person.id': c.store.getAt(c.selectedIndex).id, 'amount': p.getValue()}});
		}
		return false;
	},
	
	clear: function(s) {
		var p = Ext.getCmp("person_amount");
		var c = Ext.getCmp("person_combo_p");
		s.store.load({params:{'person.id': c.store.getAt(c.selectedIndex).id, 'amount': p.getValue()}});
		return false;
	},
	
	add: function() {
		this.hinderSelection = false;
		var parent = this;
			
		var ds = new Ext.data.JsonStore({
		    url: 'payment/calc',
		    root: 'rows',
		    id:'id',
		    fields: ['id','reason','date','amount','balance', 'partial','pay','remain','dirty'],
		    pruneModifiedRecords: true
		});
		
		ds.on({
			'load': function(s, rs) {
				s.each(function(r) {
					if (r.data.dirty) {
						r.forceDirty('pay',r.data.pay);
					}
				})
				parent.grid.getView().refresh();
			}
		});
		
		var selModel = new Ext.grid.CheckboxSelectionModel({
			listeners: {
				'beforerowselect': function(o, rowIndex, keepExisting, record) {
					if(parent.hinderSelection) {
						parent.hinderSelection = false;
						return false;
					}
				}
			}
		});

	    parent.grid = new Ext.grid.EditorGridPanel({
	    	id: 'personloan-payment-grid',
	    	frame: true,
	    	width: 550,
	    	height: 200,
			store: ds,
			selModel: selModel,
			clicksToEdit: 1,
	        bbar: new Ext.ux.RefreshToolbar({
	        	leftItems: ['->', {
	        		store: ds,
	                iconCls: "refresh",
	                tooltip: _('Clear'),
	                handler: this.clear.createDelegate(this),
	        	},'-'],
	        	sm: selModel,
	        	store: ds,
	        	listeners: {
	        		'refresh': this.doRefresh
	        	}
	        }),
	        columns: [
	            selModel
	        	,{header: _('Date'), sortable: false,renderer: Ext.util.Format.dateRenderer('d/m/Y'),dataIndex: 'date',align: 'right'}
	        	,{header: _('Reason'), sortable: false, dataIndex: 'reason'}
	        	,{header: _('Balance'), sortable: false, dataIndex: 'balance',renderer: Ext.util.Format.usMoney, align: 'right',summaryType:'sum'}
	        	,{header: _('Monthly amount'), sortable: false, dataIndex: 'partial',renderer: Ext.util.Format.usMoney, align: 'right',summaryType:'sum'}
	        	,{header: _('Pay'), sortable: false, dataIndex: 'pay',renderer: Ext.util.Format.usMoney, align: 'right'
		        	,editor: new Ext.form.NumberField({
		                allowBlank: false,
		                minValue: 0
		            })
	        	,summaryType:'sum'}
	        	,{header: _('Remaining'), sortable: false, dataIndex: 'remain',renderer: remainingRender, align: 'right',summaryType:'sum'}
	        ],
		    viewConfig: {
		        forceFit: true
		    },
		    plugins: [ new Ext.grid.GridSummary() ],
		    listeners: {
		        rowmousedown: function() {
		    		parent.hinderSelection = true;
		        }
		    }
/*		    listeners: {
		    	'rowclick': function(t) {
					var p = Ext.getCmp("person_amount");
					if (p.getValue()>0) {
						var sel = t.selModel.getSelections();
						exclude = "";
						for (i=0;i<t.selModel.getCount();i++) {
							if (exclude!="") exclude = exclude + ";";
							exclude = exclude + sel[i].id 
						}
						ds.load({params:{'exclude': exclude, 'person.id': personCombo.store.getAt(personCombo.selectedIndex).id, 'amount': p.getValue()}});
					}
		    	}
		    }*/
	    });
	    
		var personCombo = new Ext.form.ComboBox({
			id: 'person_combo_p',
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
					var p = Ext.getCmp("person_amount");
					if (p.getValue()>0) {
						ds.rejectChanges();
						ds.load({params:{'person.id': record.id, 'amount': p.getValue()}});
					}
	    		}
	    	}
		});
		
		var items = [
					personCombo,
				    {
						columnWidth: .25,
				    	xtype : "numberfield",
				    	fieldLabel: _('Amount'),
				    	id: "person_amount",
				    	name : "amount",
				    	value: "0.00",
				    	listeners: {
							'specialkey': function(t, e) {
								if (e.getKey()==Ext.EventObject.ENTER) {
									if (personCombo.selectedIndex>-1) {
										ds.rejectChanges();
										ds.load({params:{'person.id': personCombo.store.getAt(personCombo.selectedIndex).id, 'amount': t.getValue()}});
									}
								}
							},
							/*'blur': function(t) {
								if (personCombo.selectedIndex>-1) {
									ds.load({params:{'person.id': personCombo.store.getAt(personCombo.selectedIndex).id, 'amount': t.getValue()}});
								}
							}*/
						}
				    },
					{
		            	 layout: 'anchor',
		            	 width: 550,
		            	 items: [ 
		            	    parent.grid
						]
					}
		]
			
		var ed = new EditWindow({
			id: 'loanPersonSelect',
			title: _('Add Payment'),
            width: 600,
            height: 330,
            iconCls: 'icon-add-payment',
            items: items,
            focus: 'person_combo_p',
            listeners: {
				'onSubmit': function() {
					setStatus(true, _('Saving...'));
					ds.each(function(rec) {
						if (rec.data.pay > 0) {
						    data = {"loan.id": rec.id,"amount": rec.data.pay,"date": Ext.util.Format.date(new Date(), "d/m/Y")}
							$.post("payment/save", data, function() {
								/*if (response.msg) {
									setStatus(false, response.msg);
								}*/								
							}, "json");
						}
					})
					setStatus(false);
					parent.fireEvent('update');
				}
			}
		});
		ed.show();	
	},
	
	init: function() { }
	
});		