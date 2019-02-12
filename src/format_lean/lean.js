$(document).ready(function() {
    $("div.definition_text").click(
           function() {
               $(this).siblings("div.definition_lean").slideToggle()
           })
    $("div.lemma_text").click(
           function() {
               $(this).siblings("div.lemma_lean").slideToggle()
           })
    $("span.proof_item_text").click(
           function() {
               $(this).siblings("div.proof_item_lean").slideToggle()
           })

    $("span.tactic_left").click(
           function() {
               $("div.tactic_state").html(
				   $(this).siblings("span.tactic_state_left").html())
           })

    $("span.tactic_right").click(
           function() {
               $("div.tactic_state").html(
				   $(this).siblings("span.tactic_state_right").html())
           })
});
