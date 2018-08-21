"use strict";
function updateDogCards(dogs) {
    let response = ' ';
    for (let dog of dogs) {
        response += ('<div class="col-3"><div class="card" style="width: 18rem;">' +
                     '<img class="card-img-top" src="' + dog['photos'] + 
                     '" alt="Card image cap"><div class="card-body">' +
                     '<h5 class="card-title">' + dog['name'] +
                     '</h5><p class="card-text">' + dog['desc'] +
                     '</p><a href="#" class="btn btn-primary">Read More!</a>' +
                     '</div></div></div>')
    }

    $("#dog-cards").html(response);
}


function getDogBreeds(results) {
    let traits = results[0];
    let dogs = results[1];

    for (let trait of traits) {
        let t = trait.replace(/\s+/g, '-');
        let toolStr = "#tooltip-" + t;
        $(toolStr).show();
    }

    let search_dogs = [];
    let breeds = ' ';

    for (let dog of dogs) {
        let clean_desc = dog[1];
        let b = dog[0];

        let pictures = `data-pic="${dog[2]}"`;


        clean_desc = clean_desc.replace(/"/g, "&quot;");
        let desc = `data-desc="${clean_desc}"`;
        breeds += ('<a href="#" class="btn btn-primary top-ten-button" value="'+dog[0]+'" '+ desc +' '+ pictures +'>' + dog[0] + '</a></br>');
        search_dogs.push(dog[0]);
    }
    let response = ('<h2>Traits and dog breeds that match your preference!</h2>');

    console.log(search_dogs);
    $.get('/call-api.json',
          { search_dogs: search_dogs }, 
          updateDogCards);

    $(".matches-container").show();
    $(".dog-quiz").toggle();
    // $("#retake-quiz").attr("hidden", false);
    $("#dog-matches").html(response);

    $("#top-ten-breeds").html(breeds);
    $("#top-ten-desc").html(dogs[0][1]);
    $("#top-ten-img").attr("src", dogs[0][2]);
}

function getDogTraits(evt) {
    evt.preventDefault();

    const formInputs = {
        "pos_trait1": $("#pos_trait1").val(),
        "pos_trait2": $("#pos_trait2").val(),
        "pos_trait3": $("#pos_trait3").val(),
        "pos_trait4": $("#pos_trait4").val(),
        "pos_trait5": $("#pos_trait5").val(),
    };

    $.post('/dog-list.json',
           formInputs,
           getDogBreeds);
}

$("#traits-form").on("submit", getDogTraits);

// function toggleQuiz(evt) {
//     evt.preventDefault();

//     $("#dog-matches").html('');
//     $(".dog-quiz").toggle();
//     $("#retake-quiz").attr("hidden", true);
// }

// $("#retake-quiz").on("click", toggleQuiz);

function breedInfo(evt) {
    evt.preventDefault();

    let dog = $(this).attr("data-desc");
    let pic = $(this).attr("data-pic");
    $("#top-ten-desc").html(dog);
    $("#top-ten-img").attr("src", pic);
}

$("#top-ten-breeds").on("click", "a", breedInfo);

$(function () {
  $('[data-toggle="tooltip"]').tooltip();
});

var current_fs, next_fs; //fieldsets
var left, opacity, scale; //fieldset properties which we will animate
var animating; //flag to prevent quick multi-click glitches

$(".next").click(function(){
    if(animating) return false;
    animating = true;
    
    current_fs = $(this).parent();
    next_fs = $(this).parent().next();
    
    //show the next fieldset
    next_fs.show(); 
    //hide the current fieldset with style
    current_fs.animate({opacity: 0}, {
        step: function(now, mx) {
            //as the opacity of current_fs reduces to 0 - stored in "now"
            //1. scale current_fs down to 80%
            scale = 1 - (1 - now) * 0.2;
            //2. bring next_fs from the right(50%)
            left = (now * 50)+"%";
            //3. increase opacity of next_fs to 1 as it moves in
            opacity = 1 - now;
            current_fs.css({
        'transform': 'scale('+scale+')',
        'position': 'absolute'
      });
            next_fs.css({'left': left, 'opacity': opacity});
        }, 
        duration: 800, 
        complete: function(){
            current_fs.hide();
            animating = false;
        }, 
        //this comes from the custom easing plugin
        easing: 'easeInOutBack'
    });
});


