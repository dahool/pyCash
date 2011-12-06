/* --- COMON STORES - COMBOS --- */
function loadStore(store, force) {
	if (!store.isLoaded) {
		store.load();
	} else if (force) {
		store.reload();
	}
};

var categoryStore = new Ext.data.JsonStore({
	isLoaded : false,
	url : 'category/list',
	root : 'rows',
	totalProperty : 'total',
	id : 'id',
	fields : ['id', 'name'],
	baseParams : {
		sort : 'name',
		dir : 'ASC'
	},
	listeners : {
		'beforeload' : function() {
			this.isLoaded = true;
		}
	}
});

var personStore = new Ext.data.JsonStore({
	isLoaded : false,
	url : 'person/list',
	root : 'rows',
	totalProperty : 'total',
	id : 'id',
	fields : ['id', 'name'],
	baseParams : {
		sort : 'name',
		dir : 'ASC'
	},
	listeners : {
		'beforeload' : function() {
			this.isLoaded = true;
		}
	}
});

var subCategoryStore = new Ext.data.JsonStore({
	isLoaded : false,
	url : 'subCategory/list',
	root : 'rows',
	id: 'id',
	fields : ['id', 'name', 'category', 'categoryId'],
	baseParams : {
		sort : 'name',
		dir : 'ASC'
	},
	listeners : {
		'beforeload' : function() {
			this.isLoaded = true;
		}
	}
});

var paymentTypeStore = new Ext.data.JsonStore({
	isLoaded : false,
	url : 'paymentType/list',
	root : 'rows',
	totalProperty : 'total',
	id : 'id',
	fields : ['id', 'name'],
	baseParams : {
		sort : 'name',
		dir : 'ASC'
	},
	listeners : {
		'beforeload' : function() {
			this.isLoaded = true;
		}
	}
});

var cardStore = new Ext.data.JsonStore({
	isLoaded : false,
	url : 'card/list',
	root : 'rows',
	totalProperty : 'total',
	id : 'id',
	fields : ['id', 'name'],
	baseParams : {
		sort : 'name',
		dir : 'ASC'
	},
	listeners : {
		'beforeload' : function() {
			this.isLoaded = true;
		}
	}
});

var cardDatesStore = new Ext.data.JsonStore({
	isLoaded : false,
	url : 'cardDates/list',
	root : 'rows',
	totalProperty : 'total',
	id : 'id',
	fields : ['id', 'name'],
	baseParams : {
		sort : 'name',
		dir : 'ASC'
	},
	listeners : {
		'beforeload' : function() {
			this.isLoaded = true;
		}
	}
});