$('.filter').click(function() {
  $('.filter-modal').addClass('-active');
});

$('.close').click(function() {
  $('.filter-modal').removeClass('-active');
});

$('.back').on('click', function() {
  var current = $('.js-page.-active');
  var prev = current.prev('.js-page');
  current.addClass('_hidden');
  current.one('transitionend', function(){
    current.removeClass('-active');
    $('body').removeClass('-invertedbg');
    current.remove();
    prev.removeClass('_hidden').addClass('-active');
    $('.nav-bar').removeClass('-negative');
    $('.ball-animation').addClass('-active -reverse').one('animationend', function(){
      $(this).removeClass('-active -reverse');
    });
  });
})

document.addEventListener('touchmove', function(e) {
  return false;
});
