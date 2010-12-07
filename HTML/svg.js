function mouseclick(moi)
{
  var tr = moi.getAttribute('transform') ;
  var zoom = 4;
  var parent = moi.parentNode ;

  /* Bounding box will not be usable after removing from parent */
  var bb =  moi.childNodes.item(1).getBBox() ;

  /* Remove me in order to hide intermediates change */
  parent.removeChild(moi);

  if ( tr.search('matrix') == -1)
    {
      /* Make me nearly opaque */
      for(var i=0; i<moi.childNodes.length; i++)
	{
	  child = moi.childNodes.item(i) ;
	  if ( child.nodeName == 'rect' || child.nodeName == 'text')
	    {
	      /* Save style */
	      child.old_style = child.getAttribute('style') ;
	      /* Set the new style */
	      child.setAttribute('style','opacity:0.7;fill-opacity:0.7;');
	    }
	}
      /* Add the zooming matrix */
      tr = tr + ' matrix(' + zoom + ' 0 0 ' + zoom + ' ' +
	-(zoom - 1) * (bb.x + bb.width/2) + ' ' +
	-(zoom - 1) * (bb.y + bb.height/2) + ')' ;
    }
  else
    {
      /* Restore initial opacity */
      for(var i=0; i<moi.childNodes.length; i++)
	{
	  child = moi.childNodes.item(i) ;
	  if ( child.nodeName == 'rect' || child.nodeName == 'text')
	    {
	      child.setAttribute('style', child.old_style);
	    }
	}
      /* Remove the zooming matrix */
      tr = tr.replace(/ matrix.*/,'') ;
    }
  moi.setAttribute('transform', tr) ;

  /* Put me in the last, in order to hide the others */
  parent.appendChild(moi) ;
}
