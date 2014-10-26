// THE CODE THAT GOVERNS TOPOGRAPHICAL DISPLAYMENT

// -------------------------------------------------------------------------------- globals

// All caps means constant, so don't you be modifying these, ya shifty sneak
_MOUSE_UP = 0;
_MOUSE_DN = 1;

// Well, except this one. This one is set properly in window.onload below. But begone, sneak!
_CANVAS = "This hasn't been defined yet! Wait for the page to load!";

_mouse_state = _MOUSE_UP;
_map_x = 0;
_map_y = 0;

// -------------------------------------------------------------------------------- mouse handlers

function mouse_move(event){
    event = event || window.event;
    function mouseCoords(ev){
	if(ev.pageX || ev.pageY){
	    return {x: ev.pageX, y: ev.pageY};
	}
	return {
	    x: ev.clientX + document.body.scrollLeft - document.body.clientLeft,
	    y: ev.clientY + document.body.scrollTop  - document.body.clientTop
	}
    }

    var pos = mouseCoords(event);
    console.log(pos, _mouse_state);

    // TODO Set _map_x, _map_y appropriately

    // Update the map
    map_draw();
}

function mouse_up(event){    _mouse_state = _MOUSE_UP;	}
function mouse_dn(event){    _mouse_state = _MOUSE_DN;	}

window.onload = function(){
    var mapFrame = document.getElementById('mapFrame');
    _CANVAS = Raphael(mapFrame, mapFrame.style.width, mapFrame.style.height, null);
    //_CANVAS = document.getElementById('canvas');
    _CANVAS.onmousemove = mouse_move;
    _CANVAS.onmouseup   = mouse_up;
    _CANVAS.onmousedown = mouse_dn;
}

/*
function mouse_drag(event){
    console.log(event);
}

function mouse_dragstart(event){
    console.log(event);
}

function mouse_dragend(event){
    console.log(event);
}

window.onload = function(){
    _CANVAS = document.getElementById('canvas');
    _CANVAS.ondrag = mouse_drag;
    _CANVAS.ondragstart = mouse_dragstart;
    _CANVAS.ondragend = mouse_dragend;
}
*/

// -------------------------------------------------------------------------------- utilities

function tile_name(x, y){
    sign = function(n){
	return n>1 ? 1 : -1;
    }

    x = sign(x)*Math.floor(Math.abs(x))
    y = sign(y)*Math.floor(Math.abs(y))

    return "tile_"+x+"_"+y;
}

// -------------------------------------------------------------------------------- drawing

function map_draw(){
    var canvas = document.getElementById('canvas');
    if(!canvas.getContext){	// just in case?
	console.log("Couldn't find canvas element with ID `canvas'");
	return;
    }

    var g = canvas.getContext('2d');

    // draw stuff
}


/*
function change_tile_loadedness(x,y,load){
    return;

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

    // -----------------------------------------------------------------------------------
    // move the actual map
    var targ = document.getElementById("mapTableHolder");
    targ.style.left = x+'px';
    targ.style.top  = y+'px';
    
    // -----------------------------------------------------------------------------------
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

    // -----------------------------------------------------------------------------------
    // update metadata
    
    var offsetX = -x/256 + parseInt(mapFrame.style.width) /2/256 - mapSize/2;
    var offsetY = -y/256 + parseInt(mapFrame.style.height)/2/256 - mapSize/2;
    offsetX = Math.floor(offsetX*100)/100;
    offsetY = Math.floor(offsetY*100)/100;

    // km? Some invented unit? Furlong-wheelbarrows per square sharkfin? Who knows??
    var unit = " tiles "; //"<sup>T</sup>";	// "&deg;"
    offsetX = Math.abs(offsetX)+unit+(offsetX>=0 ? "East"  : "West");
    offsetY = Math.abs(offsetY)+unit+(offsetY>=0 ? "South" : "North");

    var position = "<pre>"+offsetY+", "+offsetX+"</pre>";
    document.getElementById("mapPosition").innerHTML = position;
}
*/