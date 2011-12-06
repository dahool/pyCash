Ext.namespace('Ext.ux.data');
 
Ext.ux.data.JsonGroupingStore = function(c) {
	Ext.ux.data.JsonGroupingStore.superclass.constructor.call(this, Ext.apply(c, {
		reader: (!c.reader && c.fields) ? new Ext.data.JsonReader(c, c.fields) : c.reader
	}));
};
		
Ext.extend(Ext.ux.data.JsonGroupingStore, Ext.data.GroupingStore, {
    load : function(options) {
        options = options || {};
        if(this.fireEvent("beforeload", this, options) !== false) {
			this.storeOptions(options);
			var p = Ext.apply(options.params || {}, this.baseParams);
			if(this.sortInfo && this.remoteSort) {
    			var pn = this.paramNames;
    			p[pn["sort"]] = this.sortInfo.field;
    			p[pn["dir"]] = this.sortInfo.direction;
			}
			if (this.remoteSort) {
				p["groupBy"] = this.groupField;
    		}
    		this.proxy.load(p, this.reader, this.loadRecords, this, options);
    		return true;
		} else {
  			return false;
		}
	}
});