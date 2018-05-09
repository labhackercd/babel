// var VirtualScroll = require('virtual-scroll');
//
// var targetY = 0;
// var scroll = VirtualScroll();
//
// scroll.on(function(e, i) {
//   var scrollable = d3.select('.js-svg-root:not(.-hidden) g');
//   var chartHeight = scrollable.node().getBoundingClientRect().height;
//
//   targetY = Math.min(0, e.y);
//   var minY = 0 - chartHeight;
//   targetY = Math.max(targetY, minY);
//
//   if (targetY >= chartHeight) {
//     VirtualScroll.destroy();
//   }
//
//   var scale = (1 + Math.abs(targetY) / chartHeight);
//   console.log(chartHeight - Math.abs(targetY));
//
//   scrollable.attr('transform', `translate(0, ${targetY}) scale(${scale})`);
// })

// $('main').pressAndHold({
// 	holdTime: 1000,
// 	progressIndicatorRemoveDelay: 900,
// 	progressIndicatorColor: "blue",
// 	progressIndicatorOpacity: 0.3
// })
