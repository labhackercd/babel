function loadData(url, callback) {
  var newArray = [];
  // $.getJSON(url).done(function(json) {
  //   callback(json);
  // })
  // beforeSend: function() {
  //   console.log('oi');
  // },
  // success: function() {
  //   callback(json);
  // }

  $.ajax({
    type: "GET",
    url: url,
    data: "json",
    beforeSend: function() {
      $('.hex-loading').addClass('-visible');
    },
    success: function(json){
      $('.hex-loading').removeClass('-visible');
      callback(json);
    }
  });

  return newArray;
}

var drawHexagon = d3.svg.line()
  .x(function(d) { return d.x; })
  .y(function(d) { return d.y; })
  .interpolate("cardinal-closed")
  .tension("0.25");

function addPage(element) {
  $('.wrapper').append(element);
  $('.js-page').removeClass('-active').addClass('-hidden');
  element.removeClass('-hidden').addClass('-active');
}

function zoomInAnimation(element) {
  var bbox = element.getBoundingClientRect();
  var hexPositionTop = bbox.top + bbox.height / 2;
  var hexPositionLeft = bbox.left + bbox.width / 2;
  $(element).parent().addClass('-active');
  var ball = $('.ball-animation');
  ball.addClass('-active')
    .css('top', hexPositionTop + 'px')
    .css('left', hexPositionLeft + 'px');
  ball.one('animationend', function(){
    $('.ball-animation').removeClass('-active');
    $('body').addClass('-invertedbg');
    $('.nav-bar').addClass('-negative');
  });
}

function drawCanvas(selector, chartName) {
  return d3.select(selector)
    .append("svg")
    .classed('js-page', true)
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


function tokensChart(tokenId) {
  loadData('/static/babel.json', function(data) {
    var canvas = drawCanvas('.wrapper','authors');
    var hexagonGroup = createHexagonGroup(canvas, data);
    addHexagons(hexagonGroup, 90);
    positionHexagon(hexagonGroup);
    addText(hexagonGroup);
    $('.ball-animation').on('animationend', function() {
      showHexagonGroup(hexagonGroup);
    })
    hexagonOnClick(hexagonGroup, function(data) {
      $('.ball-animation').addClass('-invertedbg');
      $('.ball-animation').one('animationend', function(){
        $('body').removeClass('-invertedbg');
        $('.nav-bar').removeClass('-negative');

        authorsChart(data.id);
      });
    })
  })
}

function authorsChart(authorId) {
  loadData("/static/authors.json", function(data) {
    var speechesPage = $(document.createElement('div'))
    speechesPage.addClass('speeches js-page');
    addPage(speechesPage);

    var hexGrid = $("<div class='hex-grid'>");
    data.forEach(function(element, index) {
      var hex = $(`<div class="hex js-manifestation" data-manifestation-id=${element.id}>`);

      var header = $('<div class="header">');
      header.append($('<div class="icon">'));

      var headerContent = $('<div class="content">');
      headerContent.append($(`<span class="date">${element.date}</span>`));
      headerContent.append($(`<span class="time">${element.time}</span>`));

      header.append(headerContent);

      hex.append(header);
      hex.append($(`<p>${element.preview}</p>`));
      hexGrid.append(hex);
    })

    speechesPage.append(hexGrid);
    $('.js-manifestation').on('click', function(e) {
      manifestationPage($(this).data('manifestationId'));
    })

    var manifestationPageElement = $(document.createElement('div'))
    manifestationPageElement.addClass('manifestation-page js-page');
    $('main').append(manifestationPageElement);
  })
}

function manifestationPage(manifestationId) {
  loadData('/static/manifestation.json', function(data) {
    var manifestationPage = $('.manifestation-page');
    manifestationPage.append($(`<div class='close-manifestation'></div>`));
    manifestationPage.append($(`<strong class='date'>${data.date}  às </strong>`));
    manifestationPage.append($(`<strong class='time'>${data.time}</strong>`));
    manifestationPage.append($(`<p>${data.content}</p>`));
    manifestationPage.addClass('-open');

    $('.close-manifestation').on('click', function() {
      manifestationPage.removeClass('-open');
    });
  })
}

loadData("/visualizations/tokens/", function(data) {
  var canvas = drawCanvas('.wrapper', 'token');
  var hexagonGroup = createHexagonGroup(canvas, data);
  addHexagons(hexagonGroup, 90);
  hexagonOnClick(hexagonGroup, function(data) {
    var currentPage = $(data.element).closest('.js-page');
    currentPage.removeClass('-active');
    $('.ball-animation').one('animationend', function(){
      currentPage.addClass('-hidden');
    });
    tokensChart(data.id);
  });
  positionHexagon(hexagonGroup);
  addText(hexagonGroup);
  showHexagonGroup(hexagonGroup);
})
