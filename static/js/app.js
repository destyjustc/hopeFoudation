$( document ).ready(function() {
	var ret = $('#winner').text();
	console.log('winner is', ret);
    var option = {
		speed : 10,
		duration : 3,
		stopImageNumber : ret,
		startCallback : function() {
			console.log('start');
		},
		slowDownCallback : function() {
			console.log('slowDown');
		},
		stopCallback : function($stopElm) {
			console.log('stop');
		}
	}
	rouletter = $('div.roulette').roulette(option);
	setTimeout(() => {
		rouletter.roulette('start');	
	}, 500);
});