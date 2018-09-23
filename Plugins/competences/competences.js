/* -*- coding: utf-8 -*- */

add_messages('fr', {
  "competences:center_before": "% de réponses rapides (vert)\n",
  "competences:center_after": "\nCliquez pour avoir une question adaptée",
  "competences:before": "",
  "competences:after": "",
  "competences:question_before": "",
  "competences:question_after": "",
  "competences:recycle": "Cliquez sur le disque à gauche du titre pour répondre à une autre version de la question",
  "competences:star1": "Vous avez accès à toutes les questions",
  "competences:star2": "Vous avez vu toutes les questions",
  "competences:star3": "Vous avez répondu correctement à toutes les questions",
  "competences:star4": "Vous avez vu toutes les versions des questions",
  "competences:star5": "Vous avez répondu rapidement à toutes les questions"
  }) ;
add_messages('en', {
  "competences:center_before": "% of fast answers (green)\n",
  "competences:center_after":  "\nClick to pick an adapted question",
  "competences:recycle": "Click on the disc to answer another version of the question",
  "competences:star1": "You have access to all the questions",
  "competences:star2": "You have read all the questions",
  "competences:star3": "You correctly answered all the questions",
  "competences:star4": "You saw all the questions alternatives",
  "competences:star5": "You answered quickly to all the questions"
  }) ;

var char_close = '▼' ;
var char_open = '▶' ;
var font_small = "6px sans-serif" ;
var font_normal = "10px sans-serif" ;
var font_selected = "20px sans-serif" ;
var competences = {} ; // competence name -> competence object
var competence_names = [] ; // sorted competences
var current_question = '' ;
var questions = {} ; // question name -> question object
var open_close_is_stats = true ;
var nr_questions = 0 ;

var ordered = [
  'suspended_until',
  'perfect_answer',
  'answered',
  'bad_answer_given',
  'not_answerable',
  'not_seen',
  'resigned',
  'question_given'
  ] ;

var student_seed ;

function escape2(txt)
{
  return encodeURIComponent(txt) ;
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
  var q = [] ;
  for(var question in question_list)
  {
    q.push(question_list[question]) ;
    question_list[question].the_weight = question_list[question].weight() ;
  }
  q.sort(function(a, b) { return b.the_weight - a.the_weight ; }) ;
  q[0].jump() ;
}

function question_redo()
{
  window.location.search = baseTag + "?question=" + escape2(current_question)
   + '&erase=1' ;
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
  this.nr_versions = info[7] ;
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
  
  if ( this.classes.indexOf("not_answerable") != -1
       || ( this.classes.indexOf("erasable") == -1
	    && this.classes.indexOf("answered") != -1 )
     )
    weight = -2 ;
  else if ( this.classes.indexOf("question_given") == -1 ) // NOT GIVEN
    weight = 14 ;
  else if ( this.nr_bad + this.nr_good == 0 )
    weight = 12 ;
  else if ( this.nr_good == 0 )
    weight = 10 ;
  else if ( ! this.is_answered() )
    weight = 8 ;
  else if ( this.nr_good < this.nr_versions )
    weight = 6 ;
  else if ( this.nr_perfect == 0 )
    weight = 4 + Math.log( (this.nr_bad+1) / this.nr_good ) / 10 ;
  else
    weight = 2 - this.nr_perfect / this.nr_versions ;
  if ( this.current )
    weight -= 1 ;
  weight += Math.pow(Math.random(), 2) ;
  return weight ;
} ;

var baseTag = document.getElementsByTagName('base')[0].href ;

Question.prototype.jump = function(recycle)
{
  var erase = '' ;
  if ( this.classes.indexOf("erasable") == -1 )
    recycle = false ;
  if ( recycle )
    erase = '&erase=1' ;
  window.location = baseTag + "?question=" + escape2(this.name) + erase ;
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

  if ( q.nr_bad + q.nr_good == 0 )
  {
    slice(ctx, "#FFFFFF", 0          , c.width/2, 0, 1, "") ;
    slice(ctx, "#808080", c.width/2.1, c.width/2, 0, 1, "") ;
    return ;
  }
  var t = [ ["", 0],
	    ["#0F0", q.nr_perfect],
	    ["#44F", q.nr_good],
	    ["#F00", q.nr_bad + q.nr_good]
	    ] ;
  for(var i = 1; i < t.length; i++)
    {
      if ( !q.is_answered || q.is_answered() )
	ctx.fillStyle = t[i][0] ;
      else
	ctx.fillStyle = t[i][0].replace(/[^#F]/g, "9") ;
      slice_path(ctx, 0, c.width/2, t[i-1][1] * n, t[i][1] * n) ;
      ctx.fill() ;
    }
  if ( q.nr_versions )
    {
      ctx.globalAlpha = 0.8 ;
      var good = 2 * Math.PI * Math.min(q.nr_good, q.nr_versions
				       ) / q.nr_versions ;
      ctx.fillStyle = "#FFF" ;
      slice_path(ctx, c.width/2.4, c.width/2, good, 2 * Math.PI) ;
      ctx.fill() ;
      ctx.fillStyle = "#000" ;
      slice_path(ctx, c.width/2.4, c.width/2, 0, good) ;
      ctx.fill() ;
      if ( q.nr_good > q.nr_versions )
      {
	var good = 2 * Math.PI * Math.min(q.nr_good - q.nr_versions,
					  q.nr_versions
					 ) / q.nr_versions ;
	slice_path(ctx, c.width/2.8, c.width/2.4, 0, good) ;
	ctx.fill() ;
      }
    }
}

var canvas_id = 0 ;
var canvas_question = {} ;

Question.prototype.click = function()
{
  this.jump(true) ;
}

Question.prototype.icons = function(left_to_right, classe)
{
  var c = left_to_right ? 0 : canvas_id++ ;
  if ( classe === undefined )
    classe = "nice_results" ;
  canvas_question[c] = this ;
  return '<div class="competences">'
    + '<a class="tips ' + classe + '" onclick="'
    + (questions[this.name] ? 'questions' : 'competences')
    + '[' + js(this.name) + '].click()"><canvas id="C_'
    + c + '"></canvas><span></span></a></div>' ;
} ;

Question.prototype.is_answered = function()
{
  return this.classes.indexOf("answered") != -1 ;
} ;

function MyRand(seed_between_0_1)
{
  this.seed = 2 * Math.PI * seed_between_0_1 ;
}

MyRand.prototype.get = function(max)
{
  var n = Math.sin(this.seed) ;
  this.seed++ ;
  return  Math.floor(Math.abs(n * max * 10000)) % max ;
}

function html(txt)
{
  return txt.replace(/&/g, "&amp;").replace(/>/g, "&gt;").replace(/</g, "&lt;");
}

Question.prototype.display_name = function()
{
  var name = html(this.name) ;
  var short_name = name.split(":") ;
  if ( isNaN(short_name[1]) )
    return name ;
  name = "" ;
  var c = "BCFRTNSDL" ;
  var v = "aeiou" ;
  var rand = new MyRand(student_seed + 1 / (1 + short_name[1]))
  for(var i=0 ; i < 3 ; i++)
  {
    name += c.substr(rand.get(c.length), 1) ;
    name += v.substr(rand.get(v.length), 1) ;
  }
  return short_name[0] + ":" + name ;
}

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

  return (open_close_is_stats ? '    ' : '')
    + this.icons()
    + '<a class="tips ' + info + '" onclick="questions['
    + js(this.name) + '].jump()">' + this.display_name() + '<span>'
    + '</span></a>' ;
} ;

function Competence(name)
{
  this.name = name ;
  this.questions = [] ;
  this.nr_bad = 0 ;
  this.nr_good = 0 ;
  this.nr_perfect = 0 ;
  this.nr_versions = 0 ;
  this.level = 1e9 ;
  competence_names.push(name) ;
}

Competence.prototype.add = function(question)
{
  this.questions.push(question) ;
  this.nr_bad += question.nr_bad ;
  this.nr_good += question.nr_good ;
  this.nr_perfect += question.nr_perfect ;
  this.nr_versions += question.nr_versions ;
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
    else if ( keys['suspended_until'] )
      info = 'suspended_until' ;
    else if ( keys['bad_answer_given'] )
      info = 'bad_answer_given' ;
    else
      info = '' ;
  return info ;
} ;

Competence.prototype.icons = Question.prototype.icons ;

Competence.prototype.click = function()
{
  this.toggle(true) ;
}


Competence.prototype.html = function()
{
  if (this.name === '')
    return '' ;
  var link = '<a class="tips ' + this.classe()
    + '" onclick="competences[' + js(this.name) + '].choose_question()">' ;
  return (open_close_is_stats ? '': link)
    + (open_close_is_stats
       ? this.icons(false, 'openclose')
       : '<var onclick="competences['+ js(this.name)
       + '].toggle();stop_event(event)">'
       + (this.is_open() ? char_close : char_open)
       + '</var> '
      )
    + (open_close_is_stats ? link : '')
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
    if ( competence.name !== '' )
    {
      s.push('<div class="line">') ;
      s.push(competence.html()) ;
      s.push('</div>') ;
    }
    if ( competence.is_open() || competence.name === '' )
    {
      for(var question in competence.questions)
	{
	  s.push('<div class="line">') ;
          s.push(competence.questions[question].html()) ;
	  s.push('</div>') ;
	}
    }
  }
  document.getElementById("competences").innerHTML = s.join('\n') ;
  for(var i = 0; i < canvas_id; i++)
    draw_nice_results(i) ;
}

function patch_title()
{
  var d = document.getElementsByTagName('DIV') ;
  var title ;
  var state = "", heart ;
  for(var i = 0 ; i < d.length; i++)
  {
    if ( d[i].className == 'competences' )
    {
      title = title || d[i].getElementsByTagName('EM')[0] ;
    }
    else if ( d[i].className == 'title_bar' )
    {
      var q = questions[current_question] ;
      if ( q )
      {
	var icon = document.createElement("TD") ;
	icon.style = "font-size: 200%" ;
	icon.innerHTML = questions[current_question].icons(true) ;
	var tr = d[i].getElementsByTagName("TR")[0] ;
	tr.childNodes[1].getElementsByTagName(
	  "A")[0].innerHTML = q.display_name() ;
	tr.insertBefore(icon, tr.childNodes[1]) ;
	draw_nice_results(0) ;
      }
      display_sunburst(title, -300, -300) ;
      heart = d[i].parentNode ;
    }
    else if ( d[i].className == 'question_bad' )
      state = "bad" ;
    else if ( d[i].className == 'question_good' )
      state = "good" ;
    else if ( d[i].className == 'question_answer' && state === '' )
      {
	if ( d[i].innerHTML.match(/<form /) )
	  state = "asked" ;
        else
          state = "done" ;
      }
  }
  if ( heart
       && current_question && current_question !== ''
       && get_level() > 0.05
     )
    {
      var s = '' ;
      var q = questions[current_question] ;
      var c = q.competences ;
      for(var competence in c)
      {
	competence = c[competence] ;
	s += '<div class="question_good" style="display:inline">'
	  + '<a class="tips key_enter">'
	  + '<button onclick="competences[\'' + competence
	  + '\'].choose_question()"><p> ∈ ' + competence
	  + '</p></button></a></div>' ;
      }
      s += '<div class="' + (questions[current_question].nr_versions < 2
			     ? 'question_erase' : 'question_redo')
	+ '" style="display:inline"><a class="tips question_redo">'
	+ '<button onclick="question_redo()" style="background:#FEE"'
	+ (questions[current_question].classes.indexOf("erasable") != -1
	   ? '' : ' disabled')
	+ '><p></p></button><span></span></a></div>' ;

      var more = document.createElement("DIV") ;
      more.style.marginTop = "1em" ;
      more.className = "competences" ;
      more.innerHTML = '<div class="question_good" style="display:inline">'
	+ '<a class="tips key_enter">'
	+ '<button onclick="click_on_next_button()"><p></p></button>'
	+ (state === 'done' || state == "good" ? '<span></span>' : '')
	+ '</a></div>'
        + s ;

      heart.appendChild(more) ;

      var e = document.getElementById('question_good_buttons') ;
      if ( e )
	e.style.display = "none" ;
    }

  if ( ! heart )
    setTimeout(patch_title, 10) ;
}

function hex2(x)
{
  x = Math.floor(255*x).toString(16) ;
  if ( x.length < 2 )
    x = "0" + x ;
  return x ;
}

function hex_color(color)
{
  return "#" + hex2(color[0]) + hex2(color[1]) + hex2(color[2]) ;
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
  angle1 += 0.0001 ;
  angle2 -= 0.0001 ;
  if ( angle2 < angle1 )
    return ;
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
  e.style.zIndex = 11 ;
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

Question.prototype.sunburst = function(ctx, center, scale, i, x, y)
{
  var i_next = i + 1./nr_questions ;
  slice(ctx, "#FFA0A0",
	center + scale*this.nr_good,
	center + scale*(this.nr_good + this.nr_bad),
	i, i_next, "", x, y) ;
  slice(ctx, "#8080FF",
	center + scale*this.nr_perfect,
	center + scale*this.nr_good,
	i, i_next, "", x, y) ;
  slice(ctx, "#40DD40",
	center,
	center + scale*this.nr_perfect,
	i, i_next, "", x, y) ;
  slice(ctx, "#CCC", center * 0.9, center, i,
	i + Math.min(this.nr_good, this.nr_versions)
	/ this.nr_versions / nr_questions,
	"", x, y) ;
  if ( this.nr_good > this.nr_versions )
    slice(ctx, "#888", center * 0.9, center, i,
	  i + Math.min(this.nr_good - this.nr_versions, this.nr_versions)
	  / this.nr_versions / nr_questions,
	  "", x, y) ;
  var selected = slice(ctx, "",
		       center,
		       center + scale*(this.nr_good + this.nr_bad),
		       i, i_next, this.display_name(), x, y) ;
  if ( this.name == current_question )
    slice(ctx, "#FFFF00", center * 0.8, center * 0.9, i, i_next, "", x, y) ;
  return selected ;
} ;

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
  var i = 0 ;
  var scale = 5 ;
  var center = 20 ;
  var nr_perfect = 0, nr_good = 0, nr_bad = 0 ;
  var redraw, selected_question ;
  for(var competence in competences)
    {
      competence =  competences[competence] ;
      var i_start = i ;
      for(var question in competence.questions)
	{
	  question = competence.questions[question] ;
	  var question_hover = question.sunburst(ctx, center, scale, i, x, y) ;
	  if ( question_hover !== false )
	    {
	      redraw = i ;
	      selected_question = question ;
	    }
	  select = question_hover || select ;
	  i += 1./nr_questions ;
	}
      if ( redraw !== undefined )
	 selected_question.sunburst(ctx, center, scale, redraw, x, y) ;
      select = slice(ctx, hex_color(competence.color()),
		     center / 3., center * 0.8, i_start, i,
		     competence.name, x, y) || select ;
      nr_good    += competence.nr_good ;
      nr_perfect += competence.nr_perfect ;
      nr_bad     += competence.nr_bad ;
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

var star_color = "#0D0" ;
var star_color_bad = "#CCC" ;
var tip_style = ' style="z-index:1000; color:#000"' ;
var star_good = '<b style="color:' + star_color + ';display:inline">★</b>';
var star_bad = '<b style="color:'+star_color_bad+ ';display:inline">★</b>';

function progress_bar(percent)
{
    return '<b style="display: inline-block; height: 0.5em; width:5em;'
    + 'border-radius: 0.2em; background: ' + star_color_bad + ';">'
    + '<span style="background:' + star_color
    + ';display:block; text-align:left; width: '
    + percent + '%; height: 100%"></span></b>' ;
}

function display_sunburst(d, width, height, x, y)
{
  var c = document.createElement('CANVAS') ;
  if ( ! c.getContext )
    return ;
  if ( width < 0 )
    {
      var level = get_level() ;
      var s = '<br><a class="tips">' ;
      for(var i=1; i<6; i++)
	s += (level >= i ? star_good : star_bad) ;
      s += '<span' + tip_style + '>' ;
      for(var i=1; i<6; i++)
	s += (level >= i ? star_good : star_bad)
	+ _("competences:star" + i) + '<br>' ;
      s += '</span></a>' ;
      if ( level < 5 )
	s += '<br><a class="tips">'
	+ progress_bar(100*(level%1)) + '<span' + tip_style + '>'
	+ (100*(level % 1)).toFixed(0) + '% → ' + star_good
	+ _("competences:star" + Math.ceil(level))
	+ '</span></a>' ;
      d.innerHTML = s ;
      height = -height ;
      width = -width ;
      c.style.position = "absolute" ;
      c.style.left = "0px" ;
      c.style.top = "0px" ;
      c.style.width = d.offsetHeight ;
      c.style.height = d.offsetHeight ;
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
  return c ;
}

function display_competences(data, question, seed)
{
  current_question = question ;
  student_seed = seed / 1000000000 ;
  for(var i in data)
    questions[data[i][0]] = new Question(data[i]) ;
  for(var competence in competences)
    competences[competence].sort() ;
  competence_names.sort(
    function(a,b) { return competences[a].level - competences[b].level ;}) ;
  document.write('<div id="competences"></div>') ;
  update_competences() ;
  for(var competence in competences)
    nr_questions += competences[competence].questions.length ;

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

// 0 - 1 : % questions accessibles
// 1 - 2 : % questions viewed
// 2 - 3 : % questions correctly answered
// 3 - 4 : % questions perfectly answered
// 4 - 5 : % questions versions done
function get_level()
{
  var nr = 0 ;
  var nr_accessible = 0 ;
  var nr_view = 0 ;
  var nr_good = 0 ;
  var nr_perfect = 0 ;
  var nr_versions = 0 ;
  var nr_total_versions = 0 ;
  var level ;

  for(var question in questions)
  {
    question = questions[question] ;
    nr++ ;
    if ( question.classes.indexOf("not_answerable") == -1 )
      nr_accessible++ ;
    if ( question.classes.indexOf("question_given") != -1 )
      nr_view++ ;
    if ( question.nr_good )
      nr_good++ ;
    if ( question.nr_perfect )
      nr_perfect++ ;
    if ( question.nr_good >= question.nr_versions )
      nr_versions++ ;
    nr_total_versions += question.nr_versions ;
    if ( false )
    {
      console.log(question) ;
      console.log(question.name + ' ' + question.weight()) ;
    }
  }
  if ( nr_accessible < nr )
    level = nr_accessible / nr ;
  else if ( nr_view < nr )
    level = 1 + nr_view / nr ;
  else if ( nr_good < nr )
    level = 2 + nr_good / nr ;
  else if ( nr_versions < nr )
    level = 3 + nr_versions / nr ;
  else
    level = 4 + nr_perfect / nr ;
  if ( true )
    console.log('questions=' + nr
		+ ' accessible=' + nr_accessible
		+ ' view=' + nr_view
		+ ' good=' + nr_good
		+ ' perfect=' + nr_perfect
		+ ' all_versions_done=' + nr_versions
		+ ' total_versions=' + nr_total_versions
		+ ' level=' + level
		) ;
  return level ;
}
