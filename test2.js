function addMoreRow() {
	var table = document.getElementsByClassName("shedule")[0];
	var n = table.childNodes.length;
	// console.log(n);

	var newRow = document.createElement("div");
	newRow.classList.add("row");
	newRow.innerHTML = '<div class="data"><textarea class="input"></textarea></div><div class="data"><button class="btn" onclick="adjustTime('+n+')">Adjust Time</button></div><div class="data"><input type="time" readonly><br><input type="checkbox"></div><div class="data"><input type="time" readonly><br><input type="checkbox"></div><div class="data"><input type="time" readonly><br><input type="checkbox"></div><div class="data"><input type="time" readonly><br><input type="checkbox"></div><div class="data"><input type="time" readonly><br><input type="checkbox"></div><div class="data"><input type="time" readonly><br><input type="checkbox"></div><div class="data"><input type="time" readonly><br><input type="checkbox"></div>';
	table.appendChild(newRow);
}

function adjustTime(n) {
	var savebtn = document.getElementsByClassName("btnSave")[0];
	savebtn.value = n;
	var modal = document.getElementsByClassName("modal")[0];
	modal.style.display = "flex";

	var row = document.getElementsByClassName("shedule")[0].childNodes[n].childNodes;
	var day = document.getElementsByClassName("day");
	for (var i = row.length - 1; i >= 2; i--) {
		if(row[i].childNodes[0].value){
			day[i-2].childNodes[2].value = row[i].childNodes[0].value;
			day[i-2].childNodes[0].childNodes[0].checked = true;
		}
	}
}
function save() {
	var savebtn = document.getElementsByClassName("btnSave")[0];
	var n = parseInt(savebtn.value);
	var row = document.getElementsByClassName("shedule")[0].childNodes[n];
	var allckbx = document.getElementsByClassName("day");
	for (var i = allckbx.length - 1; i >= 0; i--) {
		row.childNodes[i+2].childNodes[0].style.display = "none";
		row.childNodes[i+2].childNodes[0].value = '';
		row.childNodes[i+2].childNodes[2].style.display = "none";
		row.childNodes[i+2].childNodes[2].checked = false;
		if(allckbx[i].childNodes[0].childNodes[0].checked){
			// var j=((i+1)*2)+3;
			row.childNodes[i+2].childNodes[0].value = allckbx[i].childNodes[2].value;
			row.childNodes[i+2].childNodes[0].style.display = "block";
			row.childNodes[i+2].childNodes[2].checked = true;
			row.childNodes[i+2].childNodes[2].style.display = "block";
		}
	}
	cancel();
}
function cancel() {
	var allckbx = document.getElementsByClassName("day");
	for (var i = allckbx.length - 1; i >= 0; i--) {
		allckbx[i].childNodes[0].childNodes[0].checked = false;
		allckbx[i].childNodes[2].value = '';
	}
	var modal = document.getElementsByClassName("modal")[0];
	modal.style.display = "none";
}
