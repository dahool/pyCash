function _(str) {
	return str;
}

Ext.apply(Ext.grid.GridPanel.prototype, {
	loadMask: true
});

Ext.apply(Ext.grid.GridPanel.prototype, {
	loadMask: true
});

Ext.override(Ext.Window,{
    getKeyMap : function(){
        if(!this.keyMap){
            this.keyMap = new Ext.KeyMap(this.el, this.keys);
            this.keyMap.stopEvent=true;
        }
    	return this.keyMap;
	}
});

Ext.apply(Ext.form.DateField.prototype, {
	cls: 'date_field',
	format: 'd/m/Y',
	//altFormats : "m/d/Y|n/j/Y|n/j/y|m/j/y|n/d/y|m/j/Y|n/d/Y|m-d-y|m-d-Y|m/d|m-d|md|mdy|mdY|d|Y-m-d|Y/m/d",
	altFormats : "d/m/Y|d/m/y|Y/m/d",
	plugins: [ new Ext.ux.form.DateFieldTrigger() ]
});

Ext.apply(Ext.form.NumberField.prototype, {
	style: 'text-align: right;'
});

ExtTabPanel = function(config) {
    Ext.apply(this, config);
    ExtTabPanel.superclass.constructor.call(this);
};

Ext.extend(ExtTabPanel, Ext.TabPanel, {
	replaceActive: function(cmp) {
		this.remove(this.getActiveTab());
		this.addActive(cmp,false);
	},
	addActive: function(cmp, closable) {
		if (closable==undefined) closable = true;
		cmp.closable = closable;
		this.add(cmp);
		this.setActiveTab(cmp);
/*		cmp.on({
			'beforedestroy': function(panel) {
				console.log(panel);
				panel.closeWindows();
			}
		})*/		
	}	
});		

var subCategoryTpl = new Ext.XTemplate(
	'<tpl for=".">','<div class="x-combo-list-item">{name} ({category})</div>','</tpl>'
);

SubCategoryComboBox = Ext.extend(Ext.form.ComboBox, {
	hiddenName : "subCategory.id",
	displayField:'name',
	valueField:'id',
	triggerAction:'all',
	mode:'local',
	forceSelection:true,
	tpl: subCategoryTpl
});
Ext.reg('subCategoryCombo', SubCategoryComboBox);

Ext.ns('Ext.ux.layout');

Ext.ux.layout.CenterLayout = Ext.extend(Ext.layout.FitLayout, {
    setItemSize : function(item, size){
        this.container.addClass('ux-layout-center');
        item.addClass('ux-layout-center-item');
        if(item && size.height > 0){
            if(item.width){
                size.width = item.width;
            }
            item.setSize(size);
        }
    }
});
Ext.Container.LAYOUTS['ux.center'] = Ext.ux.layout.CenterLayout;

function getReaderProperty(store, property) {
	return store.reader.jsonData[property];	
}

Ext.apply(Ext.data.Record.prototype, {
	forceDirty: function(name, value) {
	    this.dirty = true;
	    if(!this.modified){
	        this.modified = {};
	    }
	    if(typeof this.modified[name] == 'undefined'){
	        this.modified[name] = this.data[name];
	    }
	    this.data[name] = value;
	    if(!this.editing && this.store){
	        this.store.afterEdit(this);
	    }	
	}
});