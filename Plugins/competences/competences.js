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
  for(var question in questions)
  {
    question = questions[question] ;
    if (question[0] == current_question )
      question.weight = 0 ;
    else if ( question[1].indexOf("not_answerable") != -1 )
      question.weight = 0 ;
    else if ( question[1].indexOf("question_given") == -1 )
      question.weight = 1000 ;
    else if ( question[2] + question[3] == 0 )
      question.weight = 20 ;
    else if ( question[3] == 0 )
      question.weight = 10 ;
    else
      question.weight = (question[2] + 1) / (question[2] + question[3]) ;
    weight += question.weight ;
  }
  var random = Math.random() * weight ;
  weight = 0 ;
  for(var question in questions)
  {
    question = questions[question] ;
    weight += question.weight ;
    if ( weight >= random )
      {
	goto_question(question[0]) ;
	return ;
      }
  }
}

function goto_question(question)
{
  var q = question_dict[question] ;
  var erase = '' ;
  if ( q[1].indexOf("answered") != -1 )
    {
      if ( confirm(erase_message) )
	erase = '&erase=1' ;
    }
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
  var b = info[2], g = info[3] ;
  var n = b + g ;
  if ( n > 6 )
  {
    b = Math.round((6 * b) / n) ;
    g = n - b ;
  }
  var s = '<div class="nice_results">' ;
  for(var i=0; i < b; i++)
    s += '<span class="bad">&nbsp;</span>' ;
  s += '<br>' ;
  for(var i=0; i < g; i++)
    s += '<span class="good">&nbsp;</span>' ;
  s += '</div>' ;
  return s
}

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
    if ( keys['answered'] == competences[competence].length )
      info = 'answered' ;
    else if ( keys['not_answerable'] == competences[competence].length )
      info = 'not_answerable' ;
    else if ( keys['bad_answer_given'] >= 1 )
      info = 'bad_answer_given' ;
    else if ( keys['resigned'] == competences[competence].length )
      info = 'question_given' ;
    else if ( keys['resigned'] == 0 )
      info = 'not_seen' ;
    else
      info = '' ;
    if (competence !== '')
      s.push('<var onclick="toggle_competence(' + js(competence) + ')">' 
             + (open ? '\u229f' : '\u229e') + '</var> '
             + '<a class="' + info
	     + '" onclick="choose_question(' + js(competence) + ')">'
	     + competence + '</a><br>') ;
    if ( open || competence === '' )
    {
      for(var q_info in competences[competence])
      {
        q_info = competences[competence][q_info] ;
        s.push(nice_results(q_info)
               + '<a class="' + q_info[1] + '" onclick="goto_question('
               + js(q_info[0]) + ')">'
               + q_info[0] + '</a><br>') ;
      }
    }
  }
  document.getElementById("competences").innerHTML = s.join('\n') ;
}

function display_competences(data, question, message)
{
  erase_message = message ;
  current_question = question ;
  for(var i in data)
    for(var q in data[i][4])
  {
    q = data[i][4][q] ;
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
