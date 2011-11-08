/* PLUGIN: hide */
var hide_message = 'Donnez la liste des roles à qui faut-il enlever ce droit :' ;

function hide_stop_event(event)
{
  if ( event.stopPropagation )
    event.stopPropagation(true) ;
  if ( event.preventDefault )
    event.preventDefault(true) ;
  else
    {
      event.returnValue = false;
      event.keyCode = 0;
    }

  event.cancelBubble = true ;
}

function hide(event, plugin)
{
   hide_stop_event(event) ;
   var who = prompt('«' + plugin + '»\n\n' + hide_message, hide_roles) ;
   window.location = '?hide=' + plugin + ',' + who ;
   return false ;
}

