(function($) {
  $(function() {
    $('.toggle-overlay').click(function() {
	console.log('Dando click');
      $('aside').toggleClass('open');
    });
  });
})(jQuery);
