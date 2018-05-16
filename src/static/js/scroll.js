var scrollPosition = 0;
var maxScroll = 30000;
var maxScale = 600;


var hammertime = new Hammer($(".wrapper")[0]);

hammertime.get('pan').set({ direction: Hammer.DIRECTION_ALL });

hammertime.on('panup pandown', function(e) {
  scrollPosition = scrollPosition - e.deltaY;
  if (scrollPosition < 0) {
    scrollPosition = 0;
  } else if (scrollPosition > maxScroll) {
    scrollPosition = maxScroll;
  }

  var scrollRatio = scrollPosition / maxScroll;

  var svg = $('.js-page.-active > .js-svg-root')[0];
  var scale = svg.style.getPropertyValue('transform').match(/scale\((?<value>.+)\)/);

  if (scale === null) {
    scale = 1;
  } else {
    scale = maxScale ** scrollRatio;
  }

  $(svg).css('transform', `scale(${scale})`);
});
