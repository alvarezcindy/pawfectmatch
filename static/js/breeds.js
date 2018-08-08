"use strict";

function getDogBreeds(results) {
    let traits = results[0];
    let dogs = results[1];

    let str_traits = ' ';
    for (let trait of traits) {
        str_traits += ('<li>' + trait + '</li>');
    }

    let str_dogs = ' ';
    for (let dog of dogs) {
        str_dogs += '<li>' + dog + '</li>';
    }

    let response = ('<h3>You said the following traits were most important to you:</h3>' +
                    str_traits +
                    '<h2>Dog breeds that match your preferences!</h2>' +
                    str_dogs
                    );

    $("#dog-matches").html(response);
    $("#dog-traits-form").html('Take Quiz Again!');
}

function getDogTraits(evt) {
    evt.preventDefault();

    var formInputs = {
        "pos_trait1": $("#pos_trait1").val(),
        "pos_trait2": $("#pos_trait2").val(),
        "pos_trait3": $("#pos_trait3").val(),
    };

    $.post('/dog-list.json',
           formInputs,
           getDogBreeds);
}

$("#dog-traits-form").on("submit", getDogTraits);