Ext.ns("Portlet");

function expenseDiffRender(value, meta, record, row, col, store) {
	return Ext.util.Format.usMoney(record.data.income - record.data.expense);
}

Ext.apply(Ext.ux.Portlet.prototype, {
	collapsible: false,
});

Portlet.Base = function(config) {
	Ext.apply(this, config);
	Portlet.Base.superclass.constructor.call(this);
};
Ext.extend(Portlet.Base, Ext.Component, {
	bind: function(mod) {
		mod.on("apply", this.doSearch, this);
		mod.portal.add(this.portlet);
		mod.portal.doLayout();
		mod.doApply();
	}			
});

Portlet.MonthGraph = Ext.extend(Portlet.Base, {
	holder: 'monthGraphHolder',
	initComponent: function() {
        this.init();			
	},
	init: function() {
		var h = $.create('div', {'id': this.holder,'style':'width:380px;height:200px'}).insertAfter('#body_content');
		this.form = new Ext.ux.Portlet({
            title: _('Month Curve'),
            height: 250,
            items: [{
            	contentEl: this.holder,
            }]
		});
		this.portlet = {
            width: 400,
            style:'padding: 10px 0 5px 10px',
            items: [this.form]
		};					
	},
	doSearch: function(params) {
		var lMask = new Ext.LoadMask(this.form.el, {msg: _('Processing...'), removeMask: true});
		lMask.show();
		var holder = "#"+this.holder;
		var data = {date: params.date,cat: params.category, subC: params.subCategory, payT: params.paymentType};
		$.getJSON('expense/monthCalc'
			,data
			,function(response) {
		    	$.plot($(holder), [response], {
		    		lines: { show: true },
		    		points: { show: true },
		    		xaxis:
		    			{
		    				mode: "time" ,
		    			 	timeformat: "%d",
		    			}
		    		});
				lMask.hide();					    		
		});
	 }
});
		
Portlet.SixMonthGraph = Ext.extend(Portlet.Base, {
	holder: 'sixMonthGraphHolder',
	initComponent: function() {
        this.init();			
	},
	init: function() {
		var h = $.create('div', {'id': this.holder,'style':'width:380px;height:200px'}).insertAfter('#body_content');
		this.form = new Ext.ux.Portlet({
            title: _('Six Month Curve'),
            height: 250,
            items: [{
            	contentEl: this.holder,
            }]
		});
		this.portlet = {
            width: 400,
            style:'padding: 10px 0 5px 10px',
            items: [this.form]
		};					
	},
	doSearch: function(params) {
		var lMask = new Ext.LoadMask(this.form.el, {msg: _('Processing...'), removeMask: true});
		lMask.show();				
		var holder = "#"+this.holder;
		var data = {date: params.date,cat: params.category, subC: params.subCategory, payT: params.paymentType};
		$.getJSON('expense/sixMonthCalc'
			,data
			,function(response) {
		    	$.plot($(holder), [response], {
		    		lines: { show: true },
		    		points: { show: true },
		    		xaxis:
		    			{
		    				mode: "time" ,
		    			 	timeformat: "%m/%y",
		    			},
		    		yaxis:
		    			{
		    				mode: "number"
		    			}
		    		});
		    	lMask.hide();
		});
	 }			
});
									
Local.Totalizer = function(config) {
	Ext.apply(this, config);
    this.addEvents(
        'apply',
        'clear'
			    );				
   				Local.Totalizer.superclass.constructor.call(this);
			};
			
			Ext.extend(Local.Totalizer, Ext.util.Observable, {
				reload: function(params) {
					this.ds.reload(params);
				},
    			init: function() {
    				var parent = this;
  
  					this.totals = new Ext.form.FieldSet({
			        	title: _('Totals'),
        	autoHeight : true,
        	width: 180,
        	//defaults: { width: 190 },
        	items: [
		        {
                    xtype:'textfield',
                    fieldLabel: _('Total'),
                    id: 'totalField',
                    readOnly: true,
                    value: this.default,
                    cls: 'number_field',
					style: 'margin-left: 15px',
					anchor: '80%'
		        },
		        {
                    xtype:'textfield',
                    fieldLabel: _('Daily Avg'),
                    id: 'avgField',
                    readOnly: true,
                    value: this.default,
                    cls: 'number_field',
                    style: 'margin-left: 15px',
                    anchor: '80%'
		        }				        		
        	]
		});
		
	    this.filter = new Ext.FormPanel({
	    	region: 'west',
	        labelAlign: 'top',
	        frame:true,
	        bodyStyle:'padding-left:5px',
	        collapsible: true,
			title: _('Total'),				        
	        width: 200,
	        items: [
		        {
                    xtype:'ux.monthfield',
                    fieldLabel: _('Period'),
                    id: 'total.month',
                    anchor: '95%',
                    format: 'M/Y',
                    value: new Date(),
                    readOnly: true,
		        },{
					xtype: 'combo',
					fieldLabel: _('Category'),
					id: 'total.categoryId',
					name: 'category.id',
					forceSelection: true,
					triggerAction: 'all',
				   	store: categoryStore,
				   	displayField: 'name',
				   	valueField: 'id',
				   	mode: 'local',
                    anchor: '95%',
                },{
			    	xtype : "subCategoryCombo",
		    		fieldLabel: _('Sub Category'),
		    		id: 'total.subCategoryId',
		    		name: 'subCategory.id',
		    		store: subCategoryStore,
		    		anchor: '95%',
                },{
			    	xtype : "combo",
			    	fieldLabel: _('Payment Type'),
			    	id: 'total.paymentType',
			    	store: paymentTypeStore,
					displayField:'name',
					valueField:'id',
			    	triggerAction:'all',
			    	mode:'local',
			    	forceSelection:true,
			    	anchor: '95%',
			  	} ,               
                this.totals],
	        tbar: new Ext.Toolbar({
	        	cls: 'plain_toolbar',
				items:['->',{
						text: _('Apply'),
						iconCls: 'icon-apply',
						handler: this.doApply.createDelegate(this)
					},{
						text: _('Clear'),
						iconCls: 'icon-clear',
						handler: this.doClear.createDelegate(this)				
					}]					        
	        }),	
	    });
		
		this.on({
			'apply': function(params) {
				var lMask = new Ext.LoadMask(this.totals.el, {msg: _('Processing'), removeMask: true});
    			lMask.show();
				Ext.Ajax.request({
							scope: this,
							url: 'stats/calc', 
				            params: { 
				               date: params.date,
				               cat: params.category,
				               subC: params.subCategory, 
				               payT: params.paymentType
				              },
				              success: function(response){
				            	obj = Ext.util.JSON.decode(response.responseText);
				            	var total = this.totals.findById("totalField");
				            	var avg = this.totals.findById("avgField"); 
				            	if (obj.data) {
				            		total.setValue(Ext.util.Format.usMoney(obj.data.total));
				            		avg.setValue(Ext.util.Format.usMoney(obj.data.avg));
				            	} else {
				            		total.setValue(this.default);
				            		avg.setValue(this.default);
				            	}
				            },
							callback: function ( options, success, response ) { 
								lMask.hide();
							}					            
			   });						
			}
		});

		this.portal = new Ext.ux.Portal({region: 'center'});

		this.panel = new Ext.Panel({
	    	id: 'stats-panel',
			title: _('Stats'),
			iconCls: 'menu-stats',
			layout:'border',
			items: [this.filter, this.portal]
		});				    
	    		    			
	},
	doApply: function() {
		var subC = this.filter.findById('total.subCategoryId');
		if (subC.getRawValue()=="") subC.setValue("");
		var cat = this.filter.findById('total.categoryId');
		if (cat.getRawValue()=="") cat.setValue("");
		var payT = this.filter.findById('total.paymentType');
		if (payT.getRawValue()=="") payT.setValue("");
		var mo = this.filter.findById('total.month');
		this.fireEvent('apply',{'date': Ext.util.Format.date(mo.getValue(), 'd/m/Y')
								,'category': cat.getValue(),
								'subCategory': subC.getValue(),
								'paymentType': payT.getValue()});
	},
	doClear: function() {
		var subC = this.filter.findById('total.subCategoryId');
		var cat = this.filter.findById('total.categoryId');
		var payT = this.filter.findById('total.paymentType');
		var mo = this.filter.findById('total.month');
		mo.setValue(new Date());
		cat.setValue("");
		subC.setValue("");
		payT.setValue("");
		this.fireEvent('clear',{})
		this.doApply();
	},
	load: function(panel) {
		panel.addActive(this.panel);
		this.panel.doLayout(true);
	},	    			    											
});
			
			
Portlet.SixMonthTable = Ext.extend(Portlet.Base, {
	initComponent: function() {
		this.initTable();
        this.init();			
	},
	init: function() {
		this.form = new Ext.ux.Portlet({
            title: _('Six Month Expenses'),
            height: 250,
            items: [this.grid]
		});
		this.portlet = {
            width: 400,
            style:'padding: 10px 0 5px 10px',
            items: [this.form]
		};					
	},
	initTable: function() {

		this.ds = new Ext.data.JsonStore({
		    url: 'stats/sixMonthCalc',
		    root: 'rows',
		    fields: ['date','expense','income'],
		    sortInfo: {field: 'date', direction: 'DESC'},
		    remoteSort: false,
		});
	
	    this.grid = new Ext.grid.GridPanel({
	    	id: 'stats-grid',
			store: this.ds,
			region: 'east',
			collapsible: false,
			height: 300,
	        columns: [
	        	{header: _('Date'), sortable: true,renderer: Ext.util.Format.dateRenderer('M/Y'),dataIndex: 'date',align: 'right'}
	        	,{header: _('Income'), sortable: true, dataIndex: 'income',renderer: Ext.util.Format.usMoney, align: 'right'}
	        	,{header: _('Expense'), sortable: true, dataIndex: 'expense',renderer: Ext.util.Format.usMoney, align: 'right'}
	        	,{header: _('Difference'), sortable: true, dataIndex: 'expense',renderer: expenseDiffRender, align: 'right'}
	        ],
		    viewConfig: {
		        forceFit: true
		    },
	    });
	    
	},
	doSearch: function(params) {
		this.ds.load({params: {date: params.date,cat: params.category, subC: params.subCategory, payT: params.paymentType}});
		/*
		var lMask = new Ext.LoadMask(this.form.el, {msg: _('Processing...'), removeMask: true});
		lMask.show();				
		var holder = "#"+this.holder;
		var data = {date: params.date,cat: params.category, subC: params.subCategory, payT: params.paymentType};
		$.getJSON('expense/sixMonthCalc'
			,data
			,function(response) {
		    	$.plot($(holder), [response], {
		    		lines: { show: true },
		    		points: { show: true },
		    		xaxis:
		    			{
		    				mode: "time" ,
		    			 	timeformat: "%m/%y",
		    			},
		    		yaxis:
		    			{
		    				mode: "number"
		    			}
		    		});
		    	lMask.hide();
		});*/
	 }			
});