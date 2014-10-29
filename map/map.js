// THE CODE THAT GOVERNS TOPOGRAPHICAL AND HIGHLY GEOGRAPHICAL DISPLAYMENT

// -------------------------------------------------------------------------------- globals

// All caps means constant, so don't you be modifying these, ya shifty sneak
_MOUSE_UP = 0;
_MOUSE_DN = 1;
_TILESIZE = 256;
_METERS_PER_PIXEL = 20;

// Well, except these ones. They're set properly in window.onload below. But begone, sneak!
_RAPHAEL  = "This hasn't been defined yet! Wait for the page to load!";
_MAPFRAME = "This hasn't been defined yet!";

_mouse_state = _MOUSE_UP;
_map_x = 0;
_map_y = 0;
_mouse_move_lastX = 0;
_mouse_move_lastY = 0;
_tile_deletionQueue = [];	// a list of tiles to remove

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
    var deltax = pos.x-_mouse_move_lastX;
    var deltay = pos.y-_mouse_move_lastY;

    if (_mouse_state == _MOUSE_DN){
	_map_x += deltax;
	_map_y += deltay;

	// move the map
	_RAPHAEL.forEach(function(el){
	    var type = el.node.tagName;
	    if (type !== "image"){
		return;
	    }

	    // el.translate() is deprecated and hella slow anyway
	    //el.translate(deltax, deltay);

	    // el.transform() is fast, avoids the image lag problem, and
	    // just.. generally doesn't suck
	    var x = el.matrix.x(0,0) + deltax;
	    var y = el.matrix.y(0,0) + deltay;
	    el.transform("t"+x+","+y);

	    // if tile is no longer visible, remove it
	    if (!tile_isVisibleEl(el)){
		if (_tile_deletionQueue.indexOf(el) == -1){
		    _tile_deletionQueue.push(el); // appends to list
		    console.log("queue edit: ",_tile_deletionQueue);
		}
		return;
	    }
	});

	// add the tiles that aren't currently visible
	/*
	for (var x = 0; x < parseInt(_RAPHAEL.width); x += _TILESIZE) {
	    for (var y = 0; y < parseInt(_RAPHAEL.height); y += _TILESIZE) {
		var els = _RAPHAEL.getElementsByPoint(x,y);
		//if (els.length != 0) // continue if there's at least one element
		//continue;

		if (els.length == 0){
		    // add tile to the map coordinate equivalent of Raphael's screen coords x,y
		    var mapX = _map_x + x;
		    var mapY = _map_y + y;
		    console.log("Adding new tile at ("+mapX+","+mapY+")");
		    tile_new(mapX, mapY);
		}else
		    console.log(0);
	    }
	}
	*/

	// update the metadata bar
	metabar_update();
    }

    _mouse_move_lastX = pos.x;
    _mouse_move_lastY = pos.y;
}

function mouse_dn(event){    _mouse_state = _MOUSE_DN;	}

function mouse_up(event){
    _mouse_state = _MOUSE_UP;
    for (var i=0; i<_tile_deletionQueue.length; i++){
	var el = _tile_deletionQueue[i];
	if (!tile_isVisibleEl(el))
	    el.remove();
    }
    _tile_deletionQueue = [];
}

window.onload = function(){
    _MAPFRAME = document.getElementById('mapFrame');
    _RAPHAEL = Raphael(mapFrame, mapFrame.style.width, mapFrame.style.height, null);

    _MAPFRAME.onmousemove = mouse_move;
    _MAPFRAME.onmouseup   = mouse_up;
    _MAPFRAME.onmousedown = mouse_dn;

    map_draw();
}

// -------------------------------------------------------------------------------- utilities

function tile_name(x, y){
    var sign = function(n){
	return n>1 ? 1 : -1;
    }

    x /= _TILESIZE;
    y /= _TILESIZE;
    x = sign(x)*Math.floor(Math.abs(x))
    y = sign(y)*Math.floor(Math.abs(y))

    return "tile_"+x+"_"+y;
}

function tile_isVisibleEl(el){
    var bbox = el.getBBox();
    return tile_isVisible(bbox['x'],bbox['y']);
}

function tile_isVisible(x,y){
    if (x < -_TILESIZE || y < -_TILESIZE)
	return false;
    if (x > parseInt(_RAPHAEL.width) || y > parseInt(_RAPHAEL.height))
	return false;
    return true;
}

function tile_new(x,y){
    _RAPHAEL.image("map/get_tile.py?n="+tile_name(x,y), x, y, _TILESIZE, _TILESIZE);
}

// -------------------------------------------------------------------------------- drawing and meta

function metabar_update(){
    var newx = Math.floor(_map_x*100/_TILESIZE)/100;
    var newy = Math.floor(_map_y*100/_TILESIZE)/100;
    var inner = newx+", "+newy;

    /*
    var fancyCoordsify = function(x){
	return x/_TILESIZE*20/1000; // one pixel is 20m
    };

    var x = fancyCoordsify(_map_x);
    var y = fancyCoordsify(_map_y);
    
    var inner = y+"km North, "+x+"km East";
    */

    document.getElementById('mapPosition').innerHTML = "<pre>"+inner+"</pre>";
}

function map_draw(){
    // draw the initial map stuff (with Raphael!)

    for (var x = _map_x - _TILESIZE; x < _map_x + parseInt(_RAPHAEL.width) + _TILESIZE; x += _TILESIZE) {
	for (var y = _map_y - _TILESIZE; y < _map_y + parseInt(_RAPHAEL.height) + _TILESIZE; y += _TILESIZE) {
	    tile_new(x,y);
	}
    }    

    var circle = _RAPHAEL.circle(_map_x, _map_y, 20, 20);
    circle.attr("fill", "#f00");
}
