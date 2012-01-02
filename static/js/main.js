(function ($, window, undefined) {
  function setupClouds() {
    $('#p-clouds #upper-left').plaxify({xRange: 16, yRange: 4})
    $('#p-clouds #upper-right').plaxify({xRange: 12, yRange: 6, invert: true})
    $('#p-clouds #mid-left').plaxify({xRange: 6, yRange: 8})
    $('#p-clouds #mid-right').plaxify({xRange: 10, yRange: 4, invert: true})
    $('#p-clouds #lower-left').plaxify({xRange: 6, yRange: 8})
    $('#p-clouds #lower-right').plaxify({xRange: 4, yRange: 6})
    $.plax.enable()
  }

  function setupEyes() {
    $('#p-yg #left-eye').plaxify({xRange: 14, yRange: 6})
    $('#p-yg #inner-left-eye').plaxify({xRange: 26, yRange: 10})
    $('#p-yg #right-eye').plaxify({xRange: 14, yRange: 6})
    $('#p-yg #inner-right-eye').plaxify({xRange: 26, yRange: 10})
    $.plax.enable()
  }

  $(document).ready(function() {
    setupEyes()

    $('#tease').each(function () {
        var self = $(this)
          , win = $(window)

        self
          .css('left', (win.width()  / 2) - (self.width()  / 2))
          .css('top',  (win.height() / 2) - (self.height() / 2))

        return false
    })
  })
})(jQuery, window)

