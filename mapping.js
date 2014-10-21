// Credit to https://stackoverflow.com/questions/17992543/how-do-i-drag-an-image-smoothly-around-the-screen-using-pure-javascript

function drag_getTarget(e){
    // IE uses srcElement, sanity uses target
    var targ = e.target ? e.target : e.srcElement;
    return targ;
}

function drag_init(e) {
    console.log("drag_init("+e+")");

    // determine event object
    if (!e) {
        var e = window.event;
    }

    var targ = drag_getTarget(e);
    if (targ.className != 'draggable') {return};

    // calculate event X, Y coordinates
    offsetX = e.clientX;
    offsetY = e.clientY;

    console.log(targ);
    console.log(targ.style);
    console.log("LEFT: "+targ.style.left);
    // assign default values for top and left properties
    //if(!targ.style.left) { targ.style.left = '0px'};
    //if(!targ.style.top)  { targ.style.top  = '0px'};

    // calculate integer values for top and left properties
    coordX = parseInt(targ.style.left);
    coordY = parseInt(targ.style.top);
    drag_isDragging = true;

    // move element
    document.onmousemove=drag_drag;
    return false;
}

function drag_drag(e) {
    console.log("drag_drag("+e+")");

    if (!drag_isDragging) {return};
    if (!e) {
	var e=window.event
    }

    var targ = drag_getTarget(e);

    var shouldMove = true;
    /* // TODO: boundary conditions
    if(coordX < 0 && offsetX < 0)
	shouldMove = true;
    if(targ.height + offsetY > 0)
	shouldMove = true;
    */

    // move element
    if(shouldMove){
	targ.style.left = coordX+e.clientX-offsetX+'px';
	targ.style.top  = coordY+e.clientY-offsetY+'px';
	//targ.style.zoom += e.scroll;
	return false;
    }
}

function drag_stop() {
    console.log("drag_stop()");
    drag_isDragging=false;
}

window.onload = function() {
    document.onmousedown = drag_init;
    document.onmouseup   = drag_stop;
}
