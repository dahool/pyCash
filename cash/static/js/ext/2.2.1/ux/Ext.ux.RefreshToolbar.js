Ext.ns('Ext.ux');

Ext.ux.RefreshToolbar = Ext.extend(Ext.Toolbar, {
	refreshText : "Refresh",
    initComponent : function(){
        Ext.ux.RefreshToolbar.superclass.initComponent.call(this);
        this.bind(this.store);
    },
    addAll: function(elm) {
    	for (var i=0;i<elm.length;i++) {
    		this.add(elm[i]);
    	}
    },
    onRender : function(ct, position) {
    	Ext.ux.RefreshToolbar.superclass.onRender.call(this, ct, position);
    	if (this.leftItems) {
    		this.addAll(this.leftItems);
    	}
        this.loading = this.addButton({
            tooltip: this.refreshText,
            iconCls: "x-tbar-loading",
            handler: this.doRefresh.createDelegate(this)
        });
    	if (this.rightItems) {
    		this.addAll(this.rightItems);
    	}
    },
	onLoad : function(store, r, o) {
        if(!this.rendered){
            return;
        }
        this.loading.enable();
    },
	beforeLoad : function() {
    	if(this.rendered && this.loading){
            this.loading.disable();
        }
    },
	onLoadError : function(){
        if(!this.rendered){
            return;
        }
        this.loading.enable();
    },    
    doRefresh: function() {
    	if(this.fireEvent("refresh", this) !== false){
    		this.store.reload();
    	}
    },
    bind: function(store){
        store = Ext.StoreMgr.lookup(store);
        store.on("beforeload", this.beforeLoad, this);
        store.on("load", this.onLoad, this);
        store.on("loadexception", this.onLoadError, this);
        this.store = store;
    }    
})