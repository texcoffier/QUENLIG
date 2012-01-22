function make_style()
{
    var a = document.getElementsByTagName('A') ;
    var location = window.location.hash.toString().substr(1) ;
    if ( location === '' )
	location = 'NEVER-HERE' ;
    
    for(var i = 0 ; i < a.length; i++)
	if ( a[i].href.split('#')[1] == location
	     ||  a[i].name == location
	     )
	    {
		a[i].parentNode.style.background = '#FF6' ;
	    }
	else
	    {
		a[i].parentNode.style.background = '' ;
	    }
}
