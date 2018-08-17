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

    let str_traits = ' ';
    for (let trait of traits) {
        str_traits += ('<li>' + trait + '</li>');

        let t = trait.replace(/\s+/g, '-');

        let toolStr = "#tooltip-" + t;
        $(toolStr).show();
    }

    let str_dogs = ' ';
    let search_dogs = [];
    for (let dog of dogs) {
        str_dogs += '<li>' + dog[0] + '</li>';
        search_dogs.push(dog[0]);

        let d = dog[0].replace(/\s+/g, '-');

        let topStr = "#top-ten-" + d;
        // $(topStr).show();
        document.querySelector(topStr).style.display = "block";

    }
    let response = ('<h2>Traits and dog breeds that match your preference!</h2>');

    $(".matches-container").show();
    $(".dog-quiz").toggle();
    // $("#retake-quiz").attr("hidden", false);
    $("#dog-matches").html(response);

    console.log(dogs[0][0]);
    
    // $("#breed-desc").html(dogs[0][0]);


    $.get('/call-api.json',
          { search_dogs: search_dogs }, 
          updateDogCards);
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

$(function () {
  $('[data-toggle="tooltip"]').tooltip()
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




