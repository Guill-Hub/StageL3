<!DOCTYPE html>
<!--[if lt IE 7]>      <html class="no-js lt-ie9 lt-ie8 lt-ie7"> <![endif]-->
<!--[if IE 7]>         <html class="no-js lt-ie9 lt-ie8"> <![endif]-->
<!--[if IE 8]>         <html class="no-js lt-ie9"> <![endif]-->
<!--[if gt IE 8]><!--> <html class="no-js"> <!--<![endif]-->
<html>
  <head>
    <title>Expérience Préférences</title>
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

var taste = ["Kiwi" ,"Litchi", "Mangue", "Mandarine", "Melon", "Mirabelle", "Mûre", "Myrtille", "Orange", "Orange sanguine","Abricot","Ananas","Banane","Citron", "Citron Vert", "Cerise", "Cassis" , "Framboise", "Coco", "Figue", "Fraise", "Fruit de la passion", "Poire", "Rhubarbe", "Pamplemousse", "Miel - Pignons", "Tiramisù" , "Chocolat Gingembre" , "Fraise Tagada" , "Nougat", "Speculoos", "Café", "Confiture de lait" , "Pistache", "Réglisse", "Lavande", "Caramel", "Dragibus" , "Rose", "Avocat","Chewing-gum", "Olive", "Chocolat Piment", "Tomate - Basilic", "Cannelle", "Chocolat Blanc", "Chocolat", "Amande", "Coquelicot", "Cookies", "Pain d'épice", "Cactus", "Bière", "Oreo", "Nutella", "Vanille", "Barbe à Papa", "Rhum-Raisins", "Potimarron", "Châtaigne", "Pollen Sauvage", "Riz au lait", "Caramel Beurre salé"]

var taste = ["Kiwi","Litchi","Mango","Mandarin","Melon","Mirabelle","Blackberry","Blueberry","Orange","Blood orange","Apricot","Pineapple","Banana","Lemon", "Lime", "Cherry","Cassis","Raspberry","Coco","Fig","Strawberry","Passion fruit","Pear","Rhubarb","Grapefruit","Honey - Pine nuts","Tiramisu","Chocolate ginger","Tagada strawberry","Nougat","Speculoos","Coffee","Milk jam","Pistachio","Licorice","Lavender","Caramel","Dragibus","Avocado","Chewing gum", "Olive","Chili chocolate", "Tomato - Basil","Cinnamon","White chocolate","Chocolate","Almond","Poppy","Cookies","Gingerbread","Cactus","Beer","Oreo", "Nutella", "Vanilla", "Candy floss", "Rum - Raisin", "Pumpkin", "Chestnut", "Wild pollen", "Rice pudding", "Salted butter caramel"]

taste = randomize(taste)
var housemates = ["user"];
var nb_selec_taste = 12
var selec_taste = selecTaste(taste)
var nb_attempt = 0;

console.log(selec_taste)

var rent = 100;
var sum = [0, 0, 0];
var polling_attempts = -1;
var max_attempts = 12;
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
  // html += "<div id='ma_page'><h1>Quelles glaces aimez-vous? </h1>";
  html += "<div id='ma_page'><h1>Which ice-cream flavor do you love ? </h1>";
  /* html += "<h2> Ce sondage a pour but de connaître la façon dont est répartie l'intensité de vos préférences dans un domaine qui intéresse beaucoup de monde : différents parfums de glace. Si vous n'aimez pas les sorbets ni les glaces, ce sondage va sans doute vous ennuyer et nous vous suggérons de ne pas le faire. Il demande 3 minutes maximum . </h2>" */
    html += "<h2> The aim of this survey is to observe the distribution of the intensity of your preferences in an interesting topic for many: ice-cream flavors. If you like neither ice-creams nor sorbets, this survey will probably bore you and we would suggest you not to do it. </h2>"
  /*html += " <div> <p class=\"property-info\">Première question : parmi les 12 parfums suivants : </br> </p>"*/
  html += " <div> <p class=\"property-info\">First question : from the following twelve flavors: </br> </p>"
  var id_pref = 0;
  var id_pire = 0;
  //html += "<div class="dropdown">"
  //html += "<button onclick="myFunction()" class="dropbtn">Dropdown</button>"
  //html += "<div id="myDropdown" class="dropdown-content">"
  /* html += "<div> Quel est le parfum que vous préférez  ? </br> " */
  html += "<div> Which one is your favorite? </br> "
  /*html +=  '<select name="pref" id="pref" onchange="change_text();">\n'
  html +=  "<option value=\"" + -1 + "\"> Choisir un parfum </option>" */
  html +=  '<select name="pref" id="pref" onchange="change_text();">\n'
  html +=  "<option value=\"" + -1 + "\"> Select a flavor: </option>"
    var j;
    for (j=0; j < nb_selec_taste; j++) {
        html += " <option value=\"" + j + "\">" + selec_taste[j] + "</option>"
    };
  html += "</select> </div></br>" /*
  html += "<div>Quel est le parfum que vous aimez le moins  ? </br>" 
  html +=  '<select name="pire" id="pire" onchange="change_text();">\n'
  html +=  "<option value=\"" + -1 + "\"> Choisir un parfum </option>"
    var j;
    for (j=0; j < nb_selec_taste; j++) {
        html += " <option value=\"" + j + "\">" + selec_taste[j] + "</option>"
    };
  html += "</select> </div></br>" 
  var pire = selec_taste[0];
    */
  var pref = selec_taste[0];
  
  /*html += "<div> <p id=\"change\" > Nous allons vous demander d'exprimer vos préférences sur les autres parfums, sachant que nous vous imposons la calibration suivante : votre parfum préféré vaut 100 points. Vous pouvez identifier le nombre de points x que vous attribuez à un parfum de la façon suivante : </br> x est le nombre tel qu'il vous est égal d'avoir ce parfum avec certitude, ou de subir un tirage au sort où vous aurez x % de chance d'avoir votre parfum préféré et 100 - x % de chance de ne rien avoir </p>"*/
  html += "<div> <p id=\"change\" > We will ask you to express your preferences among the other flavors, knowing the following constraint is imposed : your favorite flavor is worth 100 points. One way to evaluate the number of points to assosciate to one flavor is the following : </br> x is the number such that it is equivalent to you to either be certain of having this flavor, either having x% chance of getting this flavor and (100-x)% chance of getting nothing at all. </p>"
    html += " <p class=\"property-info\" id='exemple'></p> </div>"
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
    html += "            <button type='button' class='btn update' onclick='return checkBids()'>Envoyer</button>";
   // html += "            <input type=\"submit\" class='btn update' value=\"Valider\" />";
    html += "          </div>";
    html += "        </div>";
    html += "      </div>";
    html += "    </div>";
    html += "  </div>";
    html += " </form></div>";
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

function libre(i){
    var x = i
    pref = document.getElementById('pref').options[document.getElementById('pref').selectedIndex].value;
    if (x==pref){
        x += 5
    }
    return selec_taste[x]
}

function change_text(){
    pref = document.getElementById('pref').options[document.getElementById('pref').selectedIndex].value;
    $("#change").text(" We will ask you to express your preferences among the other flavors, knowing the following constraint is imposed : " + selec_taste[pref] + " worth 100 points. One way to evaluate the number of points to assosciate to one flavor is the following : </br> x is the number such that it is equivalent to you to either be certain of having this flavor, either having x% chance of getting this flavor and (100-x)% chance of getting nothing at all.
    var newText = "For example : </br>";
    /*newText += "* S'il vous est égal d'avoir une boule de " + libre(1) + ", ou d'avoir une chance sur deux d'avoir le parfum " + selec_taste[pref] +" et une chance sur deux de ne rien avoir, alors vous pouvez donner une valeur de 50 à " +  libre(1) + ".</br>"; */
     newText += "* If it is equivalent to you to be certain of either having " + libre(1) + ", either having 50% chance of getting " + selec_taste[pref] +" and 50% chance of getting nothing at all, then you can give 50 points to it. " +  libre(1) + ".</br>";
     newText += "* If it is equivalent to you to be certain of either having " + libre(2) + ", either having 30% chance of getting " + selec_taste[pref] +" and 70% chance of getting nothing at all, then you can give 30 points to it. " +  libre(2) + ".</br>";
     newText += "* If it is equivalent to you to be certain of either having " + libre(3) + ", either having 90% chance of getting " + selec_taste[pref] +" and 10% chance of getting nothing at all, then you can give 90 points to it. " +  libre(3) + ".</br>";
    $("#exemple").html(newText);
    /*for (j=0; j < nb_selec_taste; j++){
        if (j==pire){
            $("#values_0_" + j).val(0);
            //$(".nstSlider"+j).nstSlider("set_position",0);
        }else if (j==pref){
            $("#values_0_" + j).val(100);
            //$(".nstSlider"+j).nstSlider("set_position",100);
        } else {
            $("#values_0_" + j).val(50);
            //$(".nstSlider"+j).nstSlider("set_position",50);
        } 
        
        
    }*/
    /*
      $(".valuation_ipt"+i).blur(function() {
      var val = parseInt($(this).val());
      if (isNaN(val) || val<=0) val = 0;
      if (val>rent) val=rent;
      $(this).val(val);
      $(this).parent().parent().find(".nstSlider").nstSlider("set_position", val);
      updateSum($(this).data('id'));
  }); */
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

    $('#update-results-msg').text("Your request is being processed. This may take a moment.");
    $('#results-table').html('');
    $('#fairness-table').html('');
    $('#submit-demo').hide();
    /*displayError("Votre participation a bien été prise en compte, merci\n Vous pourrez recommencer dans 2 secondes","bidding-error-0");*/
    displayError("Your participation have been taken into account. You will be able to restart in two seconds.","bidding-error-0");
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
    $("#ma_page").remove();
  $('#essai-' + nb_attempt).remove();
    nb_attempt += 1;
    selec_taste = selecTaste(taste);
    createBiddingSections();

}, 2200)
    
    
  
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
