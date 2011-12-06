jQuery.extend(DateInput.DEFAULT_OPTS, {
  stringToDate: function(string) {
    var matches;
    if (matches = string.match(/^(\d{2,2})\/(\d{2,2})\/(\d{4,4})$/)) {
      return new Date(matches[3], matches[2]-1, matches[1]);
    } else {
      return null;
    };
  },

  dateToString: function(date) {
    var month = (date.getMonth() + 1).toString();
    var dom = date.getDate().toString();
    if (month.length == 1) month = "0" + month;
    if (dom.length == 1) dom = "0" + dom;
    return dom + "/" + month + "/" + date.getFullYear();
  }
  
});

//$.mask.masks.decimal = { mask : '99,999999999', type : 'reverse', defaultValue: '000'}; 
  