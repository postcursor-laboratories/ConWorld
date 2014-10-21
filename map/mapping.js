// Credit to https://stackoverflow.com/questions/17992543/how-do-i-drag-an-image-smoothly-around-the-screen-using-pure-javascript
// for the dragging code.

function drag_getTarget(e){
    // IE uses srcElement, sanity uses target
    var targ = e.target ? e.target : e.srcElement;
    return targ;
}

function drag_init(e) {
    //console.log("drag_init("+e+")");

    // determine event object
    if (!e) {
        var e = window.event;
    }

    var targ = drag_getTarget(e);
    if (targ.className != 'draggable') {
	return
    }

    // calculate event X, Y coordinates
    clickInitialX = e.clientX;
    clickInitialY = e.clientY;

    //console.log(targ);
    //console.log(targ.style);
    //console.log("LEFT: "+targ.style.left);
    // assign default values for top and left properties
    if(!targ.style.left) { targ.style.left = '0px'};
    if(!targ.style.top)  { targ.style.top  = '0px'};

    // calculate integer values for top and left properties
    coordX = parseInt(targ.style.left);
    coordY = parseInt(targ.style.top);
    drag_isDragging = true;

    // move element
    document.onmousemove=drag_drag;
    return false;
}

function drag_drag(e) {
    //console.log("drag_drag("+e+")");

    if (!drag_isDragging) {return};
    if (!e) {
	var e=window.event
    }

    var targ = drag_getTarget(e);

    var shouldMove = true;
    /* // TODO: boundary conditions
    if(coordX < 0 && clickInitialX < 0)
	shouldMove = true;
    if(targ.height + clickInitialY > 0)
	shouldMove = true;
    */

    // move element
    if(shouldMove){
	targ.style.left = coordX+e.clientX-clickInitialX+'px';
	targ.style.top  = coordY+e.clientY-clickInitialY+'px';
	//targ.style.zoom += e.scroll;
	return false;
    }
}

function drag_stop() {
    //console.log("drag_stop()");
    drag_isDragging=false;
}

window.onload = function() {
    document.onmousedown = drag_init;
    document.onmouseup   = drag_stop;
}

// ====================================================================== end dragging code

function tile_name(x, y){
    if(x < 0 || x >= 2048) return 'invalid';
    if(y < 0 || y >= 2048) return 'invalid';

    var xval = ('0000'+x).slice(-4);
    var yval = ('0000'+y).slice(-4);
    return "tile-"+xval+"-"+yval;
}

function change_tile_loadedness(x,y,loaded){
    var name = tile_name(x,y);
    var elem = document.getElementById(name);
    console.log(elem);
    var text = loaded ? '<img src="map/'+name+'.png" />' : '';
    elem.innerHTML = text;
}