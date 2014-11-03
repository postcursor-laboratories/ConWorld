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

    var _mouse_isDown = false;
    var _map_x = 0;		// in pixel units
    var _map_y = 0;
    var _mouse_move_x = 0;
    var _mouse_move_y = 0;
    var _mouse_move_lastX = 0;		// lastX|Y are used for calculating mouse deltas
    var _mouse_move_lastY = 0;
    //var _mouse_move_meta_lastX = 0;	// meta_lastX|Y are used for updating metabar data during scrolling
    //var _mouse_move_meta_lastY = 0;
    var _tile_deletionQueue = [];	// a list of tiles to remove
    var _zoom_level = 1;

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
	_zoom_level = zoom;

	// update metadata header
	document.getElementById("zoomLabel").innerHTML = "Zoom: "+_zoom_level+"x";

	// update map
	/*
	  _RAPHAEL.forEach(function(el){
	  var type = el.node.tagName;
	  if (type !== "image")
	  return;

	  tile_update(el);
	  });
	*/

	var x = 0;//_MAPFRAME.style.width;
	var y = 0;//_MAPFRAME.style.height;
	var w = unzoomcalc(_MAPFRAME_W);
	var h = unzoomcalc(_MAPFRAME_H);
	_RAPHAEL.setViewBox(x,y,w,h,false);

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
	    var zoom = _zoom_level*(delta>0 ? 1.05 : .95);
	    zoom_update(zoom);
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
	var tile = _RAPHAEL.image("map/get_tile.py?n="+tile_name(x,y),
				  zoomcalc(x), zoomcalc(y), zoomcalc(_TILESIZE), zoomcalc(_TILESIZE));
	tile.data(_RAPHAEL_IMAGE_CUSTOM_DATA_KEY, { tilex: x, tiley: y });
    }

    function zoomcalc(x){      return _zoom_level*x;	}
    function unzoomcalc(x){    return x/_zoom_level;	}

    // -------------------------------------------------------------------------------- drawing and meta

    function tile_update(el){
	var dat = el.data(_RAPHAEL_IMAGE_CUSTOM_DATA_KEY);
	var tx  = zoomcalc(_TILESIZE*dat.x + _map_x);
	var ty  = zoomcalc(_TILESIZE*dat.y + _map_y);
	var transform = "s"+_zoom_level+"t"+tx+","+ty;
	el.transform(transform);
    }

    // heartbeat() is a function that is called periodically (via setInterval()) to perform updates
    function heartbeat(){
	var deltax = _mouse_move_x-_mouse_move_lastX;
	var deltay = _mouse_move_y-_mouse_move_lastY;

	if (_mouse_isDown){
	    _map_x += unzoomcalc(deltax);
	    _map_y += unzoomcalc(deltay);

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
		/*
		  if (!tile_isVisibleEl(el)){
		  if (_tile_deletionQueue.indexOf(el) == -1){
		  _tile_deletionQueue.push(el); // appends to list
		  //console.log("queue edit: ", _tile_deletionQueue);
		  }
		  return;
		  }
		*/
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
	/*
	  if (!_mouse_isDown)
	  metabar_update(_map_x+_mouse_move_x, _map_y+_mouse_move_y);
	  else
	  metabar_update(_map_x+_mouse_move_meta_lastX, _map_y+_mouse_move_meta_lastY);
	*/
	metabar_update(_map_x, _map_y);

	//console.log(_map_x, _map_y, _mouse_move_x, _mouse_move_y);
	//metabar_update(_map_x + _mouse_move_x, _map_y + _mouse_move_y);

	_mouse_move_lastX = _mouse_move_x;
	_mouse_move_lastY = _mouse_move_y;
	requestAnimationFrame(heartbeat);
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

	var newInnerHTML = "<pre>"+inner+"</pre>";
	var mapPos = document.getElementById('mapPosition');
	if (mapPos.innerHTML != newInnerHTML)
	    mapPos.innerHTML  = newInnerHTML;
    }

    // -------------------------------------------------------------------------------- main

    // draw the initial map stuff (with Raphael!)
    for (var x = _map_x - _TILESIZE; x < _map_x + parseInt(_RAPHAEL.width) + _TILESIZE; x += _TILESIZE) {
	for (var y = _map_y - _TILESIZE; y < _map_y + parseInt(_RAPHAEL.height) + _TILESIZE; y += _TILESIZE) {
	    tile_new(x,y);
	}
    }

    requestAnimationFrame(heartbeat);
});