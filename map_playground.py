#!/usr/bin/env python3

import index

def print_content():
    print('<table border=4><tr><th>')
    print("""
<style type="text/css">
	.draggable{
		position:relative;
		cursor: move;
	}
</style>
<script type="text/javascript">
        function startDrag(e) {
            // determine event object
            if (!e) {
                var e = window.event;
            }

            // IE uses srcElement, others use target
            var targ = e.target ? e.target : e.srcElement;

            if (targ.className != 'dragme') {return};
            // calculate event X, Y coordinates
                offsetX = e.clientX;
                offsetY = e.clientY;

            // assign default values for top and left properties
            if(!targ.style.left) { targ.style.left='0px'};
            if (!targ.style.top) { targ.style.top='0px'};

            // calculate integer values for top and left 
            // properties
            coordX = parseInt(targ.style.left);
            coordY = parseInt(targ.style.top);
            drag = true;

            // move div element
                document.onmousemove=dragDiv;

	    return false;
        }
        function dragDiv(e) {
            if (!drag) {return};
            if (!e) { var e= window.event};
            var targ=e.target?e.target:e.srcElement;
            // move div element
            targ.style.left=coordX+e.clientX-offsetX+'px';
            targ.style.top=coordY+e.clientY-offsetY+'px';
            return false;
        }
        function stopDrag() {
            drag=false;
        }
        window.onload = function() {
            document.onmousedown = startDrag;
            document.onmouseup = stopDrag;
        }
</script>
""")

    print("<img src='globe.gif' class='draggable' />")
    print('</th></tr></table>')

if __name__ == '__main__':
    index.main(print_content)
