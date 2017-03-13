$(document).ready(function(){
  $("#train-stop").click(function() {
    $(".loader").fadeOut(2000); 
  });

  $(".loader img").click(function (e) {
    e.stopPropogation();
  })
  
  $(".loader").click(function () {
    $(".loader").fadeOut(2000); 
  })
});