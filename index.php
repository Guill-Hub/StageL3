<!DOCTYPE html>
<!--[if lt IE 7]>      <html class="no-js lt-ie9 lt-ie8 lt-ie7"> <![endif]-->
<!--[if IE 7]>         <html class="no-js lt-ie9 lt-ie8"> <![endif]-->
<!--[if IE 8]>         <html class="no-js lt-ie9"> <![endif]-->
<!--[if gt IE 8]><!--> <html class="no-js"> <!--<![endif]-->
<html>
  <head>
    <title>Live Demo: Assign selec_taste and Share Rent - Spliddit</title>
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
    <meta name="description" content="Spliddit&#x27;s rent calculator helps roommates to assign selec_taste and share rent when moving into a new house or apartment. With the live demo, you can experiment with the calculator and view the results on a single screen in a matter of seconds.">
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

var taste = [" Kiwi" ," Litchi", "Mange", "Mandarine", "Melon", "Mirabelle", "Mûre", "Myrtille", "Orange", "Orange sanguine","Abricot","Ananas","Banane","Citron", "Citron Vert", "Cerise", "Cassis" , "Cassis" , "Framboise", "Coco", "Figue", "Fraise", "Fruit de la passion", "Poire", "Rhubarbe", "Pamplemousse"]
taste = randomize(taste)
var housemates = ["user"];
var nb_selec_taste = 7
var selec_taste = [];
var i;
for (i = 0; i < nb_selec_taste; i++){
    selec_taste.push(taste[i]);
}

console.log(selec_taste)

var rent = 100;
var sum = [0, 0, 0];
var polling_attempts = -1;
var max_attempts = 15;
var id = -1;
var pwd = "";

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
  var bidding_text = "Sur une échelle de 0 à " + rent + " 100 à quel point serez-vous heureux d'obtenir une boule de glace d'un parfum donné. Il faut ensuite normaliser ces valeurs avec le bonton rescale"
  var housemates_copy = housemates;
  var bidding_sections = new Array();
  var html = "";
  var i = 0;
    html += "  <div>";
    html += "    <p>" + bidding_text + "</p>";
    html += "    <p id='bidding-error-" + i + "' class='error-msg error-text'></p>";
    html += "    <div class='range-calc'>";
    html += "      <div class='calculations'>";
    var j;
    for (j=0; j < selec_taste.length; j++) {
      html += "      <div class='calc-row'>";
      html += "        <div class='name'>";
      html += "          <p>" + selec_taste[j] + "</p>";
      html += "        </div>";
      html += "        <div class='nstSlider range nstSlider" + i + "' data-range_min='0' data-range_max='" + rent + "' data-cur_min='0' data-id='" + i + "'>";
      html += "          <div class='leftGrip'></div>";
      html += "        </div>";
      html += "        <span class='calc-value'>";
      html += "          <input type='text' data-id='" + i + "' id='values_" + i + "_" + j + "' name='values[" + i + "][" + j + "]' class='valuation_ipt leftLabel cost valuation_ipt"+i+"'>"
      html += "        </span>";
      html += "      </div>";
    }
    html += "        <div class='calc-control'>";
    html += "          <div class='btns'>";
    html += "            <button type='button' class='btn reset' onclick='return resetSliders(" + i + ")'>Reset</button>";
    html += "            <button type='button' class='btn update' onclick='return updateSliders(" + i + ")'>Rescale</button>";
    html += "            <button type='button' class='btn update' onclick='return checkSliders(" + i + ")'>Continue</button>";
    html += "          </div>";
    html += "          <div class='totals'>";
    html += "            <p><strong>Current Total:</strong> <span id = 'sum-" + i + "'>0</span></p>";
    html += "            <p><strong>Target:</strong> " + rent + "</p>";
    html += "          </div>";
    html += "        </div>";
    html += "      </div>";
    html += "    </div>";
    html += "  </div>";
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
    return true;
  } else {
    displayError("Please make sure your evaluations add to " + rent + ".", "bidding-error-"+i);
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
    $.ajax({
      type: "POST",
      url: "../../../demo/create",
      data: { app: "rent", input: buildJSON() }
    }).fail(function() {
      $('#update-results-msg').text("We encountered an internal server error. Sorry for the inconvenience.");
      $('#submit-demo').show();
    });
  } else {
    displayError("Some participants haven't entered their evaluations, or have errors (checkmarks indicate those who have successfully entered their evaluations). Once everyone is done, press the submit button again.", "update-results-msg");
  }
}

function buildJSON() {
  var json = {}
  json['rent'] = rent;
  json['selec_taste'] = selec_taste;
  json['bids'] = {};
  for (var j = 0; j < nb_selec_taste; j++) {
      value = parseInt($('#values_'+0+'_'+j).val(), 10);
      json['bids'][selec_taste[j]] = value;      
    }
    console.log(json)
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
        padding: 0.2em
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