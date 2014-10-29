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
_mouse_move_x = 0;
_mouse_move_y = 0;
_mouse_move_lastX = 0;
_mouse_move_lastY = 0;
_tile_deletionQueue = [];	// a list of tiles to remove

// -------------------------------------------------------------------------------- mouse handlers

function mouse_move(event){
    event = event || window.event;
    if(event.pageX || event.pageY){
	var pos = { x: event.pageX, y: event.pageY };
    }else{
	var pos = {
	    x: event.clientX + document.body.scrollLeft - document.body.clientLeft,
	    y: event.clientY + document.body.scrollTop  - document.body.clientTop
	};
    }

    _mouse_move_x = pos.x - $("#mapFrame").offset().left;
    _mouse_move_y = pos.y - $("#mapFrame").offset().top;

    return false;
}

function mouse_dn(event){
    _mouse_state = _MOUSE_DN;

    return false;
}

function mouse_up(event){
    _mouse_state = _MOUSE_UP;
    for (var i=0; i<_tile_deletionQueue.length; i++){
	var el = _tile_deletionQueue[i];
	if (!tile_isVisibleEl(el))
	    el.remove();
    }
    _tile_deletionQueue = [];

    return false;
}

window.onload = function(){
    _MAPFRAME = document.getElementById('mapFrame');
    _RAPHAEL = Raphael(mapFrame, mapFrame.style.width, mapFrame.style.height, null);

    _MAPFRAME.onmousemove = mouse_move;
    _MAPFRAME.onmouseup   = mouse_up;
    _MAPFRAME.onmousedown = mouse_dn;

    setInterval(heartbeat, 100);
    
    /*
    setInterval(function(){
	console.time('heartbeat');
	heartbeat();
	console.timeEnd('heartbeat');
    }, 100);
    */

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

// heartbeat() is a function that is called periodically (via setInterval()) to perform updates
function heartbeat(){
    var deltax = _mouse_move_x-_mouse_move_lastX;
    var deltay = _mouse_move_y-_mouse_move_lastY;

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
		    //console.log("queue edit: ", _tile_deletionQueue);
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
    }

    // Update the metadata bar
    
    if (_mouse_state == _MOUSE_UP)
	metabar_update(_map_x+_mouse_move_x, _map_y+_mouse_move_y);
    else
	metabar_update(_map_x, _map_y);
    

    console.log(_map_x, _map_y, _mouse_move_x, _mouse_move_y);
    //metabar_update(_map_x + _mouse_move_x, _map_y + _mouse_move_y);

    _mouse_move_lastX = _mouse_move_x;
    _mouse_move_lastY = _mouse_move_y;
}

function metabar_update(xval, yval){
    /*
    var newx = Math.floor(_map_x*100/_TILESIZE)/100;
    var newy = Math.floor(_map_y*100/_TILESIZE)/100;
    var inner = newx+", "+newy;
    */

    var fancyCoordsify = function(x, obj){
	var direction = x > 0 ? obj.pos : obj.neg;
	x = Math.abs(x);

	var toTwoPlaces = function(n){ return Math.floor(n*100)/100; }

	var meters = x*_METERS_PER_PIXEL;
	if (meters < 1000){
	    return toTwoPlaces(meters)+"m "+direction;
	}else{
	    return toTwoPlaces(meters/1000)+"km "+direction;
	}
    };

    var x = fancyCoordsify(xval, { pos: "West",  neg: "East"  });
    var y = fancyCoordsify(yval, { pos: "North", neg: "South" });
    
    var inner = y+", "+x;

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
