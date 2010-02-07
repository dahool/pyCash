Ext.ns("Ext.ux.form");

Ext.ux.form.DateFieldTrigger = function(config) {
	Ext.apply(this, config);
	Ext.ux.form.DateFieldTrigger.superclass.constructor.call(this);
};

Ext.extend(Ext.ux.form.DateFieldTrigger, Ext.util.Observable, {
	init: function(dateField) {
		dateField.enableKeyEvents=true;
		dateField.addListener('keydown',this.onKeyPress); 
	},
	onKeyPress: function(field, e) {
		if (e.getKey() == Ext.EventObject.SPACE) {
		 	e.stopEvent();
		 	field.onTriggerClick();
		} else if (e.getKey() == Ext.EventObject.RETURN) {
			if (""==field.getValue()) field.setValue(new Date());
		}
	},
});