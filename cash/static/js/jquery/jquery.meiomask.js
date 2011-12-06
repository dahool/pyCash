/**
 * jquery.meiomask.js
 *
 * @version 1.0.2
 * Created by Fabio M. Costa on 2008-09-16. Please report any bug at http://www.meiocodigo.com
 *
 * Copyright (c) 2008 Fabio M. Costa http://www.meiocodigo.com
 *
 * The MIT License
 *
 * Permission is hereby granted, free of charge, to any person
 * obtaining a copy of this software and associated documentation
 * files (the "Software"), to deal in the Software without
 * restriction, including without limitation the rights to use,
 * copy, modify, merge, publish, distribute, sublicense, and/or sell
 * copies of the Software, and to permit persons to whom the
 * Software is furnished to do so, subject to the following
 * conditions:
 * 
 * The above copyright notice and this permission notice shall be
 * included in all copies or substantial portions of the Software.
 * 
 * THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
 * EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES
 * OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
 * NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT
 * HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
 * WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
 * FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
 * OTHER DEALINGS IN THE SOFTWARE.
 */

(function($){
	
	$.extend({
		mask : {
			
			// the mask rules. You may add yours!
			// number rules will be overwritten
			rules : {
				'z': /[a-z]/,
				'Z': /[A-Z]/,
				'a': /[a-zA-Z]/,
				'*': /[0-9a-zA-Z]/,
				'@': /[0-9a-zA-ZÁ«·‡„ÈËÌÏÛÚı˙˘¸]/
			},
			
			// fixed chars to be used on the masks. You may change it for your needs!
			fixedChars : '[(),.:/ -]',
			
			// these keys will be ignored by the mask. You may add yours!
			keys : {
				BKSPACE	: 8,
				TAB		: 9,
				ENTER	: 13,
				SHIFT	: 16,
				CTRL	: 17,
				ALT		: 18,
				//SPACE	: 32,
				PGUP	: 33,
				PGDOWN	: 34,
				END		: 35,
				HOME	: 36,
				LEFT	: 37,
				UP		: 38,
				RIGHT	: 39,
				DOWN	: 40,
				INSERT	: 45,
				DELETE	: 46,
				METAKEY : 91, // Command key on Mac. '[' key haves this same keycode but on keypress... and this list is used on keydown. So '[' still works as it haves code 221 on keydown.
				F5		: 116
			},
			
			// default settings for the plugin
			options : {
				attr: 'alt', // an attr to look for the mask name or the mask itself
				mask : null, // the mask to be used on the input
				type : 'fixed', // the mask of this mask
				defaultValue : '', // the default value for this input
				//sufix : '',
				//prefix : '',
				//acceptNegative : false,
				onInvalid : function(){},
				onValid : function(){},
				onOverflow : function(){}
			},
			
			// masks. You may add yours!
			// Ex: $.fn.setMask.masks.msk = {mask: '999'}
			// and then if the 'attr' options value is 'alt', your input shoul look like:
			// <input type="text" name="some_name" id="some_name" alt="msk" />
			masks : {
				'phone'		: { mask : '(99) 9999-9999' },
				'phone-us'	: { mask : '(999) 9999-9999' },
				'cpf'		: { mask : '999.999.999-99' }, // cadastro nacional de pessoa fisica
				'cnpj'		: { mask : '99.999.999/9999-99' },
				'date'		: { mask : '39/19/9999' }, //uk date
				'date-us'	: { mask : '19/39/9999' },
				'cep'		: { mask : '99999-999' },
				'time'		: { mask : '29:69' },
				'cc'		: { mask : '9999 9999 9999 9999' }, //credit card mask
				'integer'	: { mask : '999.999.999.999', type : 'reverse' },
				'decimal'	: { mask : '99,999.999.999.999', type : 'reverse', defaultValue : '000' },
				'decimal-us': { mask : '99.999,999,999,999', type : 'reverse', defaultValue : '000' }
			},
			
			//maxength constants
			MAXLENGTH : {
				ie : 2147483647 // IE's max value from the maxlength attr
			},
			
			init : function(){
				// if has not inited...
				if( !this.hasInit ){
					var i;
					this.ignore = false;
					this.fixedCharsReg = new RegExp(this.fixedChars);
					this.fixedCharsRegG = new RegExp(this.fixedChars,'g');
					this.ignoreArray = new Array();
					
					// constructs number rules
					for(i=0; i<=9; i++){
						this.rules[i] = new RegExp('[0-'+i+']');
					}
					
					//we gonna ignore these keys while using the mask
					for( i in this.keys ){
						this.ignoreArray.push(this.keys[i]);
					}
					this.hasInit = true;
				}
			},
			
			set: function(el,options){
				
				var maskObj = this,
					$el = $(el),
					mlStr = 'maxlength';
					
				this.init();
				
				return $el.each(function(){
					
					var $this = $(this),
						o = $.extend({},maskObj.options),
						attrValue = $this.attr(o.attr),
						tmpMask = '',
						// 'input' event fires on every keyboard event on the input
						pasteEvent = ( $.browser.opera || ( $.browser.mozilla && parseFloat($.browser.version.substr(0,3)) < 1.9 ))?'input':'paste';
						
					// then we look for the 'attr' option
					tmpMask = ( typeof options == 'string' )?options:( attrValue != '' )?attrValue:null;
					if(tmpMask) o.mask = tmpMask;
					
					// then we see if it's a defined mask
					if(maskObj.masks[tmpMask]) o = $.extend(o,maskObj.masks[tmpMask]);
					
					// then it looks if the options is an object, if it is we will overwrite the actual options
					if( typeof options == 'object' ) o = $.extend(o,options);
					
					//then we look for some metadata on the input
					if($.metadata) o = $.extend(o,$this.metadata());
					
					if( o.mask != null ){
						
						maskObj.unset($this);
						
						var defaultValue = o.defaultValue,
							mlValue = $this.attr(mlStr);
						o = $.extend({},o,{
							maxlength: mlValue,
							maskArray : o.mask.split(''),
							maskNonFixedCharsArray : o.mask.replace(maskObj.fixedCharsRegG,'').split(''),
							defaultValue: o.defaultValue.split('')
						});
						
						$this.data('mask',o);
						
						// apply mask to the current value of the input
						if($this.val()!='') $this.val( maskObj.string($this.val(),o) );
						
						// apply the default value of the mask to the input
						else if(defaultValue!='') $this.val( maskObj.string(defaultValue,o) );
						
						//sets text-align right for reverse masks
						if(o.type=='reverse') $this.css('text-align','right');
						
						// in safari, chrome and ie, if the attr maxlength is not
						// set it will have a very high value... we dont need maxlength
						// to be set so if its set by the user we set it to a very high value.
						// removing the attribute in IE will set maxlength to a null string, preventing users of doing any input.
						switch(true){
							case ( $.browser.msie )://(ie)
								$this.attr(mlStr, maskObj.MAXLENGTH.ie);
								break;
							case ( $.browser.safari )://(webkit)
								$this.removeAttr(mlStr);
								break;
							default:
								// in mozilla and opera if maxlength is not set it will have value -1.
								// Removing the attribute if it is set will solve the problem
								if( mlValue > -1 ){
									$this.removeAttr(mlStr);
								}
								break;
						}
						// setting the input events
						$this.bind('keydown',{func:maskObj._keyDown,thisObj:maskObj},maskObj._onMask)
							.bind('keyup',{func:maskObj._keyUp,thisObj:maskObj},maskObj._onMask)
							.bind('keypress',{func:maskObj._keyPress,thisObj:maskObj},maskObj._onMask)
							.bind(pasteEvent,{func:maskObj._paste,thisObj:maskObj},maskObj._delayedOnMask);
					}
				});
			},
			
			//unsets the mask from el
			unset : function(el){
				var $el = $(el),
					_this = this;
				return $el.each(function(){
					var $this = $(this);
					if( $this.data('mask') ){
						var maxLength = $this.data('mask').maxlength,
							pasteEvent = ( $.browser.opera || ( $.browser.mozilla && parseFloat($.browser.version.substr(0,3)) < 1.9 ))?'input':'paste';
						if(maxLength == -1)
							$this.removeAttr('maxlength');
						else
						$this.attr('maxlength',maxLength);
						$this.unbind('keydown',_this._onMask)
							.unbind('keypress',_this._onMask)
							.unbind('keyup',_this._onMask)
							.unbind(pasteEvent,_this._delayedOnMask)
							.removeData('mask');
					}
				});
			},
			
			//masks a string
			string : function(str,options){
				this.init();
				var o={};
				if(typeof str != 'string') str = String(str);
				if( typeof options == 'string' ){
					// then we see if it's a defined mask
					if(this.masks[options]) o = $.extend(o,this.masks[options]);
					else o.mask = options;
				}
				else if( typeof options == 'object' )
					o = $.extend(o,options)
				return this.__maskArray(str.split(''),
							o.mask.replace(this.fixedCharsRegG,'').split(''),
							o.mask.split(''),
							(o.type=='reverse'),
							o.defaultValue);
			},
			
			_onMask : function(e){
				var thisObj = e.data.thisObj,
					o = {};
				o._this = e.target;
				o.$this = $(o._this);
				// if the input is readonly it does nothing
				if( o.$this.attr('readonly') ) return true;
				o.value = o.$this.val();
				o.valueArray = o.value.split('');
				o.data = o.$this.data('mask');
				o.nKey = thisObj.__getKeyNumber(e);
				o.range = thisObj.__getRangePosition(o._this);
				o.reverse = (o.data.type=='reverse');
				return e.data.func.call(thisObj,e,o);
			},
			
			// the timeout is set because on ie we can't get the value from the input without it
			_delayedOnMask : function(e){
				setTimeout(function(){ e.data.thisObj._onMask(e) },1);
			},
			
			_keyDown : function(e,o){
				// verifies if the pressed key should be ignored
				this.ignore = ( $.inArray(o.nKey,this.ignoreArray) > -1 );
				return true;
			},
			
			_keyUp : function(e,o){
				return this._paste(e,o);
			},
			
			_paste : function(e,o){
				var $thisVal = this.__maskArray(
					o.valueArray,
					o.data.maskNonFixedCharsArray,
					o.data.maskArray,
					o.reverse,
					o.data.defaultValue
				);
				o.$this.val( $thisVal );
				if(!o.reverse) this.__setRange(o._this,o.range.start,o.range.end);
				//this.__setRange(o._this,$thisVal.length+o.data.prefix.length);
				return true;
			},
			
			_keyPress: function(e,o){
				//console.log('Numero da tecla',o.nKey,this.ignore);
				//if( o.nKey == this.keys.SPACE ) return false;
				//if( o.range.start<=o.data.prefix.length ) return false;
				if( this.ignore || e.ctrlKey || e.metaKey || e.altKey ){
					o.data.onValid.call(o._this,""	);
					return true;
				}
				
				var rangeStart = o.range.start,
					rawValue = o.value,
					c = String.fromCharCode(o.nKey),
					// the input value from the range start to the value start
					valueStart = rawValue.substr(0,rangeStart),
					// the input value from the range end to the value end
					valueEnd = rawValue.substr(o.range.end,rawValue.length),
					maskArray = o.data.maskArray;
					
				if(o.reverse) rawValue = (valueStart+c+valueEnd);
				
				var valueArray = rawValue.replace(this.fixedCharsRegG,'').split(''),
					// searches for fixed chars begining from the range start position, till it finds a non fixed
					extraPos = this.__extraPositionsTill(rangeStart,maskArray);
					
				o.rsEp = rangeStart+extraPos;
				// if the new character is not obeying the law... :P
				if( !this.rules[maskArray[o.rsEp]] ){
					o.data.onOverflow.call(o._this,c);
					return false;
				}
				else if( !this.rules[maskArray[o.rsEp]].test( c ) ){
					o.data.onInvalid.call(o._this,c);
					return false;
				}
				else o.data.onValid.call(o._this,c);
				
				var $thisVal = this.__maskArray(
					valueArray,
					o.data.maskNonFixedCharsArray,
					maskArray,
					o.reverse,
					o.data.defaultValue,
					extraPos
				);
				
				//o.$this.val( o.data.prefix+$thisVal+o.data.sufix );
				o.$this.val( $thisVal );
				//this.__setRange(o._this,$thisVal.length+o.data.prefix.length);
				
				if(o.reverse)
					return this._keyPressReverse(e,o);
				else
					return this._keyPressFixed(e,o);
					
			},
			
			_keyPressReverse : function(e,o){
				return false;
			},
			
			_keyPressFixed : function(e,o){
				if(o.rangeStart==o.range.end || o.data.defaultValue){
					// the 0 thing is cause theres a particular behavior i wasnt liking when you put a default
					// value on a fixed mask and you select the value from the input the range would go to the
					// end of the string when you enter a char. with this it will overwrite the first char wich is a better behavior.
					//opera fix, cant have range value bigger than value length, i think it loops thought the input value...
					if( (o.rsEp==0 && o.value.length==0) || o.rsEp<o.value.length){
						this.__setRange(o._this,o.rsEp,o.rsEp+1);
					}
				}
				else
					this.__setRange(o._this,o.range.start,o.range.end);
				
				return true;
			},
			
			__getKeyNumber : function(e){
				return (e.charCode||e.keyCode||e.which);
			},
			
			// this function is totaly specific to be used with this plugin, youll never need it
			// it gets the array representing an unmasked string and masks it depending on the type of the mask
			__maskArray : function(valueArray,maskNonFixedCharsArray,maskArray,reverse,defaultValue,extraPos){
				if(reverse) valueArray.reverse();
				valueArray = this.__removeInvalidChars(valueArray,maskNonFixedCharsArray);
				if(defaultValue) valueArray = this.__applyDefaultValue.call(valueArray,defaultValue);
				valueArray = this.__applyMask(valueArray,maskArray,extraPos);
				if(reverse){
					valueArray.reverse();
					return valueArray.join('').substring(valueArray.length-maskArray.length);
				}
				else
					return valueArray.join('').substring(0,maskArray.length);
			},
			
			// applyes the default value to the result string
			__applyDefaultValue : function(defaultValue){
				var defLen = defaultValue.length,thisLen = this.length,i;
				//removes the def chars
				for(i=thisLen-1;i>=0;i--){
					if(this[i]==defaultValue[0]) this.pop();
					else break;
				}
				// apply the mask to the value
				for(i=0;i<defLen;i++){
					if(!this[i])
						this[i] = defaultValue[i];
				}
				return this;
			},
				
			// Removes values that doesnt match the mask from the valueArray
			// Returns the array without the invalid chars.
			__removeInvalidChars : function(valueArray,maskNonFixedCharsArray){
				// removes invalid chars
				for(var i=0; i<valueArray.length; i++ ){
					if( maskNonFixedCharsArray[i] && this.rules[maskNonFixedCharsArray[i]] && !this.rules[maskNonFixedCharsArray[i]].test(valueArray[i]) ){
						valueArray.splice(i,1);
						i--;
					}
				}
				return valueArray;
			},
			
			// Apply the current input mask to the valueArray and returns it. 
			__applyMask : function(valueArray,maskArray,plus){
				if( typeof plus == 'undefined' ) plus = 0;
				// apply the current mask to the array of chars
				for(var i=0; i<valueArray.length+plus; i++ ){
					if( maskArray[i] && this.fixedCharsReg.test(maskArray[i]) )
						valueArray.splice(i,0,maskArray[i]);
				}
				return valueArray;
			},
			
			// searches for fixed chars begining from the range start position, till it finds a non fixed
			__extraPositionsTill : function(rangeStart,maskArray){
				var extraPos = 0;
				while( this.fixedCharsReg.test(maskArray[rangeStart]) ){
					rangeStart++;
					extraPos++;
				}
				return extraPos;
			},
			
			// http://www.bazon.net/mishoo/articles.epl?art_id=1292
			__setRange : function(input,start,end) {
				if(typeof end == 'undefined') end = start;
				if (input.setSelectionRange) {
					input.setSelectionRange(start, end);
				} else {
					// assumed IE
					var range = input.createTextRange();
					range.collapse();
					range.moveStart("character", start);
					range.moveEnd("character", end - start);
					range.select();
				}
			},
			
			// a comment at http://www.bazon.net/mishoo/articles.epl?art_id=1292
			__getRangePosition : function(input){
				var result = { start: 0, end: 0 };
				if (input.setSelectionRange){
					result.start = input.selectionStart;
					result.end = input.selectionEnd;
				}
				else if (document.selection && document.selection.createRange){
					var range = document.selection.createRange();
					var r2 = range.duplicate();
					result.start = 0 - r2.moveStart('character', -100000);
					result.end = result.start + range.text.length;
				}
				return result;
			}
			
		}
	});
	
	$.fn.extend({
		setMask : function(options){
			return $.mask.set(this,options);
		},
		unsetMask : function(){
			return $.mask.unset(this);
		}
	});
})(jQuery);
