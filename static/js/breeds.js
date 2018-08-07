"use strict";

function getDogBreeds(results) {
    let status = results;
    $('#form-results').html('<p> hello </p>');

function getDogTraits(evt) {
    evt.preventDefault();

    var formInputs = {
        "pos_trait1": $("#pos_trait1").val(),
        "pos_trait2": $("#pos_trait2").val(),
        "pos_trait3": $("#pos_trait3").val(),
    };

    $.post("/dog-list.json",
           formInputs,
           getDogBreeds);
}

$("#dog-traits-form").on("submit", getDogTraits);