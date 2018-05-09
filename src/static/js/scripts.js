$('.filter').click(function() {
  $('.filter-modal').addClass('-active');
});

$('.close').click(function() {
  $('.filter-modal').removeClass('-active');
});

$('.back').on('click', function() {
  $('.nav-bar').removeClass('-negative');
  var current = $('.js-svg-root.-active');
  var prev = current.prev('.js-svg-root');
  current.addClass('-hidden');
  current.one('transitionend', function(){
    current.removeClass('-active');
    $('body').removeClass('-invertedbg');
    current.remove();
    prev.removeClass('-hidden').addClass('-active');
    $('.ball-animation').addClass('-active -reverse').one('animationend', function(){
      $(this).removeClass('-active -reverse');
    });
  });
})

document.addEventListener('touchmove', function(e) {
  return false;
});
