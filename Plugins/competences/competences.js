/* -*- coding: latin-1 -*- */
var competences = {} ;
var competence_names = [] ;
var current_question = '' ;
var question_dict = {} ;

function toggle_competence(competence)
{
  localStorage[competence] = localStorage[competence] == '1' ? '0' : '1' ;
  update_competences() ;
}

function escape2(txt)
{
  return escape(txt).replace(/[+]/g, "%2B") ;
}

function choose_question(competence)
{
  var questions = competences[competence] ;
  var weight = 0 ;
  var q_sorted = [] ;
  for(var question in questions)
  {
    question = questions[question] ;
    if ( question[1].indexOf("not_answerable") != -1 )
      question.weight = 0 ;
    else if ( question[1].indexOf("question_given") == -1 ) // NOT GIVEN
      question.weight = 1024 ;
    else if ( question[2] + question[3] == 0 ) // BAD + GOOD = 0
      question.weight = 64 ;
    else if ( question[3] == 0 ) // GOOD = 0
      question.weight = 16 ;
    else if ( question[4] == 0 ) // PERFECT = 0
      question.weight = 4 ;
    else
      question.weight = 1. / question[4] ;
    if ( question[0] == current_question )
      question.weight /= 10 ;
    question.weight += Math.random() / 1000 ;
    weight += question.weight ;
    q_sorted.push(question) ;
  }
  q_sorted.sort(function(a,b) { return a.weight - b.weight ; }) ;
  var random = Math.random() * weight ;
  weight = 0 ;
  for(var question in q_sorted)
  {
    question = q_sorted[question] ;
    weight += question.weight ;
    if ( weight >= random )
      {
	goto_question(question[0]) ;
	return ;
      }
  }
}

function goto_question(question, recycle)
{
  var q = question_dict[question] ;
  var erase = '' ;
  if ( recycle )
    erase = '&erase=1' ;
  window.location = "?question=" + escape2(question) + erase ;
}

function js(t)
{
  return "'" + t.toString().replace(/\\/g,'\\\\')
    .replace(/"/g,'\\042').replace(/'/g,"\\047").replace(/\n/g,'\\n')
    + "'" ;
}

function nice_results(info)
{
  var b = info[2], g = info[3], p = info[4] ;
  var s = '<a class="nice_results tips"><div>' ;
  for(var i=0; i < b; i++)
    s += '<var class="bad">&nbsp;</var>' ;
  s += '<br>' ;
  for(var i=0; i < g-p; i++)
    s += '<var class="good">&nbsp;</var>' ;
  s += '<br>' ;
  for(var i=0; i < p; i++)
    s += '<var class="perfect">&nbsp;</var>' ;
  s += '</div><span></span></a>' ;
  return s
}

var ordered = [
  'perfect_answer',
  'answered',
  'bad_answer_given',
  'not_answerable',
  'not_seen',
  'resigned',
  'question_given'
  ] ;

function update_competences()
{
  var s = [] ;
  for(var competence in competence_names)
  {
    competence = competence_names[competence] ;
    var open = localStorage[competence] == "1" ;
    var keys = {}, nb = 0 ;
    for(var q_info in competences[competence])
    {
      q_info = competences[competence][q_info][1].split(/  */) ;
      for(var i in q_info)
      {
        if ( keys[q_info[i]] === undefined )
          keys[q_info[i]] = 0 ;
        keys[q_info[i]]++ ;
        nb++ ;
      }
    }
    if ( keys['perfect_answer'] == competences[competence].length )
      info = 'perfect_answer' ;
    else if ( keys['answered'] == competences[competence].length )
      info = 'answered' ;
    else if ( keys['not_answerable'] == competences[competence].length )
      info = 'not_answerable' ;
    else if ( keys['not_seen'] )
      info = 'not_seen' ;
    else if ( keys['resigned'] )
      info = 'question_given' ;
    else if ( keys['bad_answer_given'] )
      info = 'bad_answer_given' ;
    else
      info = '' ;
    if (competence !== '')
      s.push('<var onclick="toggle_competence(' + js(competence) + ')">' 
             + (open ? '\u229f' : '\u229e') + '</var> '
             + '<a class="tips ' + info
	     + '" onclick="choose_question(' + js(competence) + ')">'
	     + competence + '<span></span></a><br>') ;
    if ( open || competence === '' )
    {
      for(var q_info in competences[competence])
      {
        q_info = competences[competence][q_info] ;
	info = '' ;
	for(var i in ordered)
	  if ( q_info[1].indexOf(ordered[i]) != -1 )
	    {
	      info = ordered[i] ;
	      break ;
	    }
        s.push(nice_results(q_info)
               + '<a class="tips ' + info + '" onclick="goto_question('
               + js(q_info[0]) + ')">'
               + q_info[0] + '<span></span></a>'
	       + (q_info[1].indexOf("answered") != -1
		  ? '<a class="tips" style="font-size:130%;position:absolute;" onclick="goto_question('
		  + js(q_info[0]) + ',true)">&#9850;<span class="erase"></span></a>' // &#9851;
		  : ""
		  )
	       + '<br>') ;
      }
    }
  }
  document.getElementById("competences").innerHTML = s.join('\n') ;
}

function display_competences(data, question)
{
  current_question = question ;
  for(var i in data)
    for(var q in data[i][5])
  {
    q = data[i][5][q] ;
    if ( competences[q] === undefined )
      competences[q] = [] ;
    competences[q].push(data[i]) ;
    question_dict[data[i][0]] = data[i] ;
  }
  for(var competence in competences)
    competence_names.push(competence) ;
  competence_names.sort() ;

  document.write('<div id="competences"></div>') ;
  update_competences() ;
}
