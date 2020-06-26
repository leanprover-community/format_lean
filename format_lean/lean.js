var dragging = false;

$('#dragbar').mousedown(function(e){
  e.preventDefault();
  dragging = true;
  var content = $('#content');
  var dragbar = $('#dragbar');
  var tsw = $('#tactic_state_wrapper');
  console.log("Resizing...");
  $(document).mousemove(function(ex){
    content.css("width", ex.pageX +2);
    dragbar.css("left", ex.pageX +2);
    tsw.css("margin-left", ex.pageX +2);
  });
});

$(document).mouseup(function(e){
  if (dragging) 
  {
    $(document).unbind('mousemove');
    dragging = false;
  }
});

$(document).ready(function() {
    $("div.definition_text").click(
           function() {
               $(this).siblings("div.definition_lean").slideToggle()
           })
    $("div.example_text").click(
           function() {
               $(this).siblings("div.example_lean").slideToggle()
           })
    $("div.lemma_text").click(
           function() {
               $(this).siblings("div.lemma_lean").slideToggle()
           })
    $("div.theorem_text").click(
           function() {
               $(this).siblings("div.theorem_lean").slideToggle()
           })
    $("span.proof_item_text").click(
           function() {
               $(this).siblings("div.proof_item_lean").slideToggle()
           })

    $("span.tactic_left").click(
           function() {
			   var width = $('#content').css("width");
               $("div#tactic_state").html(
				   $(this).siblings("span.tactic_state_left").html());
			   $('#content').css("width", width);
           })

    $("span.tactic_right").click(
           function() {
			   var width = $('#content').css("width");
               $("div#tactic_state").html(
				   $(this).siblings("span.tactic_state_right").html())
			   $('#content').css("width", width);
           })
});
