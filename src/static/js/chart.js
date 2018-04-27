function loadData(callback) {
  var newArray = [];
  $.getJSON('/static/babel.json').done(function(json) {
    json.forEach(function(element, index) {
      var previous = newArray[index - 1];
      var size = 1;
      if (previous) {
        size = previous.size * 0.7;
      }
      data = {
        "id": element.id,
        "token": element.token,
        "occurrences": element.occurrences,
        "size": size
      }
      newArray.push(data);
    })
    callback(newArray);
  })
  return newArray;
}

var drawHexagon = d3.svg.line()
  .x(function(d) { return d.x; })
  .y(function(d) { return d.y; })
  .interpolate("cardinal-closed")
  .tension("0.25");

function zoomInAnimation(element) {
  var bbox = element.getBoundingClientRect();
  var hexPositionTop = bbox.top + bbox.height / 2;
  var hexPositionLeft = bbox.left + bbox.width / 2;
  $(element).parent().addClass('-active');
  var ball = $('.ball-animation');
  ball.addClass('-active')
    .css('top', hexPositionTop + 'px')
    .css('left', hexPositionLeft + 'px');
  ball.on('transitionend', function(){
    $('.ball-animation').removeClass('-active');
    $('body').addClass('-invertedbg');
  });
}

function drawCanvas(selector, chartName) {
  return d3.select(selector)
    .append("svg")
    .classed("js-svg-root", true)
    .classed('-active', true)
    .attr("width", "100%")
    .attr("height", "100%")
    .attr("data-chart-name", chartName)
    .append('g')
      .attr("transform-origin", "center top");
}

function createHexagonGroup(canvas, data) {
  return canvas.selectAll("rect")
    .data(data)
    .enter()
      .append('g')
      .attr('id', function(d, i) {
        var chartName = $(this).closest('.js-svg-root').data('chartName');
        return `${chartName}-hexagon-${d.id}`;
      })
      .classed('-hidden', true)
      .classed('-small', true)
      .attr("transform-origin", "center top");
}

function hexagonOnClick(hexagonGroup, callback) {
  hexagonGroup.on('click', function(d, i) {
    zoomInAnimation(this);
    callback(d);
  })
}

function addHexagons(hexagonGroup, radius) {
  hexagonGroup.append("path")
  .attr("fill", "white")
  .attr("d", function(d, i) {
    var h = (Math.sqrt(3)/2),
      scaledRadius = radius * d.size,
      hexagonData = [
        { "x": scaledRadius,   "y": 0},
        { "x": scaledRadius / 2,  "y": scaledRadius * h},
        { "x": - scaledRadius / 2,  "y": scaledRadius * h},
        { "x": - scaledRadius,  "y": 0},
        { "x": - scaledRadius / 2,  "y": - scaledRadius * h},
        { "x": scaledRadius / 2, "y": - scaledRadius * h}
      ];
      return drawHexagon(hexagonData);
  })
}

function positionHexagon(hexagonGroup) {
  hexagonGroup.attr('transform', function(d, i) {
    d['element'] = this;
    bbox = this.getBoundingClientRect();

    var translateX = 120;
    var translateY = 140;

    var previous = hexagonGroup.data()[i - 1];
    if (previous) {
      var chartName = $(this).closest('.js-svg-root').data('chartName');
      var previousBBox = previous.element.getBoundingClientRect();
      previous = d3.select(`#${chartName}-hexagon-${previous.id}`);
      previousTransform = d3.transform(previous.attr("transform"));
      translateX = previousTransform.translate[0];
      translateY = previousTransform.translate[1] + bbox.height;
      if (i % 2 !== 0) {
        translateX = translateX + bbox.width;
      } else {
        translateX = translateX - bbox.width;
      }
    }
    return `translate(${translateX}, ${translateY})`;
  })
}

function addText(hexagonGroup) {
  hexagonGroup.append("foreignObject")
    .attr('x', function(d, i) { return d.element.getBBox().x; })
    .attr('y', function(d, i) { return d.element.getBBox().y; })
    .attr('width', function(d, i) { return d.element.getBBox().width; })
    .attr('height', function(d, i) { return d.element.getBBox().height; })
    .attr('transform', function(d, i) { return `scale(${d.size})`})
    .append('xhtml:div')
      .attr("class", 'text-box')
      .append('xhtml:p')
        .attr('class', 'text')
        .text((d) => {return d.token;})
}

function showHexagonGroup(hexagonGroup) {
  hexagonGroup.each(function(d, i) {
    setTimeout(function() {
      $(d.element).removeClass('-hidden');
    }, i * 150)
  })
}


function authorsChart(authorId) {
  loadData(function(data) {
    console.log(data);
    var canvas = drawCanvas('main','authors');
    var hexagonGroup = createHexagonGroup(canvas, data);
    addHexagons(hexagonGroup, 90);
    positionHexagon(hexagonGroup);
    addText(hexagonGroup);
    $('.ball-animation').on('transitionend', function() {
      showHexagonGroup(hexagonGroup);
    })
  })
}

loadData(function(data) {
  var canvas = drawCanvas('main', 'token');
  var hexagonGroup = createHexagonGroup(canvas, data);
  addHexagons(hexagonGroup, 90);
  hexagonOnClick(hexagonGroup, function(data) {
    var essevege = $(data.element).closest('.js-svg-root');
    essevege.removeClass('-active');
    $('.ball-animation').on('transitionend', function(){
      essevege.addClass('-hidden');
      $('.nav-bar').addClass('-black');
    });
    authorsChart(data.id);
  });
  positionHexagon(hexagonGroup);
  addText(hexagonGroup);
  showHexagonGroup(hexagonGroup);
})
