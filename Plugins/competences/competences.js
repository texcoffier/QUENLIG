/* -*- coding: latin-1 -*- */

add_messages('fr', {
  "competences:center_before": "% de réponses rapides (vert)\n",
  "competences:center_after": "\nCliquez pour avoir une question adaptée",
  "competences:before": "",
  "competences:after": "",
  "competences:question_before": "",
  "competences:question_after": "",
  }) ;
add_messages('en', {
  "competences:center_before": "% of fast answers (green)\n",
  "competences:center_after":  "\nClick to pick an adapted question",
  }) ;

var char_close = '&#9660;' ;
var char_open = '&#9654;' ;
var char_recycle = '&#9851;' ;
var font_small = "6px sans-serif" ;
var font_normal = "10px sans-serif" ;
var font_selected = "20px sans-serif" ;
var competences = {} ; // competence name -> competence object
var competence_names = [] ; // sorted competences
var current_question = '' ;
var questions = {} ; // question name -> question object

var ordered = [
  'perfect_answer',
  'answered',
  'bad_answer_given',
  'not_answerable',
  'not_seen',
  'resigned',
  'question_given'
  ] ;

function escape2(txt)
{
  return escape(txt).replace(/[+]/g, "%2B") ;
}

function js(t)
{
  return "'" + t.toString().replace(/\\/g,'\\\\')
    .replace(/"/g,'\\042').replace(/'/g,"\\047").replace(/\n/g,'\\n')
    + "'" ;
}

function stop_event(event)
{
  (event || window.event).cancelBubble = true ;
}

function random_jump(question_list)
{
  var weight = 0 ;
  for(var question in question_list)
    weight += question_list[question].weight() ;
  var random = Math.random() * weight ;
  weight = 0 ;
  for(var question in question_list)
  {
    question = question_list[question] ;
    weight += question.weight() ;
    if ( weight >= random )
      {
	question.jump() ;
	return ;
      }
  }
}

function Question(info)
{
  this.name        = info[0] ;
  this.classes     = info[1] ;
  this.nr_bad      = info[2] ;
  this.nr_good     = info[3] ;
  this.nr_perfect  = info[4] ;
  this.competences = info[5] ;
  this.level       = info[6] ;
  this.current     = this.name == current_question ;

  for(var competence in this.competences)
  {
    competence = this.competences[competence] ;
    if ( competences[competence] === undefined )
      competences[competence] = new Competence(competence) ;
    competences[competence].add(this) ;
  }
}

Question.prototype.weight = function()
{
  var weight ;
  
  if ( this.classes.indexOf("not_answerable") != -1 )
    weight = 0 ;
  else if ( this.classes.indexOf("question_given") == -1 ) // NOT GIVEN
    weight = 100000 ;
  else if ( this.nr_bad + this.nr_good == 0 )
    weight = 10000 ;
  else if ( this.nr_good == 0 )
    weight = 1000 ;
  else if ( ! this.is_answered() )
    weight = 100 ;
  else if ( this.nr_perfect == 0 )
    weight = 10 ;
  else
    weight = 1. / this.nr_perfect ;
  if ( this.current )
    weight *= 0.9 ;
  weight += Math.random() / 1000 ;
  return weight ;
} ;

Question.prototype.jump = function(recycle)
{
  var erase = '' ;
  if ( recycle )
    erase = '&erase=1' ;
  window.location = "?question=" + escape2(this.name) + erase ;
} ;

Question.prototype.nice_results = function(left_to_right)
{
  var cols = Math.max(this.nr_bad,
		      this.nr_good - this.nr_perfect,
		      this.nr_perfect,
		     6) ;
  var s = ['<a class="tips nice_results"><table class="nice_results">'] ;
  function add_line(nr, cls)
  {
    s.push('<tr>') ;
    for(var i=0; i < cols; i++)
    {
      if ( left_to_right
	   ? i < nr
	   : i >= cols - nr
	   )
	s.push('<td class="' + cls + '">') ;
      else
	s.push('<td>') ;
    }
    s.push("</tr>") ;
  }
  add_line(this.nr_bad, "bad") ;
  add_line(this.nr_good - this.nr_perfect, "good") ;
  add_line(this.nr_perfect, "perfect") ;
  s.push("</table><span></span></a>") ;
  return s.join('') ;
} ;

function draw_nice_results(canvas_id)
{
  var c = document.getElementById('C_' + canvas_id) ;
  if ( ! c )
    return ;
  if ( ! c.getContext )
    return ;
  c.width = c.height ;
  var ctx = c.getContext("2d") ;
  var q = canvas_question[canvas_id] ;
  ctx.translate(c.width/2, c.height/2) ;
  var n = 2 * Math.PI / (q.nr_bad + q.nr_good) ;

  var t = [ ["", 0],
	    ["#0F0", q.nr_perfect],
	    ["#00F", q.nr_good],
	    ["#F00", q.nr_bad + q.nr_good]
	    ] ;
  for(var i = 1; i < t.length; i++)
    {
      ctx.fillStyle = t[i][0] ;
      slice_path(ctx, 0, c.width/2, t[i-1][1] * n, t[i][1] * n) ;
      ctx.fill() ;
    }
}

var canvas_id = 0 ;
var canvas_question = {} ;

Question.prototype.nice_results = function(left_to_right)
{
  var c = left_to_right ? 0 : canvas_id++ ;
  canvas_question[c] = this ;
  return '<div class="competences" style="display:inline"><a class="tips nice_results"><canvas id="C_'
    + c + '" style="height:1em; opacity:0.2"></canvas><span></span></a></div>'
}

Question.prototype.is_answered = function()
{
  return this.classes.indexOf("answered") != -1 ;
} ;

Question.prototype.icons = function(left_to_right)
{
  return '<div class="competences" style="display:inline">'
    + this.nice_results(left_to_right)
    + '<a class="tips char_recycle" '
    + (this.is_answered()
       ? 'onclick="questions[' + js(this.name) + '].jump(true)"'
       : 'style="opacity:0.3"'
       )
    + '>' + char_recycle + '<span></span></a></div>' ;
} ;

Question.prototype.html = function()
{
  var info = '' ;
  for(var i in ordered)
    {
      if ( this.classes.indexOf(ordered[i]) != -1 )
      {
	info = ordered[i] ;
	break ;
      }
    }
  if ( this.current )
    info += ' current_question' ;

  return this.icons()
    + '<a class="tips ' + info + '" onclick="questions['
    + js(this.name) + '].jump()">' + this.name + '<span>'
    // + '<br>' + this.weight()
    + '</span></a>' ;
} ;

function Competence(name)
{
  this.name = name ;
  this.questions = [] ;
  this.nr_bad = 0 ;
  this.nr_good = 0 ;
  this.nr_perfect = 0 ;
  this.level = 1e9 ;
  competence_names.push(name) ;
}

Competence.prototype.add = function(question)
{
  this.questions.push(question) ;
  this.nr_bad += question.nr_bad ;
  this.nr_good += question.nr_good ;
  this.nr_perfect += question.nr_perfect ;
  this.level = Math.min(question.level, this.level) ;
} ;

Competence.prototype.sort = function()
{
  this.questions.sort(function(a,b) { return a.level - b.level ; }) ;
} ;

Competence.prototype.is_open = function()
{
  return localStorage[this.name] == '1' ;
} ;

Competence.prototype.open = function()
{
  localStorage[this.name] = '1' ;
} ;

Competence.prototype.toggle = function()
{
  localStorage[this.name] = this.is_open() ? '0' : '1' ;
  update_competences() ;
} ;

Competence.prototype.choose_question = function()
{
  // this.open() ;
  random_jump(this.questions) ;
}

Competence.prototype.nr_questions_perfect = function()
{
  var nr = 0 ;
  for(var i in this.questions)
    if ( this.questions[i].nr_perfect )
      nr++ ;
  return nr ;
}

Competence.prototype.classe = function()
{
    var keys = {} ;
    for(var question in this.questions)
    {
      q_info = this.questions[question].classes.split(/  */) ;
      for(var i in q_info)
      {
        if ( keys[q_info[i]] === undefined )
          keys[q_info[i]] = 0 ;
        keys[q_info[i]]++ ;
      }
    }
    if ( keys['perfect_answer'] == this.questions.length )
      info = 'perfect_answer' ;
    else if ( keys['answered'] == this.questions.length )
      info = 'answered' ;
    else if ( keys['not_answerable'] == this.questions.length )
      info = 'not_answerable' ;
    else if ( keys['not_seen'] )
      info = 'not_seen' ;
    else if ( keys['resigned'] )
      info = 'question_given' ;
    else if ( keys['bad_answer_given'] )
      info = 'bad_answer_given' ;
    else
      info = '' ;
  return info ;
} ;

Competence.prototype.html = function()
{
  if (this.name === '')
    return '' ;
  return '<a class="tips ' + this.classe()
    + '" onclick="competences[' + js(this.name) + '].choose_question()">'
    +'<var onclick="competences['+ js(this.name) +'].toggle();stop_event(event)">'
    + (this.is_open() ? char_close : char_open) + '</var> '
    + this.name + '<span></span></a>' ;
} ;

function get_color(nr_bad, nr_good, nr_perfect)
{
  var s = nr_bad + nr_good ;
  if ( s == 0 )
    return [1, 1, 1] ;
  s *= 2 ;
  return [0.5 + nr_bad / s, 0.5 + nr_perfect / s,
	  0.5 + (nr_good - nr_perfect) / s] ;
}

function hex_color(color)
{
  return "#" + hex2(color[0]) + hex2(color[1]) + hex2(color[2]) ;
}

Competence.prototype.color = function()
{
  return get_color(this.nr_bad, this.nr_good, this.nr_perfect) ;
} ;

function update_competences()
{
  var s = [] ;
  canvas_id = 1 ; // Do not erase the title canvas
  for(var competence in competence_names)
  {
    competence = competences[competence_names[competence]] ;
    s.push(competence.html() +  '<br>') ;
    if ( competence.is_open() || competence.name === '' )
    {
      for(var question in competence.questions)
        s.push(competence.questions[question].html() + '<br>') ;
    }
  }
  document.getElementById("competences").innerHTML = s.join('\n') ;
  for(var i = 0; i < canvas_id; i++)
    draw_nice_results(i) ;
}

function patch_title()
{
  var d = document.getElementsByTagName('DIV') ;
  for(var i = 0 ; i < d.length; i++)
    {
      if ( d[i].className == 'competences' )
	{
	  var title = d[i].getElementsByTagName('EM')[0] ;
	}
      if ( d[i].className == 'title_bar' )
      {
	var q = questions[current_question] ;
	if ( q )
	  {
	    var t = d[i].getElementsByTagName("TD")[0].getElementsByTagName("DIV")[0] ;
	    t.innerHTML = questions[current_question].icons(true)
	      + t.innerHTML ;
	    draw_nice_results(0) ;
	  }
	title.style.position = "relative" ;
	display_sunburst(title) ;
	return ;
      }
    }
  setTimeout(patch_title, 10) ;
}

function hex2(x)
{
  x = Math.floor(255*x).toString(16) ;
  if ( x.length < 2 )
    x = "0" + x ;
  return x ;
}

function display_ifs(d)
{
  function draw_ifs(ctx, depth, transformations, color, d)
  {
    if ( depth == 0 )
    {
      ctx.fillStyle = hex_color(color) ;
      ctx.fillRect(0, 0, 60, 60) ;
      return ;
    }
    var tr, c ;
    d /= 2 ;
    depth-- ;
    for(var i in transformations)
    {
      ctx.save() ;
      tr = transformations[i] ;
      ctx.scale(tr[0], tr[0]) ;
      ctx.rotate(tr[1]) ;
      ctx.translate(tr[2], tr[3]) ;
      c = [color[0] + d*tr[4], color[1] + d*tr[5], color[2] + d*tr[6]] ;
      draw_ifs(ctx, depth, transformations, c, d) ;
      ctx.restore() ;
    }
  }
  var transformations = [] ;
  var i = 0 ;
  for(var competence in competences)
    {
      competence = competences[competence] ;
      var s = competence.nr_bad + competence.nr_good ;
      if ( s == 0 )
	s = 1 ;
      var color = competence.color() ;
      transformations.push(
	[(1-1/(Math.log(s*3)+1.1))/1.5,
	 (competence.questions.length - competence.nr_questions_perfect()
	 ) / competence.questions.length,
	 100 * Math.floor(i/2), 30 * (i % 2),
	 color[0], color[1], color[2]
	]) ;
      i++ ;
    }

  var c = document.createElement('CANVAS') ;
  if ( ! c.getContext )
    return ;
  var ctx = c.getContext("2d") ;

  c.width = 500 ;
  c.height = 200 ;
  c.style.position = "absolute" ;
  c.style.right = "0px" ;
  c.style.top = "0px" ;
  d.appendChild(c) ;

  ctx.translate(50, 50);
  ctx.scale(0.5, 0.5);
  ctx.globalAlpha = 0.2 ;

  var start = new Date() ;
  n = 3
  while(1)
    {
      t = new Date() ;
      if ( t.getTime() - start.getTime() > 50 )
	break ;
      draw_ifs(ctx, n++, transformations, [0,0,0], 1) ;
    }
}

function slice_path(ctx, radius0, radius, angle1, angle2)
{
  ctx.beginPath() ;
  ctx.moveTo(radius0 * Math.cos(angle1), radius0 * Math.sin(angle1)) ;
  ctx.lineTo(radius * Math.cos(angle1), radius * Math.sin(angle1)) ;
  ctx.arc(0, 0, radius, angle1, angle2) ;
  ctx.lineTo(radius0 * Math.cos(angle2), radius0 * Math.sin(angle2)) ;
  ctx.arc(0, 0, radius0, angle2, angle1, true) ;
  ctx.closePath() ;
}

function slice(ctx, color, radius0, radius, angle1, angle2, text, x, y)
{
  angle1 += 0.0005 ;
  angle2 -= 0.0005 ;
  angle1 = 2 * Math.PI * angle1 ;
  angle2 = 2 * Math.PI * angle2 ;
  ctx.fillStyle = color ;
  slice_path(ctx, radius0, radius, angle1, angle2) ;
  var inside = x && ctx.isPointInPath(x, y) ;
  if ( color !== '' )
    ctx.fill() ;
  if ( inside && text != "" )
  {
    if ( text.indexOf(":") == -1 )
      slice_path(ctx, radius0, 150, angle1, angle2) ;
    ctx.fillStyle = "#FFFFFF" ;
    ctx.globalAlpha = 0.5 ;
    ctx.fill() ;
    ctx.globalAlpha = 1 ;
  }
  if ( text !== "" )
    {
      var scale = 0.2 ;
      ctx.save() ;
      ctx.scale(scale, scale) ;
      var angle = (angle1 + angle2) / 2 ;
      if ( angle > Math.PI/2 && angle < 3*Math.PI/2 )
	{
	  angle += Math.PI ;
	  radius0 *= -1 ;
	  ctx.textAlign = "end" ;
	}
      var display_text = text ;
      if ( text.substr(0,1) == " " )
	{
	  // Center label
	  display_text = text.substr(1) ;
	  if ( inside )
	     display_text = _("competences:center_before") + display_text
	    + _("competences:center_after") ;
	  ctx.textAlign = "center" ;
	}
      else
	{
	  if ( inside )
	    {
	      if ( text.indexOf(":") == -1 )
		{
		  display_text = _("competences:before") + display_text
		  + _("competences:after") ;
		}
	      else
		{
		  display_text = _("competences:question_before")
		  + display_text + _("competences:question_after") ;
		}
	    }
	}
      ctx.rotate(angle) ;
      ctx.fillStyle = "#000000" ;
      if ( inside )
	ctx.font = font_selected ;
      else
	{
	  if ( angle2 - angle1 > 0.08 )
	    ctx.font = font_normal ;
	  else
	    ctx.font = font_small ;
	}
      var t = display_text.split('\n') ;
      var h = ctx.font.split('px')[0] ;
      ctx.translate(0, h*(0.5 - t.length/2)) ;
      for(var i in t)
	{
	  ctx.fillText(t[i], radius0/scale, 0) ;
	  ctx.translate(0, h) ;
	}
      ctx.restore() ;
    }
  return inside ? text : false ;
}

function get_xy(event)
{
  event = event || window.event ;
  if ( event.touches && event.touches.length >= 1 )
  {
    var finger0 = event.touches[0] ;
    return [finger0.pageX, finger0.pageY - 30] ;
  }
  else
    return [event.pageX, event.pageY] ;
}

var do_draw_sunburst = false ;

function draw_sunburst(x, y)
{
  do_draw_sunburst = [x, y] ;
}

function zoom_me_move(event)
{
  xy = get_xy(event) ;
  draw_sunburst(xy[0], xy[1]) ;
}

function zoom_me(event)
{
  var e = document.createElement("DIV") ;
  e.style.position = "absolute" ;
  e.style.left = "0%" ;
  e.style.right = "0%" ;
  e.style.top = "0%" ;
  e.style.bottom = "0%" ;
  e.style.opacity = 0.9 ;
  e.id = "competences_zoomed" ;
  e.onmousemove = zoom_me_move ;
  e.addEventListener("touchmove", zoom_me_move, false);
  e.onclick = function(event) {
    event = event || window.event ;
    draw_sunburst(event.pageX, event.pageY) ;
    select = draw_sunburst_real() ;
    if ( select )
      {
	if ( select.substr(0, 1) == " " )
	  random_jump(questions) ;
	else if ( questions[select] )
	  questions[select].jump() ;
	else if ( competences[select] )
	  competences[select].choose_question() ;
	else
	  alert("BUG=(" + select + ')') ;
      }
    else
      e.parentNode.removeChild(e) ;
    } ;
  document.getElementsByTagName("BODY")[0].appendChild(e) ;
  xy = get_xy(event) ;
  display_sunburst(e, e.offsetWidth, e.offsetHeight, xy[0], xy[1]) ;
}

function draw_sunburst_real()
{
  if ( ! do_draw_sunburst )
    return ;
  var select ;
  var ctx = display_sunburst.ctx ;
  x = do_draw_sunburst[0] ;
  y = do_draw_sunburst[1] ;
  if ( x )
    {
      ctx.fillStyle = "#FFFFFF" ;
      ctx.fillRect(-100, -100, 200, 200) ;
    }
  var nr_questions = 0 ;
  for(var competence in competences)
    nr_questions += competences[competence].questions.length ;
  var i = 0 ;
  var scale = 5 ;
  var center = 20 ;
  var nr_perfect = 0, nr_good = 0, nr_bad = 0 ;
  for(var competence in competences)
    {
      competence =  competences[competence] ;
      var i_start = i ;
      for(var question in competence.questions)
	{
	  var i_next = i + 1./nr_questions ;
	  question = competence.questions[question] ;
	  slice(ctx, "#FFA0A0",
		center + scale*question.nr_good,
		center + scale*(question.nr_good + question.nr_bad),
		i, i_next, "", x, y) ;
	  slice(ctx, "#8080FF",
		center + scale*question.nr_perfect,
		center + scale*question.nr_good,
		i, i_next, "", x, y) ;
	  slice(ctx, "#40DD40",
		center,
		center + scale*question.nr_perfect,
		i, i_next, "", x, y) ;
	  select = slice(ctx, "",
			 center,
			 center + scale*(question.nr_good + question.nr_bad),
			 i, i_next, question.name, x, y) || select ;
	  if ( question.name == current_question )
	    slice(ctx, "#FFFF00", center * 0.9, center, i, i_next, "", x, y) ;
	  i = i_next ;
	}
      select = slice(ctx, hex_color(competence.color()),
		     center / 3., center * 0.9, i_start, i,
		     competence.name, x, y) || select ;
      nr_good += competence.nr_good ;
      nr_perfect += competence.nr_perfect ;
      nr_bad += competence.nr_bad ;
    }
  var pc = Math.floor(100 * nr_perfect / (nr_bad+nr_good)) ;
  if ( isNaN(pc) )
    pc = "0" ;
  select = slice(ctx,
		 hex_color(get_color(nr_bad, nr_good, nr_perfect)),
		 0, center / 3. * 0.8, 0, 1, ' ' + pc + '%',
		 x, y) || select ;
  do_draw_sunburst = false ;
  return select ;
}

function display_sunburst(d, width, height, x, y)
{
  var c = document.createElement('CANVAS') ;
  if ( ! c.getContext )
    return ;
  if ( width === undefined )
    {
      height = width = d.offsetHeight ;
      c.style.position = "absolute" ;
      c.style.right = "0px" ;
      c.style.top = "0px" ;
      c.style.opacity = 0.5 ;
      c.onmouseenter = function() { this.style.opacity = 1 ; } ;
      c.onmouseout = function() { this.style.opacity = 0.5 ; } ;
      c.onclick = zoom_me ;
    }
  var ctx = c.getContext("2d") ;

  c.width = width ;
  c.height = height ;
  d.appendChild(c) ;
  ctx.translate(width/2, height/2) ;
  ctx.scale(width/200, width/200) ;
  ctx.textBaseline = "middle";
  display_sunburst.ctx = ctx ;
  draw_sunburst(x, y) ;
}

function display_competences(data, question)
{
  current_question = question ;
  for(var i in data)
    questions[data[i][0]] = new Question(data[i]) ;
  for(var competence in competences)
    competences[competence].sort() ;
  competence_names.sort(
    function(a,b) { return competences[a].level - competences[b].level ;}) ;
  document.write('<div id="competences"></div>') ;
  update_competences() ;

  if ( document.getElementsByTagName("BODY")[0] )
    document.getElementsByTagName("BODY")[0].onkeypress = function(event) {
      if ( event.eventPhase == Event.AT_TARGET && event.keyCode == 13 )
	random_jump(questions) ;
      e = document.getElementById("competences_zoomed") ;
      if ( e )
	e.parentNode.removeChild(e) ;

    } ;
  patch_title() ;
  setInterval(draw_sunburst_real, 100) ;
}

