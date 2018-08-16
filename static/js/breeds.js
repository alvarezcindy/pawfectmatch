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
    }

    let str_dogs = ' ';
    let search_dogs = [];
    for (let dog of dogs) {
        str_dogs += '<li>' + dog[0] + '</li>';
        search_dogs.push(dog[0]);
    }
    let response = ('<h3>You said the following traits were most important to you:</h3>' +
                    str_traits +
                    '<h2>Dog breeds that match your preferences!</h2>' +
                    str_dogs 
                    );

    $(".dog-quiz").toggle();
    $("#retake-quiz").attr("hidden", false);
    $("#dog-matches").html(response);

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

function toggleQuiz(evt) {
    evt.preventDefault();

    $("#dog-matches").html('');
    $(".dog-quiz").toggle();
    $("#retake-quiz").attr("hidden", true);
}

$("#retake-quiz").on("click", toggleQuiz);





