// Credit to https://stackoverflow.com/questions/17992543/how-do-i-drag-an-image-smoothly-around-the-screen-using-pure-javascript
// for the dragging code.

function drag_getTarget(e){
    // IE uses srcElement, sanity uses target
    //var targ = e.target ? e.target : e.srcElement;

    // it was the above because we were dragging images; here, we want to drag a full div
    var targ = document.getElementById("mapTableHolder");
    return targ;
}

function drag_init(e) {
    //console.log("drag_init("+e+")");
    
    // determine event object
    if (!e)
	var e = window.event;

    var targ = drag_getTarget(e);
    if (targ.className != 'draggable'){
	return;
    }

    // calculate event X, Y coordinates
    clickInitialX = e.clientX;
    clickInitialY = e.clientY;

    // assign default values for top and left properties
    if(!targ.style.left) { targ.style.left = '0px'};
    if(!targ.style.top)  { targ.style.top  = '0px'};

    // calculate integer values for top and left properties
    coordX = parseInt(targ.style.left);
    coordY = parseInt(targ.style.top);
    drag_isDragging = true;

    // move element
    document.getElementById("mapTableHolder").onmousemove=drag_drag;
    return false;
}

function drag_drag(e) {
    //console.log("drag_drag("+e+")");

    if (!drag_isDragging)   return;
    if (!e)	var e=window.event;

    // get new position
    var x = coordX+e.clientX-clickInitialX;
    var y = coordY+e.clientY-clickInitialY;

    map_move(x,y);

     // return false so the browser doesn't derp about handling mouse events
    return false;
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

    x = Math.floor(x)
    y = Math.floor(y)

    var xval = ('0000'+x).slice(-4);
    var yval = ('0000'+y).slice(-4);
    return "tile-"+xval+"-"+yval;
}

function change_tile_loadedness(x,y,load){
    var name = tile_name(x,y);
    var elem = document.getElementById(name);

    if (!elem)
	console.log("Couldn't get elem "+name+":", elem);

    var text = '<img src="map/' + (load ? 'get_tile.py?n='+name : 'unloaded.png') + '" />';
    var currLoaded = elem.attributes['currentlyLoaded'].value === 'Y';

    if (currLoaded != load){
	elem.innerHTML = text;
	elem.attributes['currentlyLoaded'].value = load?'Y':'N';
    }
}

function map_move(x,y){
    // for boundary calculations.
    var mapFrame = document.getElementById("mapFrame");
    var mapTable = document.getElementById("mapTable");
    var minX = -mapTable.clientWidth  + parseInt(mapFrame.style.width);
    var minY = -mapTable.clientHeight + parseInt(mapFrame.style.height);

    // check boundaries
    if (x > 0)	x = 0;
    if (y > 0)	y = 0;
    if (x < minX)	x = minX;
    if (y < minY)	y = minY;

    // move the actual map
    var targ = document.getElementById("mapTableHolder");
    targ.style.left = x+'px';
    targ.style.top  = y+'px';
    
    // update metadata
    document.getElementById("mapXPosition").innerHTML = "X: "+x;
    document.getElementById("mapYPosition").innerHTML = "Y: "+y;

    // load or unload tiles (units in tiles, not pixels)
    var radius_unload = 4;
    var radius_load   = 2;

    if(typeof map_move_lastMidTileX === 'undefined')	map_move_lastMidTileX = -1;
    if(typeof map_move_lastMidTileY === 'undefined')	map_move_lastMidTileY = -1;

    var midTileX = Math.floor(-x/256 + parseInt(mapFrame.style.width)/2/256);
    var midTileY = Math.floor(-y/256 + parseInt(mapFrame.style.height)/2/256);

    if (midTileX !== map_move_lastMidTileX || midTileY !== map_move_lastMidTileY){
	for(var i=-radius_unload; i<radius_unload; i++)
	    for(var j=-radius_unload; j<radius_unload; j++){
		if (midTileX+i < 0)	continue;
		if (midTileY+j < 0)	continue;
		if (midTileX+i >= mapSize)	continue;
		if (midTileY+j >= mapSize)	continue;

		var load = i*i+j*j < radius_load*radius_load;
		change_tile_loadedness(midTileX+i, midTileY+j, load);
	    }
    }

    map_move_lastMidTileX = midTileX;
    map_move_lastMidTileY = midTileY;
}
