Ext.apply(Ext.data.Store.prototype, {
    load : function(options){
        options = options || {};
        if(this.fireEvent("beforeload", this, options) !== false){
            this.storeOptions(options);
            var p = Ext.apply(options.params || {}, this.baseParams);
            if(this.sortInfo && this.remoteSort){
                var pn = this.paramNames;
                if (this.sortInfo.sortField==undefined) {
                	this.sortInfo.sortField = this.sortInfo.field;
                }
                p[pn["sort"]] = this.sortInfo.sortField;
                p[pn["dir"]] = this.sortInfo.direction;
            }
            this.proxy.load(p, this.reader, this.loadRecords, this, options);
            this.proxy.on({
            	'loadexception': function(obj,opt,response,e) {
            		res = Ext.util.JSON.decode(response.responseText);
            		if (res.target!=undefined) {
           				window.location = res.target;
           				return false;
            		}
            	}
            });
            return true;
        } else {
          return false;
        }
    },
    sort : function(fieldName, dir){
        var f = this.fields.get(fieldName);
        if(!f){
            return false;
        }
        if(!dir){
            if(this.sortInfo && this.sortInfo.field == f.name){
            	dir = (this.sortToggle[f.name] || "ASC").toggle("ASC", "DESC");
            }else{
                dir = f.sortDir;
            }
        }
        var st = (this.sortToggle) ? this.sortToggle[f.name] : null;
        var si = (this.sortInfo) ? this.sortInfo : null;

        this.sortToggle[f.name] = dir;
        
        var fname;
        if (f.sortField) {
        	fname = f.sortField;
        } else if (!f.mapping) {
        	fname = f.name;	
        } else {
        	fname = f.mapping;
        }
        this.sortInfo = {field: f.name, direction: dir, sortField: fname};
        
        if(!this.remoteSort){
            this.applySort();
            this.fireEvent("datachanged", this);
        }else{
            if (!this.load(this.lastOptions)) {
                if (st) {
                    this.sortToggle[f.name] = st;
                }
                if (si) {
                    this.sortInfo = si;
                }
            }
        }
    }
});

Ext.extend(Ext.ux.data.JsonGroupingStore, Ext.data.GroupingStore, {
    load : function(options) {
        options = options || {};
        if(this.fireEvent("beforeload", this, options) !== false) {
			this.storeOptions(options);
			var p = Ext.apply(options.params || {}, this.baseParams);
			if(this.sortInfo && this.remoteSort) {
    			var pn = this.paramNames;
    		    if (this.sortInfo.sortField==undefined) {
    		    	this.sortInfo.sortField = this.sortInfo.field;
    		    }
    			p[pn["sort"]] = this.sortInfo.sortField;
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