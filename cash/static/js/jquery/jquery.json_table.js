/*
JsonTable 0.1
Requires jQuery version: 1.2.6
Requires Ext 2.2

Copyright (c) 2008 Sergio Gabriel Teves

Permission is hereby granted, free of charge, to any person
obtaining a copy of this software and associated documentation
files (the "Software"), to deal in the Software without
restriction, including without limitation the rights to use,
copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the
Software is furnished to do so, subject to the following
conditions:

The above copyright notice and this permission notice shall be
included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES
OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT
HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
OTHER DEALINGS IN THE SOFTWARE.
*/

JsonTable = (function($) { // Localise the $ function
	function parse(opts) {
		if (typeof(opts) != "object") opts = {};
		this.options = opts;
		this.build();
	};
	JsonTable.prototype = {
		build: function() {
			
		}
	}
	
})(jQuery); // End localisation of the $ function

Members = {
	membersToTable: function( url, $container ) {
		var $table = $('<table/>');
		var table = $table.attr( "border", "1" )[0];
		var headers = [
			"<tr>",
			    "<th>Member Type</th>", "<th>Last</th>", "<th>First</th>",
			    "<th>Last Paid</th>", "<th>Phone</th>", "<th>Email</th>",
			    "<th>Address</th>", "<th>City</th>",
			    "<th>Postal Code</th>", "<th>Notes</th>",
			"</tr>"
		].join('');
		var headers = ["<tr>"];
		for (var i = 0; i < 
		
		
		
		$table.append( headers );

        $.getJSON( url, function( jsonObj ){
                $.each( jsonObj.members, function(i, member) {
                        Members.memberToRow( member, table );
                });
                $container.append( $table );
        });
	},
	memberToRow: function( member, table ) {
        var tr = document.createElement('tr');
        for( var i = 0; i < member.length; i++ ) {
                var td = document.createElement('td');
                td.appendChild(document.createTextNode( member[i]) );
                tr.appendChild(td);
        }
        table.appendChild(tr);
	}
}
