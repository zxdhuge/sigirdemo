$(document).ready(function(){
    var classTitle = $("h3.title");
    classTitle.click(function(){
        $(this).next("div").slideToggle("slow");
    });
})
