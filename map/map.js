// THE CODE THAT GOVERNS TOPOGRAPHICAL AND HIGHLY GEOGRAPHICAL DISPLAYMENT

$(function(){
    // -------------------------------------------------------------------------------- globals

    // All caps means constant, so don't you be modifying these, ya shifty sneak!
    // I got me eye on ya! Now scram!
    var _TILESIZE = 256;
    var _METERS_PER_PIXEL = 20;
    var _RAPHAEL_IMAGE_CUSTOM_DATA_KEY = "ThisIsAUniqueStringThatNoOneElseWillUse";

    var _MAPFRAME = $("#mapFrame"); //document.getElementById('mapFrame');
    var _MAPFRAME_W = parseInt(_MAPFRAME[0].style.width);
    var _MAPFRAME_H = parseInt(_MAPFRAME[0].style.height);
    var _RAPHAEL = Raphael(_MAPFRAME[0], _MAPFRAME_W, _MAPFRAME_H, null);

    var _viewBox = { x: 0, y: 0, w: _MAPFRAME_W, h: _MAPFRAME_H };

    var _mouse_isDown = false;
    var _mouse_move_x = 0;
    var _mouse_move_y = 0;
    var _mouse_move_lastX = 0;		// lastX|Y are used for calculating mouse deltas
    var _mouse_move_lastY = 0;
    //var _mouse_move_meta_lastX = 0;	// meta_lastX|Y are used for updating metabar data during scrolling
    //var _mouse_move_meta_lastY = 0;
    var _tile_deletionQueue = [];	// a list of tiles to remove
    var _zoom_level = 1;

    // TODO REMOVE THIS. It's only here for debugging.
    _handle = function(exp){
	return eval(exp);
    }

    // -------------------------------------------------------------------------------- event handlers

    _MAPFRAME.mousemove(function(event){
	event = event || window.event;
	if(event.pageX || event.pageY){
	    var pos = { x: event.pageX, y: event.pageY };
	}else{
	    var pos = {
		x: event.clientX + document.body.scrollLeft - document.body.clientLeft,
		y: event.clientY + document.body.scrollTop  - document.body.clientTop
	    };
	}

	_mouse_move_x = pos.x - _MAPFRAME.offset().left;
	_mouse_move_y = pos.y - _MAPFRAME.offset().top;

	return false;
    });

    _MAPFRAME.mousedown(function(event){
	_mouse_isDown = true;
	//_mouse_move_meta_lastX = _mouse_move_x;
	//_mouse_move_meta_lastY = _mouse_move_y;

	return false;
    });

    _MAPFRAME.mouseup(function(event){
	_mouse_isDown = false;
	for (var i=0; i<_tile_deletionQueue.length; i++){
	    var el = _tile_deletionQueue[i];
	    if (!tile_isVisibleEl(el))
		el.remove();
	}
	_tile_deletionQueue = [];

	return false;
    });

    function zoom_update(zoom){
	var minZoom = .0625;
	var maxZoom = 8;
	if (zoom < minZoom)
	    zoom = minZoom;
	if (zoom > maxZoom)
	    zoom = maxZoom;
	_zoom_level = zoom;

	// update metabar
	var places = 2;
	var zoomish = Math.floor(Math.pow(10,places)*_zoom_level)/Math.pow(10,places);
	document.getElementById("zoomLabel").innerHTML = "Zoom: "+zoomish+"x";

	// update map
	/*
	  _RAPHAEL.forEach(function(el){
	  var type = el.node.tagName;
	  if (type !== "image")
	  return;

	  tile_update(el);
	  });
	*/

	var vb_w = _viewBox.w;
	var vb_h = _viewBox.h;
	_viewBox.w = unzoomcalc(_MAPFRAME_W);
	_viewBox.h = unzoomcalc(_MAPFRAME_H);
	_viewBox.x -= (_viewBox.w-vb_w)/2;
	_viewBox.y -= (_viewBox.h-vb_h)/2;

	return false;
    }

    /*
    // for actually dragging the slider control
    $("#zoomSlider").on("input change", function(e){
	var raw = $("#zoomSlider").val();
	var zoom = 4/(1<<raw);	// 2**raw
	zoom_update(zoom);
    });
    */
    
    function mouse_wheel(event){
	var delta = 0;
	if(!event)		// because IE sucks
	    event = window.event;

	if(event.wheelDelta){	// IE/Opera
	    delta = event.wheelDelta/120;
	}else if(event.detail){	// Mozilla
	    delta = -event.detail/3;
	}

	// delta is positive if scrolled up, negative if scrolled down
	if(delta){
	    var absDelta = (delta>0 ? delta : -delta);
	    if (absDelta > 5)
		absDelta = 5;

	    var zoomFactor = 1 + (delta>0 ? 1 : -1)*absDelta/25;
	    zoom_update(_zoom_level*zoomFactor);
	}

	// prevents default mouse wheel action
	if(event.preventDefault)
	    event.preventDefault();
	event.returnValue = false;
	return false;
    }

    // for spinning the mouse wheel
    if (_MAPFRAME[0].addEventListener)
	_MAPFRAME[0].addEventListener('DOMMouseScroll', mouse_wheel, false);
    _MAPFRAME[0].onmousewheel = mouse_wheel;

    // -------------------------------------------------------------------------------- utilities

    function tile_name(x, y){
	var sign = function(n){
	    return n>1 ? 1 : -1;
	}

	x = unzoomcalc(x);
	y = unzoomcalc(y);
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
	x = zoomcalc(x);
	y = zoomcalc(y);
	if (x < -_TILESIZE || y < -_TILESIZE)
	    return false;
	if (x > _MAPFRAME_W || y > _MAPFRAME_H)
	    return false;
	return true;
    }

    function tile_new(x,y){
	var tile = _RAPHAEL.image("map/get_tile.py?n="+tile_name(x,y),
				  zoomcalc(x), zoomcalc(y), zoomcalc(_TILESIZE), zoomcalc(_TILESIZE));
	tile.data(_RAPHAEL_IMAGE_CUSTOM_DATA_KEY, { tilex: x, tiley: y });
    }

    function zoomcalc(x){      return x*_zoom_level;	}
    function unzoomcalc(x){    return x/_zoom_level;	}

    function updateViewBox(){  _RAPHAEL.setViewBox(_viewBox.x, _viewBox.y, _viewBox.w, _viewBox.h);  }

    // -------------------------------------------------------------------------------- drawing and meta

    // heartbeat() is a function that is called periodically (via setInterval()) to perform updates
    function heartbeat(){
	//var start = performance.now();
	var deltax = _mouse_move_x-_mouse_move_lastX;
	var deltay = _mouse_move_y-_mouse_move_lastY;

	if (_mouse_isDown){
	    _viewBox.x -= unzoomcalc(deltax);
	    _viewBox.y -= unzoomcalc(deltay);

	    /*
	    // remove invisible tiles
	    _RAPHAEL.forEach(function(el){
		var type = el.node.tagName;
		if (type !== "image"){
		    return;
		}

		// if tile is no longer visible, remove it
		if (!tile_isVisibleEl(el)){
		    if (_tile_deletionQueue.indexOf(el) == -1){
			_tile_deletionQueue.push(el); // appends to list
			//console.log("queue edit: ", _tile_deletionQueue);
		    }
		}
	    });

	    // add tiles that should be visible but aren't
	    for (var x = 0; x < _RAPHAEL.width; x += _TILESIZE) {
		for (var y = 0; y < _RAPHAEL.height; y += _TILESIZE) {
		    var els = _RAPHAEL.getElementsByPoint(x,y);
		    if (els.length != 0) // continue if there's at least one element
			continue;
		    
		    if (els.length == 0){
			// add tile to the map coordinate equivalent of Raphael's screen coords x,y
			var mapX = _viewBox.x + x;
			var mapY = _viewBox.y + y;
			console.log("Adding new tile at ("+mapX+","+mapY+")");
			tile_new(mapX, mapY);
		    }else
			console.log(0);
		}
	    }
	    */
	}

	// perform zooming and panning
	updateViewBox();

	// Update the metadata bar
	/*
	  if (!_mouse_isDown)
	  metabar_update(_viewBox.x+_mouse_move_x, _viewBox.y+_mouse_move_y);
	  else
	  metabar_update(_viewBox.x+_mouse_move_meta_lastX, _viewBox.y+_mouse_move_meta_lastY);
	*/
	metabar_update(_viewBox.x+_viewBox.w/2, _viewBox.y+_viewBox.h/2);

	_mouse_move_lastX = _mouse_move_x;
	_mouse_move_lastY = _mouse_move_y;
	requestAnimationFrame(heartbeat);

	//var deltaT = performance.now() - start;
	//console.log("heartbeat: ", Math.floor(deltaT)+"ms");
    }

    function metabar_update(xval, yval){
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

	var x = fancyCoordsify(-xval, { pos: "West",  neg: "East"  });
	var y = fancyCoordsify(-yval, { pos: "North", neg: "South" });
	
	var inner = y+", "+x;

	var newInnerHTML = "<pre>"+inner+"</pre>";
	var mapPos = document.getElementById('mapPosition');
	if (mapPos.innerHTML != newInnerHTML)
	    mapPos.innerHTML  = newInnerHTML;
    }

    // -------------------------------------------------------------------------------- main

    // draw the initial map stuff (with Raphael!)
    for (var tilex = -10; tilex < 10; tilex++){
	for (var tiley = -10; tiley < 10; tiley++){
	    tile_new(tilex*_TILESIZE, tiley*_TILESIZE);
	}
    }

    requestAnimationFrame(heartbeat);
});