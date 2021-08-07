<!DOCTYPE html>
<!--[if lt IE 7]>      <html class="no-js lt-ie9 lt-ie8 lt-ie7"> <![endif]-->
<!--[if IE 7]>         <html class="no-js lt-ie9 lt-ie8"> <![endif]-->
<!--[if IE 8]>         <html class="no-js lt-ie9"> <![endif]-->
<!--[if gt IE 8]><!--> <html class="no-js"> <!--<![endif]-->
<html>
  <head>
    <title>Exprérience Préférences</title>
    <link href="application-3f30be57b6c118e639cf350d34fb118c.css" media="all" rel="stylesheet" type="text/css" />

    <script src="application-4fd66bbc1d249312453de646bbc94e92.js" type="text/javascript"></script>

    <!--[if !IE]> -->
    <script src="modern/modern.min-5f5bac5f30d1194ef32dc3d387c148c9.js" type="text/javascript"></script>
    <!-- <![endif]-->

    <!--[if lte IE 9]>
    <script src="/assets/legacy/legacy.min-fc84d4940f21d232d4f440973eabff24.js" type="text/javascript"></script>
    <![endif]-->

    <meta charset="utf-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge,chrome=1">
    <meta name="viewport" content="width=device-width">
    <link href="/assets/favicon-095b13468d95e2fa09239289e51417ba.ico" rel="shortcut icon" type="image/vnd.microsoft.icon" />
    <script type="text/javascript">

    
function randomize(tab) {
    var i, j, tmp;
    for (i = tab.length - 1; i > 0; i--) {
        j = Math.floor(Math.random() * (i + 1));
        tmp = tab[i];
        tab[i] = tab[j];
        tab[j] = tmp;
    }
    return tab;
}

var taste = ["Kiwi" ,"Litchi", "Mangue", "Mandarine", "Melon", "Mirabelle", "Mûre", "Myrtille", "Orange", "Orange sanguine","Abricot","Ananas","Banane","Citron", "Citron Vert", "Cerise", "Cassis" , "Framboise", "Coco", "Figue", "Fraise", "Fruit de la passion", "Poire", "Rhubarbe", "Pamplemousse", "Miel - Pignons", "Tiramisù" , "Chocolat Gingembre" , "Fraise Tagada" , "Nougat", "	Speculoos", "Café", "Confiture de lait" , "Pistache", "Réglisse", "Lavande", "Caramel", "Dragibus" , "Rose", "Avocat","Chewing-gum", "Olive", "Chocolat Piment", "Tomate - Basilic", "Cannelle", "Chocolat Blanc", "Chocolat", "Amande", "Coquelicot", "Cookies", "Pain d'épice", "Cactus", "Bière", "Oreo", "Nutella", "Vanille", "Barbe à Papa", "Rhum-Raisins", "Potimarron", "Châtaigne", "Pollen Sauvage", "Riz au lait", "Caramel Beurre salé"]
taste = randomize(taste)
var housemates = ["user"];
var nb_selec_taste = 15
var selec_taste = selecTaste(taste)
var nb_attempt = 0;

console.log(selec_taste)

var rent = 100;
var sum = [0, 0, 0];
var polling_attempts = -1;
var max_attempts = 15;
var id = -1;
var pwd = "";


function selecTaste(taste){
    taste = randomize(taste)
    var selec_taste = [];
    var i;
    for (i = 0; i < nb_selec_taste; i++){
        selec_taste.push(taste[i]);
    }
    return selec_taste
}

$(document).ready(function() {
  $.ajaxSetup({
    headers: {
      'X-CSRF-Token': $('meta[name="csrf-token"]').attr('content')
    }
  });
  createBiddingSections();
});



function displayError(msg, id) {
  var element = $("#"+id);
  var in_focus = scrollToView(element);
  if (element.text() == "" || !in_focus) {
    element.text(msg).fadeIn();
  } else {
    element.fadeOut(400, function() {
      element.text(msg).fadeIn();
    });    
  }
}

function createBiddingSections() {
/*
  var bidding_text = "Quel est votre pref/pire, pire vaut 0, meilleur vaut 100, classer les autres par rapport à cet échelle :
        50 à citron  c'est à peu près pareil que avoir une boule de citron ou avoir avec une chance sur deux avoir une boule de chocolat ou une chance sur deux de cerise"
    var bidding_text2 = "On doit élire le meilleur parfum : 100 point à répartir comment vous les répartissez ?" il faut expliquer comment le gagnant est calculé
  */
  /*var bidding_text = "Sur une échelle de 0 à 100 à quel point serez-vous heureux d'obtenir une boule de glace d'un parfum donné en sachant que votre parfum préféré vaut 100 et votre pire 0. Il faut ensuite normaliser ces valeurs avec le bouton normaliser afin de n'octroyer que 100 jetons au total";
  var bidding_text = "En considérant que votre parfum préféré vaut 100 et votre pire vaut 0, classez les autres en considérant le fait que vous octroyez x points à un parfum s'il vous ai égal d'avoir ce parfum que d'avoir x % de chance d'avoir votre parfum préféré sinon votre pire.<br>Par exemple si je mets 50 sur citron c'est que je considère qu'il m'est égal d'avoir une boule de citron que d'avoir une chance sur deux d'avoir mon parfum préféré ou mon pire. <br> Il faut ensuite normaliser afin de n'utiliser au total que 100 jetons";
  // var bidding_text = "On décide d'organiser un concours du meilleur parfum de glace, pour cela vous devez donner votre avis avant de procéder à un vote"
  */
  var bidding_text = "";
  var housemates_copy = housemates;
  var bidding_sections = new Array();
  var html = "";
  html += "<h1>Quelles glaces aimez-vous? </h1>";
  html += "<h2> Ce sondage a pour but de connaître la façon dont sont réparties l'intensité de vos préférences dans un domaine qui intéresse beaucoup de monde : différents parfums de glace. Si vous n'aimez pas les sorbets ni les glaces, ce sondage va sans doute vous ennuyer et nous vous suggérons de ne pas le faire. Il demande 3 minutes maximum . </h2>"
  html += " <div> <p class=\"property-info\">Premièrement parmis les 15 parfums suivants: </br> Quel est le parfum que vous préférez  ? </br> "
  var id_pref = 0;
  var id_pire = 0;
  //html += "<div class="dropdown">"
  //html += "<button onclick="myFunction()" class="dropbtn">Dropdown</button>"
  //html += "<div id="myDropdown" class="dropdown-content">"
  html += "<div>"
  html +=  '<select name="pref" id="pref" onchange="change_pref();>\n'
    var j;
    for (j=0; j <= nb_selec_taste; j++) {
        html += " <option value=\"" + (j+1) + "\">" + selec_taste[j-1] + "</option>"
    };
  html += "</select> </div></br>"
  html += "<div>" 
  html +=  '<select name="pref" id="pref" onchange="change_pref();>\n'
    var j;
    for (j=0; j <= nb_selec_taste; j++) {
        html += " <option value=\"" + (j+1) + "\">" + selec_taste[j-1] + "</option>" // je ne coomprend pas pourquoi je dois passer par ça
    };
  html += "</select> </div></br>" 
  var pref = selec_taste[0];
  var pire = selec_taste[0];
  
  html += "<div> <p class=\"change\" > Nous allons vous demander d'exprimer vos préférences sur les autres différents parfum, sachant que nous vous imposons la calibration suivante : le parfum " + pref + " vaut 100 point et le parfum " + pire + " vaut 0 point. La façon dont vous pouvez identifier le nombre de points x que vous attribuez à un parfum : x est le nombre tel qu'il vous est égal d'avoir ce parfum avec certitude, et de subit un tirage au sort où vous aurez x % de chance d'avoir votre parfum préféré, et 100-x % d'avoir celui que vous aimez le moins. </p>"
    html += " <p class=\"property-info\"> Par exemple : </br> * J’aime beaucoup la mangue, je mets 90 points sur la mangue car je considère qu'il m'est égal d'avoir une boule de mangue que d'avoir 90% de chances d'avoir mon parfum préféré et 10% d'avoir celui que j’aime le moins.</br>* J’aime beaucoup moins le réglisse, je mets 10 points car je considère qu'il m'est égal d'avoir une boule de réglisse que d'avoir 10% de chances d'avoir mon parfum préféré et 90% celui que j’aime le moins.</br>* Je mets 50 points sur le citron car je considère qu'il m'est égal d'avoir une boule de citron que d'avoir une chance sur deux d'avoir mon parfum préféré ou celui que j’aime le moins.<p> </div></div>"
  var i = 0;
    html += " <form method=\"post\" action=\"recup.php\">";
    html += "  <div id ='essai-" + nb_attempt + "'>";
    html += "    <p>" + bidding_text + "</p>";
    html += "    <p id='bidding-error-" + i + "' class='error-msg error-text'></p>";
    html += "    <div class='range-calc'>";
    html += "      <div class='calculations'>";
    
    for (j=0; j < nb_selec_taste; j++) {
      html += "      <div class='calc-row'>";
      html += "        <div class='name'>";
      html += "          <p>" + selec_taste[j] + "</p>";
      html += "        </div>";
      html += "        <div class='nstSlider range nstSlider" + i + "' data-range_min='0' data-range_max='" + rent + "' data-cur_min='0' data-id='" + i + "'>";
      html += "          <div class='leftGrip'></div>";
      html += "        </div>";
      html += "        <span class='calc-value'>";
      html += "          <input type='text' data-id='" + i + "' id='values_" + i + "_" + j + "' name= '" + selec_taste[j] + "' class='valuation_ipt leftLabel cost valuation_ipt"+i+"'>";
      html += "        </span>";
      html += "      </div>";
    }
    
    html += "        <div class='calc-control'>";
    html += "          <div class='btns'>";
    html += "            <button type='button' class='btn reset' onclick='return resetSliders(" + i + ")'>Réinitialiser</button>";
    html += "            <button type='button' class='btn update' onclick='return updateSliders(" + i + ")'>Normaliser</button>";
    html += "            <button type='button' class='btn update' onclick='return checkSliders(" + i + ")'>Envoyer</button>";
   // html += "            <input type=\"submit\" class='btn update' value=\"Valider\" />";
    html += "          </div>";
    html += "          <div class='totals'>";
    html += "            <p><strong>Current Total:</strong> <span id = 'sum-" + i + "'>0</span></p>";
    html += "            <p><strong>Target:</strong> " + rent + "</p>";
    html += "          </div>";
    html += "        </div>";
    html += "      </div>";
    html += "    </div>";
    html += "  </div>";
    html += " </form>";
  $('.accordion-bidding').remove();
  $("#basics").after(html);
  $(".nstSlider").nstSlider({
    left_grip_selector:".leftGrip",
    value_changed_callback: function(cause, v) {
      $(this).parent().find(".leftLabel").val(v);
      updateSum($(this).data('id'));
    }
  });   
  for (i = 0; i < housemates.length; i++) { 
    $(".valuation_ipt"+i).blur(function() {
      var val = parseInt($(this).val());
      if (isNaN(val) || val<=0) val = 0;
      if (val>rent) val=rent;
      $(this).val(val);
      $(this).parent().parent().find(".nstSlider").nstSlider("set_position", val);
      updateSum($(this).data('id'));
  });
  
    resetSliders(i);
  }

  $('.accordion').unbind();
  $('.accordion').accordion({defaultOpen: 'basics'});
}
function change_pire(){
    pire = document.getElementById('pire').options[document.getElementById('pire').selectedIndex].value;
    $(".change").text("Nous allons vous demander d'exprimer vos préférences sur les autres différents parfum, sachant que nous vous imposons la calibration suivante : le parfum " + pref + " vaut 100 point et le parfum " + pire + " vaut 0 point. La façon dont vous pouvez identifier le nombre de points x que vous attribuez à un parfum : x est le nombre tel qu'il vous est égal d'avoir ce parfum avec certitude, et de subit un tirage au sort où vous aurez x % de chance d'avoir votre parfum préféré, et 100-x % d'avoir celui que vous aimez le moins. ");
}

function change_pref(){
    pire = document.getElementById('pref').options[document.getElementById('pref').selectedIndex].value;
    $(".change").text(" Nous allons vous demander d'exprimer vos préférences sur les autres différents parfum, sachant que nous vous imposons la calibration suivante : le parfum " + pref + " vaut 100 point et le parfum " + pire + " vaut 0 point. La façon dont vous pouvez identifier le nombre de points x que vous attribuez à un parfum : x est le nombre tel qu'il vous est égal d'avoir ce parfum avec certitude, et de subit un tirage au sort où vous aurez x % de chance d'avoir votre parfum préféré, et 100-x % d'avoir celui que vous aimez le moins. ");
}
function containsDuplicates(array) {
  var valuesSoFar = {};
  for (var i = 0; i < array.length; ++i) {
      if (!(array[i] === "")) {
        var value = array[i];
        if (Object.prototype.hasOwnProperty.call(valuesSoFar, value)) {
            return true;
        }
        valuesSoFar[value] = true;
      }
  }
  return false;
}

function updateSum(i) {
  sum[i] = 0;
  var temp;
  $(".valuation_ipt"+i).each(function() {
    temp = parseInt($(this).val(),10);
    if (!isNaN(temp)) {
      sum[i] += temp;
    }
  });
  $('#sum-'+i).html(sum[i]);
  $("#bidding_"+i+" .white-check").remove();
  if (sum[i] == rent) {
    $("#bidding_"+i).append("<span class='white-check'>&#10003;</span>");
  }
}

function resetSliders(i) {
  $(".nstSlider"+i).nstSlider("set_position",0);
  $(".valuation_ipt"+i).val(0);
  updateSum(i);
}

function updateSliders(i) {
  if (sum[i] == 0) return;
  var multiplier = 1.0 * rent / sum[i];
  
  var scaled_sum = 0;
  $(".valuation_ipt"+i).each(function() {
    scaled_sum += Math.round(multiplier * parseInt($(this).val(),10));
  });

  var remainder = rent - scaled_sum;
  $(".valuation_ipt"+i).each(function() {
    scaled_val = Math.round(multiplier * parseInt($(this).val(),10));
    if (remainder < 0 && scaled_val > 0) {
      remainder++;
      $(this).val(scaled_val - 1);
    } else if (remainder > 0 && scaled_val < rent) {
      remainder--;
      $(this).val(scaled_val + 1);
    } else {
      $(this).val(scaled_val);
    }
    $(this).parent().parent().find(".nstSlider").nstSlider("set_position", parseInt($(this).val()));
  });  

  $("#bidding_"+i+" .white-check").remove();
  $("#bidding_"+i).append("<span class='white-check'>&#10003;</span>");
}

function checkSliders(i) {
  $("#bidding_"+i+" .white-check").remove();
  if (sum[i] == rent) {
    advanceAccordion($('#bidding_'+i));
    $("#bidding-error-"+i).text("");
    $("#bidding_"+i).append("<span class='white-check'>&#10003;</span>");
    return checkBids();
  } else {
    displayError("Veuillez normaliser avec le bouton normaliser afin de n'utiliser que " + rent + " jetons.", "bidding-error-0");
    return false;
  }
}

function advanceAccordion(cur_tab) {
  next_tab = cur_tab.next().next();
  if (!next_tab.hasClass('accordion')) return;
  
  cur_tab.next().slideUp('slow', function() {
    next_tab.next().slideDown('slow', function() {
      scrollToView(next_tab);
    });
  });
  cur_tab.removeClass('accordion-open');
  cur_tab.addClass('accordion-close');

  
  next_tab.removeClass('accordion-close');
  next_tab.addClass('accordion-open');
  
}

function checkBids() {
  var success = true;
  var i;
  for (i = 0; i < housemates.length; i++) {
    $("#bidding_"+i+" .white-check").remove();
    if (sum[i] != rent) {
      success = false;
    } else {
      $("#bidding_"+i).append("<span class='white-check'>&#10003;</span>");
    }
  }
  if (success) {
    $('#update-results-msg').text("Your request is being processed. This may take a moment.");
    $('#results-table').html('');
    $('#fairness-table').html('');
    $('#submit-demo').hide();
    displayError("Votre participation a bien été prise en compte, merci\n Vous pourrez recommencer dans 2 secondes","bidding-error-0");
    json = buildJSON();
    $.ajax({
      type: "POST",
      url: "recup.php",
      data: {input: json }
    }).fail(function() {
      $('#update-results-msg').text("We encountered an internal server error. Sorry for the inconvenience.");
      $('#submit-demo').show();
    });
    setTimeout(function (){

  $('#essai-' + nb_attempt).remove();
    nb_attempt += 1;
    selec_taste = selecTaste(taste);
    createBiddingSections();

}, 2200)
    
    
  } else {
    displayError("Some participants haven't entered their evaluations, or have errors (checkmarks indicate those who have successfully entered their evaluations). Once everyone is done, press the submit button again.", "update-results-msg");
  }
}

function buildJSON() {
  var json = {}
  // json['selec_taste'] = selec_taste;
  for (var j = 0; j < nb_selec_taste; j++) {
      value = parseInt($('#values_'+0+'_'+j).val(), 10);
      json[selec_taste[j]] = value;      
    }
  return json;
}

function pollResults() {
  $.getScript('../../../demo/poll?id='+id+'&p='+pwd);
}</script>
    <!--[if lt IE 9]>
<script src="http://html5shim.googlecode.com/svn/trunk/html5.js"></script>
<![endif]-->    
  </head>

  <body>


<style>
    .site{
        padding: 1.5em
    }
    
    p {
        font-size : 1em !important
    }
</style>
<div class="site">



<div class="page-content">


    <p id='bidding-error-" + i + "' class='error-msg error-text'></p>
    <div class="wrap" id="basics">
       
    </div>
</div>
</div><!--.site-->
  </body>
  
</html>
