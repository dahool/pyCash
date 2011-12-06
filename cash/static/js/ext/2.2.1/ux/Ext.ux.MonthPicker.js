/**
 * A picker that allows you to select a month and year.
 *
 * This component has been originally started by Joseph Kralicky and
 * further enhanced by cariad. As of version 0.2 I added support for
 * a minimum and maximum date (allowed date range) and noPastMonths.
 *
 * @class     Ext.ux.MonthPicker
 * @extends   Ext.Component
 *
 * @author    Philipp Rosenhagen
 * @date      2008-08-28
 * @version   0.2
 * @link      http://extjs.com/forum/showthread.php?t=20181
 *
 * @license Ext.ux.grid.Search is licensed under the terms of
 * the Open Source LGPL 3.0 license.  Commercial use is permitted to the extent
 * that the code/component(s) do NOT become part of another Open Source or Commercially
 * licensed development library or toolkit without explicit permission.
 *
 * License details: http://www.gnu.org/licenses/lgpl.html
 *
 * This extension has been tested and developed with IE6, FF2, FF3 using Ext 2.0.2.
 * The license is LGPL 3.0 - at least for the Ext 2.0.x branch. Feel free to try it
 * with the latest Ext but don't ask me under which license you can use it...
 * 
 * 2008-12-04 Sergio Gabriel Teves
 * 	Add submitFormat support
 */

Ext.namespace('Ext.ux');

/**
 * @class     Ext.ux.MonthPicker
 * @extends   Ext.Component
 * @param     {Object} config configuration object
 * @constructor
 */
Ext.ux.MonthPicker = function(config) {
    Ext.apply(this, config);
    Ext.ux.MonthPicker.superclass.constructor.call(this);
};

Ext.ux.MonthPicker = Ext.extend(Ext.Component, {

    format : "M, Y",

	submitFormat: "Y/m/d",

    okText : Ext.MessageBox.buttonText.ok,

    cancelText : Ext.MessageBox.buttonText.cancel,

    constrainToViewport : true,

    monthNames : Date.monthNames,

    startDay : 0,

    minDate: null,

    maxDate: null,

    value : 0,

    noPastYears: false, // only use the current year and future years

    noPastMonths: false, // only use the current month and future months

    useDayDate : 1, // set to a number between 1-31 to use this day when creating the resulting date object (or null to use todays date or keep existing)

    initComponent: function(){
        Ext.ux.MonthPicker.superclass.initComponent.call(this);

        this.value = this.value ?
                 this.value.clearTime() : new Date().clearTime();
        this.activeDate = this.value;

        this.addEvents(

            'select'
        );

        if(this.handler){
            this.on("select", this.handler,  this.scope || this);
        }
    },

    focus : function(){
        if(this.el){
            this.update(this.activeDate);
        }
    },

    onRender : function(container, position){
        var m = [ '<div style="width: 175px; height:175px;"></div>' ]
        m[m.length] = '<div class="x-date-mp"></div>';

        var el = document.createElement("div");
        el.className = "x-date-picker";
        el.innerHTML = m.join("");

        container.dom.insertBefore(el, position);

        this.el = Ext.get(el);
        this.monthPicker = this.el.down('div.x-date-mp');
        this.monthPicker.enableDisplayMode('block');

        this.el.unselectable();

        this.showMonthPicker();

        if(Ext.isIE){
            this.el.repaint();
        }

        this.update(this.value);

    },

    createMonthPicker : function(){
        var minMonth = -1;
        if (this.noPastMonths) {
            minMonth = new Date().getMonth();
        }

        if(!this.monthPicker.dom.firstChild){
            var buf = ['<table border="0" cellspacing="0">'];
            for(var i = 0; i < 6; i++){
                buf.push(
                    '<tr><td class="x-date-mp-month'+(i < minMonth ? ' x-date-disabled' : '')+'"><a href="#">', this.monthNames[i].substr(0, 3), '</a></td>',
                    '<td class="x-date-mp-month x-date-mp-sep"><a href="#">', this.monthNames[i+6].substr(0, 3), '</a></td>',
                    i == 0 ?
                    '<td class="x-date-mp-ybtn" align="center"><a class="x-date-mp-prev"></a></td><td class="x-date-mp-ybtn" align="center"><a class="x-date-mp-next"></a></td></tr>' :
                    '<td class="x-date-mp-year"><a href="#"></a></td><td class="x-date-mp-year"><a href="#"></a></td></tr>'
                );
            }
            buf.push(
                '<tr class="x-date-mp-btns"><td colspan="4"><button type="button" class="x-date-mp-ok">',
                    this.okText,
                    '</button><button type="button" class="x-date-mp-cancel">',
                    this.cancelText,
                    '</button></td></tr>',
                '</table>'
            );
            this.monthPicker.update(buf.join(''));
            this.monthPicker.on('click', this.onMonthClick, this);
            this.monthPicker.on('dblclick', this.onMonthDblClick, this);

            this.mpMonths = this.monthPicker.select('td.x-date-mp-month');
            this.mpYears = this.monthPicker.select('td.x-date-mp-year');

            this.mpMonths.each(function(m, a, i){
                i += 1;
                if((i%2) == 0){
                    m.dom.xmonth = 5 + Math.round(i * .5);
                }else{
                    m.dom.xmonth = Math.round((i-1) * .5);
                }
            });
        }
    },

    showMonthPicker : function(){
        this.createMonthPicker();
        var size = this.el.getSize();
        this.monthPicker.setSize(size);
        this.monthPicker.child('table').setSize(size);

        this.mpSelMonth = (this.activeDate || this.value).getMonth();
        this.updateMPMonth(this.mpSelMonth);
        this.mpSelYear = (this.activeDate || this.value).getFullYear();
        this.updateMPYear(this.mpSelYear);

        this.monthPicker.show();
        //this.monthPicker.slideIn('t', {duration:.2});
    },

    updateMonthPicker: function() {
        if ((this.activeDate && !isNaN(this.activeDate.getElapsed())) || (this.value && !isNaN(this.value.getElapsed))) {
            this.mpSelMonth = (this.activeDate || this.value || new Date()).getMonth();
            this.updateMPMonth(this.mpSelMonth);
            this.mpSelYear = (this.activeDate || this.value || new Date()).getFullYear();
            this.updateMPYear(this.mpSelYear);
        }
    },

    updateMPYear : function(y){

        if ( this.noPastYears ) {
            var minYear = new Date().getFullYear();
            if ( y < (minYear+4) ) {
                y = minYear+4;
            }
        }

        this.mpyear = y;
        var ys = this.mpYears.elements;
        for(var i = 1; i <= 10; i++){
            var td = ys[i-1], y2;
            if((i%2) == 0){
                y2 = y + Math.round(i * .5);
                td.firstChild.innerHTML = y2;
                td.xyear = y2;
            }else{
                y2 = y - (5-Math.round(i * .5));
                td.firstChild.innerHTML = y2;
                td.xyear = y2;
            }

            /*
             * Add disabled class if out of allowed range.
             */
            var yearDate = new Date(Date.parse(y2+'/1/1'));
            if (this.minDate && this.maxDate) {
                if (!yearDate.between(new Date(Date.parse(this.minDate.getFullYear()+'/1/1')) || yearDate, new Date(Date.parse(this.maxDate.getFullYear()+'/1/1')) || yearDate)) {
                    Ext.get(td).addClass('x-date-disabled');
                } else {
                    Ext.get(td).removeClass('x-date-disabled');
                }
            }

            this.mpYears.item(i-1)[y2 == this.mpSelYear ? 'addClass' : 'removeClass']('x-date-mp-sel');
        }

        /*
         * We have to make sure, that the user can only select the months which lay within the range!
         */
        if (this.minDate && this.maxDate) {
            this.mpMonths.each( function(m, a, i){
                i += 1;
                if (this.mpSelYear == this.maxDate.getFullYear()) {
                    if (m.dom.xmonth > this.maxDate.getMonth()) {
                        m.addClass('x-date-disabled')
                    } else {
                        m.removeClass('x-date-disabled');
                    }
                } else if (this.mpSelYear == this.minDate.getFullYear()) {
                    if (m.dom.xmonth < this.minDate.getMonth()) {
                        m.addClass('x-date-disabled')
                    } else {
                        m.removeClass('x-date-disabled');
                    }
                } else {
                    m.removeClass('x-date-disabled');
                }
            }, this);
        }
    },

    updateMPMonth : function(sm){
        this.mpMonths.each(function(m, a, i){
            m[m.dom.xmonth == sm ? 'addClass' : 'removeClass']('x-date-mp-sel');
        });
    },

    selectMPMonth: function(m){

    },

    getAdjustedDate : function (year,month){
        return new Date(
            year,
            month,
            this.useDayDate ? // use a specific day date?
            (Math.min(this.useDayDate, (new Date(year, month, 1)).getDaysInMonth())) // yes, cap it to month max
            :
            (this.activeDate || this.value).getDate() // keep existing
        );
    },

    onMonthClick : function(e, t){
        e.stopEvent();
        if (!Ext.fly(t.parentNode).hasClass("x-date-disabled")) {
            var el = new Ext.Element(t), pn;

            // now following the other handling (from original implementation)
            if(el.is('button.x-date-mp-cancel')){
                this.hideMonthPicker();
            }
            else if(el.is('button.x-date-mp-ok')){
                this.update(this.getAdjustedDate(this.mpSelYear, this.mpSelMonth));
                this.fireEvent("select", this, this.value, this.oldValue);
            }
            else if(pn = el.up('td.x-date-mp-month', 2)){
                this.mpMonths.removeClass('x-date-mp-sel');
                pn.addClass('x-date-mp-sel');
                this.mpSelMonth = pn.dom.xmonth;
            }
            else if(pn = el.up('td.x-date-mp-year', 2)){
                this.mpYears.removeClass('x-date-mp-sel');
                pn.addClass('x-date-mp-sel');
                this.mpSelYear = pn.dom.xyear;

                /*
                 * We have to make sure, that no invalid (out of allowed range) month is selected
                 * when switching to a different year. It might be possible that currently the
                 * selected month is valid (meaning lays within the allowed range) but switching
                 * to a different year now invalidates the current month selection. So we deal with
                 * this by switching to the first possible (allowed) month when switching the years.
                 */
                if (this.minDate && this.maxDate) {
                    this.mpMonths.removeClass('x-date-mp-sel'); // bulk-remove from all
                    this.mpMonths.each( function(m, a, i) {
                        if (this.mpSelYear == this.maxDate.getFullYear()) {
                            if (m.dom.xmonth > this.maxDate.getMonth()) {

                            } else {
                                m.addClass('x-date-mp-sel');
                                this.mpSelMonth = m.dom.xmonth;
                                return false;
                            }
                        } else if (this.mpSelYear == this.minDate.getFullYear()) {
                            if (m.dom.xmonth < this.minDate.getMonth()) {

                            } else {
                                m.addClass('x-date-mp-sel');
                                this.mpSelMonth = m.dom.xmonth;
                                return false;
                            }
                        } else {
                            m.addClass('x-date-mp-sel');
                            this.mpSelMonth = m.dom.xmonth;
                            return false;
                        }
                    }, this);
                }
            }
            else if(el.is('a.x-date-mp-prev')){
                this.updateMPYear(this.mpyear-10);
            }
            else if(el.is('a.x-date-mp-next')){
                this.updateMPYear(this.mpyear+10);
            }

            /*
             * We have to make sure, that the user can only select the months which lay within the range!
             */
            if (this.minDate && this.maxDate) {
                this.mpMonths.each( function(m, a, i){
                    i += 1;
                    if (this.mpSelYear == this.maxDate.getFullYear()) {
                        if (m.dom.xmonth > this.maxDate.getMonth()) {
                            m.addClass('x-date-disabled')
                        } else {
                            m.removeClass('x-date-disabled');
                        }
                    } else if (this.mpSelYear == this.minDate.getFullYear()) {
                        if (m.dom.xmonth < this.minDate.getMonth()) {
                            m.addClass('x-date-disabled')
                        } else {
                            m.removeClass('x-date-disabled');
                        }
                    } else {
                        m.removeClass('x-date-disabled');
                    }
                }, this);
            }
        }
    },

    onMonthDblClick : function(e, t){
        e.stopEvent();
        if (!Ext.fly(t.parentNode).hasClass("x-date-disabled")) {
            var el = new Ext.Element(t), pn;
            if(pn = el.up('td.x-date-mp-month', 2)){
                this.update(this.getAdjustedDate(this.mpSelYear, pn.dom.xmonth));
                this.fireEvent("select", this, this.value, this.oldValue);
            }
            else if(pn = el.up('td.x-date-mp-year', 2)){
                this.update(this.getAdjustedDate(pn.dom.xyear, this.mpSelMonth));
                this.fireEvent("select", this, this.value, this.oldValue);
            }
        }
    },

    hideMonthPicker : function(disableAnim){
        Ext.menu.MenuMgr.hideAll();
    },


    showPrevMonth : function(e){
       this.update(this.activeDate.add("mo", -1));
    },


    showNextMonth : function(e){
        this.update(this.activeDate.add("mo", 1));
    },


    showPrevYear : function(){
        this.update(this.activeDate.add("y", -1));
    },


    showNextYear : function(){
        this.update(this.activeDate.add("y", 1));
    },

    update : function( date ) {
        this.activeDate = date;
        this.oldValue = this.value || date; // remember the old value
        this.value = date;

        if(!this.internalRender){
            var main = this.el.dom.firstChild;
            var w = main.offsetWidth;
            this.el.setWidth(w + this.el.getBorderWidth("lr"));
            Ext.fly(main).setWidth(w);
            this.internalRender = true;

            if(Ext.isOpera && !this.secondPass){
                main.rows[0].cells[1].style.width = (w - (main.rows[0].cells[0].offsetWidth+main.rows[0].cells[2].offsetWidth)) + "px";
                this.secondPass = true;
                this.update.defer(10, this, [date]);
            }
        }
    },

    setValue : function( date ) {
        if (date == 'Invalid Date') {
            this.activeDate = null;
            this.value = null;
        } else {
            this.activeDate = date;
            this.value = date;
        }
    }

});

Ext.reg('ux.monthpicker', Ext.ux.MonthPicker);

Ext.ux.MonthItem = function(config){
    Ext.ux.MonthItem.superclass.constructor.call(this, new Ext.ux.MonthPicker(config), config);

    this.picker = this.component;
    this.addEvents('select');

    this.picker.on("render", function(picker){
        picker.getEl().swallowEvent("click");
        picker.container.addClass("x-menu-date-item");
    });

    this.picker.on("select", this.onSelect, this, this.picker.value, this.picker.oldValue);
};

Ext.extend(Ext.ux.MonthItem, Ext.menu.Adapter, {
    onSelect : function(picker, date, value, oldValue){
        this.fireEvent("select", this, date, picker, value, oldValue);
        Ext.ux.MonthItem.superclass.handleClick.call(this);
    }
});

Ext.reg('ux.monthitem', Ext.ux.MonthItem);

Ext.ux.MonthMenu = function(config){
    Ext.ux.MonthMenu.superclass.constructor.call(this, config);
    this.plain = true;
    var mi = new Ext.ux.MonthItem(config);
    this.add(mi);

    this.picker = mi.picker;

    this.relayEvents(mi, ["select"]);
};

Ext.extend(Ext.ux.MonthMenu, Ext.menu.Menu, {
    cls:'x-date-menu',

    /**
     * (Pre-)Set the date.
     */
    setDate: function(d) {
        this.picker.setValue(d);
    },

    setMinDate: function(d) {
        this.picker.minDate = d;
    },

    setMaxDate: function(d) {
        this.picker.maxDate = d;
    }

});

Ext.reg('ux.monthmenu', Ext.ux.MonthMenu);

Ext.ux.MonthField = function(config){
    Ext.ux.MonthField.superclass.constructor.call(this, config);
}

Ext.extend(Ext.ux.MonthField, Ext.form.DateField, {
	submitFormat: Ext.ux.MonthPicker.prototype.submitFormat,
    format : Ext.ux.MonthPicker.prototype.format,
    noPastYears: Ext.ux.MonthPicker.prototype.noPastYears,
    noPastMonths: Ext.ux.MonthPicker.prototype.noPastMonths,
    useDayDate: Ext.ux.MonthPicker.prototype.useDayDate,
    onTriggerClick : function(){
        if(this.disabled){
            return;
        }
        if(this.menu == null){
            this.menu = new Ext.ux.MonthMenu();
        }
        Ext.apply(this.menu.picker, {
            format : this.format,
            noPastYears : this.noPastYears,
            noPastMonths : this.noPastMonths,
            useDayDate : this.useDayDate
        });
        this.menu.on(Ext.apply({}, this.menuListeners, {
            scope:this
        }));
        this.menu.picker.setValue(this.getValue() || new Date());
        this.menu.show(this.el, "tl-bl?");
    }
    ,onRender:function() {
        // call parent
        Ext.ux.MonthField.superclass.onRender.apply(this, arguments);

        var name = this.name || this.el.dom.name;
        this.hiddenField = this.el.insertSibling({
             tag:'input'
            ,type:'hidden'
            ,name:name
            ,value:this.formatHiddenDate(this.parseDate(this.value))
        });
        this.hiddenName = name; // otherwise field is not found by BasicForm::findField
        this.el.dom.removeAttribute('name');
        this.el.on({
             keyup:{scope:this, fn:this.updateHidden}
            ,blur:{scope:this, fn:this.updateHidden}
        });

        this.setValue = this.setValue.createSequence(this.updateHidden);

    } // eo function onRender

    ,onDisable: function(){
        // call parent
        Ext.ux.MonthField.superclass.onDisable.apply(this, arguments);
        if(this.hiddenField) {
            this.hiddenField.dom.setAttribute('disabled','disabled');
        }
    } // of function onDisable

    ,onEnable: function(){
        // call parent
        Ext.ux.MonthField.superclass.onEnable.apply(this, arguments);
        if(this.hiddenField) {
            this.hiddenField.dom.removeAttribute('disabled');
        }
    } // eo function onEnable

    ,formatHiddenDate : function(date){
        return Ext.isDate(date) ? Ext.util.Format.date(date, this.submitFormat) : date;
    }

    ,updateHidden:function() {
        this.hiddenField.dom.value = this.formatHiddenDate(this.getValue());
    } // eo function updateHidden    
});

Ext.reg('ux.monthfield', Ext.ux.MonthField);
