var height = 0;
$('messages p').each(function(i, value){
    height += parseInt($(this).height());
});

height += '';

$('div').animate({scrollTop: height});