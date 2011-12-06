// Wait for PhoneGap to load
//
document.addEventListener("deviceready", onDeviceReady, false);

// PhoneGap is ready
//
function onDeviceReady() {
	var db = initDb();    
    db.transaction(populateDB, errorCB, successCB);
    db.transaction(populateData, errorCB, successCB);
	db.transaction(loadData, errorCB);
}

function initDb() {
	return window.openDatabase("cashapp", "1.0", "Cash App Db", 200000);
}

function loadData(tx) {
	tx.executeSql('SELECT * FROM PAYMENT_TYPE', [], querySuccess, errorCB);
}

function querySuccess(tx, results) {
    var len = results.rows.length;
    alert(len);
    console.log("DEMO table: " + len + " rows found.");
    for (var i=0; i<len; i++){
        console.log("Row = " + i + " ID = " + results.rows.item(i).id + " Data =  " + results.rows.item(i).text);
    }
}

// Populate the database 
//
function populateDB(tx) {
     tx.executeSql('CREATE TABLE IF NOT EXISTS PAYMENT_TYPE (id unique, text)');
     tx.executeSql('CREATE TABLE IF NOT EXISTS CATEGORIES (id unique, text, category_text)');
}
// Transaction error callback
//
function errorCB(tx, err) {
    alert("Error processing SQL: "+err);
}
// Transaction success callback
//
function successCB() {
    console.log("Hecho");
}

function populateData(tx) {
	tx.executeSql('DELETE FROM PAYMENT_TYPE');
    tx.executeSql('INSERT INTO PAYMENT_TYPE (id, text) VALUES (1, "Efectivo")');
    tx.executeSql('INSERT INTO PAYMENT_TYPE (id, text) VALUES (2, "Tarjeta")');
}