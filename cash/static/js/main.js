/* ----- COMMON ------ */

$.postJSON = function(url, data, callback, text) {
	if (jQuery.isFunction(data)) {
		callback = data;
		data = {};
	}
	if (text == undefined) text = _('Please wait...');
	setStatus(true, text);
	$.post(url, data, function(response) {
		if (response.msg) {
			setStatus(false, response.msg);
		} else {
			setStatus(false);
		}
		callback(response);
	}, "json");
};

function getPageSizeList() {
	return [25, 50, 75, 100, 150, 200, 500, 1000];
}

function forceValidation(form) {
	var items = form.items.items;
	for (var i = 0; i < items.length; i++) {
		items[i].validate();
	}
}

function setStatus(busy, text) {
	if (busy == undefined)
		busy = true;

	if (text == undefined) {
		if (busy)
			mainStatusBar.showBusy();
		else
			mainStatusBar.clearStatus({
				useDefaults : true
			});
	} else {
		if (busy)
			mainStatusBar.showBusy(text);
		else {
			mainStatusBar.clearStatus();
			mainStatusBar.setStatus({
				text : text
			});
		}
	}
}

function loadPage(url, id) {
	var tab = false;
	if (id != undefined)
		tab = mainTabPanel.getComponent(id);
	if (!tab) {
		setStatus() // buzy
		$('#body_content').load(url,
				function(responseText, textStatus, XMLHttpRequest) {
					setStatus(false)
				})
	} else {
		mainTabPanel.setActiveTab(tab);
	}
}

EditWindow = function(config) {
	Ext.apply(this, config, {
		width : 390,
		height : 200,
		labelWidth : 70,
		defaultSubmit : true,
		closeOnSubmit : true
	});
	this.addEvents('beforeSubmit','success', 'afterSubmit', 'failure','cancel','onSubmit');
	EditWindow.superclass.constructor.call(this);
};

Ext.extend(EditWindow, Ext.util.Observable, {
	destroy : function() {
		if (this.current)
			this.current.destroy();
	},
	setFocus : function(id) {
		var el = this.edForm.findById(id);
		if (el != null)
			el.focus(false, true);
	},
	submit : function(edForm) {
		var parent = this;
		parent.fireEvent('onSubmit', this);
		if (edForm.getForm().isValid()) {
			parent.fireEvent('beforeSubmit', this);
			this.values = edForm.getForm().getValues();
			if (this.url != undefined) {
				setStatus(true, _('Saving...'));
				edForm.getForm().submit({
					method : 'POST',
					waitTitle : _('Saving...'),
					waitMsg : _('Saving...'),
					success : function(form, action) {
						parent.fireEvent('success', this);
						if (parent.closeOnSubmit) {
							parent.current.close();
						}
						obj = Ext.util.JSON.decode(action.response.responseText);
						if (obj.msg) {
							setStatus(false, obj.msg);
						} else {
							setStatus(false);
						}
					},
					failure : function(form, action) {
						parent.fireEvent('failure', this);
						setStatus(false);
						if (action.failureType == 'server') {
							Ext.Msg.warn(String.format(_('Server unreachable: [{0}]'),action.response.responseText));
						} else {
							if (action.response != undefined) {
								obj = Ext.util.JSON
										.decode(action.response.responseText);
								setStatus(false, obj.msg);
								Ext.Msg.error(obj.msg);
							}
						}
					}
				});				
			} else {
				if (parent.closeOnSubmit) {
					parent.current.close();
				}				
			}
			parent.fireEvent('afterSubmit', this);
		}
	},
	show : function() {
		var winname = 'ed_' + this.id;
		var win = Ext.get(winname);
		var parent = this;
		if (!win) {
			this.edForm = new Ext.form.FormPanel({
				url : this.url,
				waitMsgTarget : true,
				frame : true,
				height : this.height,
				autoWidth : true,
				items : [{
					xtype : "fieldset",
					autoHeight : true,
					labelWidth : this.labelWidth,
					defaults : {
						msgTarget : 'side',
						width : 180,
						maxLength : 255,
						allowBlank : false,
						selectOnFocus : true,
						enableKeyEvents : true,
						validationEvent : 'keydown',
						listeners : {
							keypress : function(field, e) {
								if (e.getKey() == Ext.EventObject.RETURN) {
									var comboTest = new RegExp("/combo/");
									if (comboTest.test(field.getXTypes())
											&& field.forceSelection
											&& field.getValue() == ""
											&& !field.allowBlank) {
										field.reset();
										field.onTriggerClick();
									} else if (field.submit) {
										parent.submit(parent.edForm);
									} else {
										var items = parent.edForm.form.items.items;
										for (var i = 0; i < items.length; i++) {
											if (items[i].id == field.id) {
												if (i == items.length - 1) {
													if (parent.defaultSubmit) {
														parent
																.submit(parent.edForm);
													}
												} else {
													if (items[i].validate()) {
														items[i + 1].focus();
													}
													break;
												}
											}
										}
									}
								}
							}
						}
					},
					items : this.items
				}],
				tbar : [{
					xtype : 'button',
					text : this.submitText || _('Save'),
					iconCls : this.submitIcon || 'icon-save',
					formBind : true,
					handler : function() {
						parent.submit(parent.edForm);
					}
				}, {
					text : this.cancelText || _('Cancel'),
					iconCls : this.cancelIcon || 'icon-cancel',
					handler : function() {
						parent.current.close();
					}
				}]
			});

			win = new Ext.Window({
				id : winname,
				title : this.title,
				width : this.width,
				minWidth : this.width,
				minHeight : this.height,
				iconCls : this.iconCls,
				resizable : false,
				maximizable : false,
				items : this.edForm,
				listeners : {
					'show' : function() {
						if (parent.focus != undefined)
							parent.setFocus(parent.focus);
					},
					'beforeclose' : function() {
						parent.fireEvent('close');
					}
				}
			});
			this.current = win;
		}
		win.show();
	}
});

Ext.apply(Ext.Msg, {
	error : function(text) {
		this.show({
			title : _('Error'),
			msg : text,
			buttons : this.OK,
			icon : this.ERROR
		})
	},
	warn : function(text) {
		this.show({
			title : _('Warn'),
			msg : text,
			buttons : this.OK,
			icon : this.WARNING
		})
	},
	message : function(text) {
		this.show({
			title : '',
			msg : text,
			buttons : this.OK
		})
	},
	info : function(text) {
		this.show({
			title : _('Notice'),
			msg : text,
			buttons : this.OK,
			icon : this.INFO
		})
	}
});

Ext.ns("Local");

Local.LocalPanel = function(config) {
	Ext.apply(this, config);
	this.windows = [];
	Local.LocalPanel.superclass.constructor.call(this);
};

Ext.extend(Local.LocalPanel, Ext.util.Observable, {
	newWindow: function(opt) {
		var ed = new EditWindow(opt);
		this.windows.push(ed);
		return ed;
	},
	closeWindows: function() {
		for (var i = 0; i < this.windows.length; i++) {
			if (this.windows[i])
				this.windows[i].destroy();
		}
		this.windows = [];			
	}
});

Ext.apply(Ext.form.VTypes, {
	range: function(val,field) {
		if (field.getValue()=="") {
			return;
		}
		if (field.cmpField) {
			var cmp = Ext.getCmp(field.cmpField);
			if (cmp.getValue()!="" && cmp.getValue()>field.getValue()) {
				return false;
			} else {
				return true;
			}
		}
	},
	rangeText: _('The range is invalid.'),
});	

Ext.ns('Ext.ux.util');

function booleanRender(value) {
	if (value=="1") return _('Yes')
	return _('No')
}

function categoryRender(value, meta, rec, row, col, store) {
	subCategoryStore.clearFilter();
	s = subCategoryStore.getById(value);
	if (s) {
		return String.format("{0} ({1})", s.data.name, s.data.category);
	} else {
		return "";
	}
}