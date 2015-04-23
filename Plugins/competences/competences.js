/* -*- coding: latin-1 -*- */
var competences = {} ; // competence name -> competence object
var competence_names = [] ; // sorted competences names
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
    weight = 10000 ;
  else if ( this.nr_bad + this.nr_good == 0 )
    weight = 1000 ;
  else if ( this.nr_good == 0 )
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

Question.prototype.nice_results = function()
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
      if ( i >= cols - nr )
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

  return this.nice_results()
    + '<a class="tips ' + info + '" onclick="questions['
    + js(this.name) + '].jump()">' + this.name + '<span>'
    /* + '<br>' + this.weight() */
    + '</span></a>'
    + (this.classes.indexOf("answered") != -1
       ? '&nbsp;<a class="tips ' + info + '" style="position:absolute;" onclick="questions['
       + js(this.name) + '].jump(true)">&#9850;<span class="erase"></span></a>'
       : ""
      ) ;
} ;

function Competence(name)
{
  this.name = name ;
  this.questions = [] ;
  this.nr_bad = 0 ;
  this.nr_good = 0 ;
  this.nr_perfect = 0 ;
  competence_names.push(name) ;
  competence_names.sort() ;
}

Competence.prototype.add = function(question)
{
  this.questions.push(question) ;
  this.nr_bad += question.nr_bad ;
  this.nr_good += question.nr_good ;
  this.nr_perfect += question.nr_perfect ;
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
  return '<var onclick="competences['+ js(this.name) +'].toggle()">' 
    + (this.is_open() ? '\u229f' : '\u229e') + '</var> '
    + '<a class="tips ' + this.classe()
    + '" onclick="competences[' + js(this.name) + '].choose_question()">'
    + this.name + '<span></span></a>' ;
} ;

function update_competences()
{
  var s = [] ;
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
}

function patch_title()
{
  var d = document.getElementsByTagName('DIV') ;
  for(var i = 0 ; i < d.length; i++)
    if ( d[i].className == 'title_bar' )
      {
	d = d[i].getElementsByTagName('TABLE')[0] ;
	d = d.rows[0].cells[0].getElementsByTagName('DIV')[0] ;
	var e = document.createElement('DIV') ;
	e.className = "competences" ;
	e.style.display = "inline" ;
	e.innerHTML = questions[current_question].nice_results() ;
	d.insertBefore(e, d.lastChild) ;
	display_ifs(d) ;
	return ;
      }
  setTimeout(patch_title, 10) ;
}

function display_ifs(d)
{
  function hex2(x)
  {
    x = Math.floor(255*x).toString(16) ;
    if ( x.length < 2 )
      x = "0" + x ;
    return x ;
  }

  function draw_ifs(ctx, depth, transformations, color, d)
  {
    if ( depth == 0 )
    {
      ctx.fillStyle = "#" + hex2(color[0]) + hex2(color[1]) + hex2(color[2]) ;
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
      transformations.push(
	[(1-1/(Math.log(s*3)+1.1))/1.5,
	 (competence.questions.length - competence.nr_questions_perfect()
	 ) / competence.questions.length,
	 100 * Math.floor(i/2), 30 * (i % 2),
	 competence.nr_bad / s,
	 competence.nr_perfect / s,
	 (competence.nr_good - competence.nr_perfect) / s
	]) ;
      i++ ;
    }

  var c = document.createElement('CANVAS') ;
  if ( ! c.getContext )
    return ;
  var ctx = c.getContext("2d") ;

  d.appendChild(c) ;

  c.width = 500 ;
  c.height = 200 ;
  c.style.position = "absolute" ;
  c.style.right = "0px" ;
  c.style.top = "0px" ;

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

function display_competences(data, question)
{
  current_question = question ;
  for(var i in data)
    questions[data[i][0]] = new Question(data[i]) ;
  document.write('<div id="competences"></div>') ;
  update_competences() ;

  if ( document.getElementsByTagName("BODY")[0] )
    document.getElementsByTagName("BODY")[0].onkeypress = function(event) {
      if ( event.eventPhase == Event.AT_TARGET && event.keyCode == 13 )
	random_jump(questions) ;
    } ;
  patch_title() ;
}

