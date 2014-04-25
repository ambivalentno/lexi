function onYouTubePlayerReady(playerId) {
    var player = $('#video-wrapper').find('embed').get(0);
    player.addEventListener('onStateChange', 'handler')
}

function handler(state) {
    if (state === 0) {
		$("html, body").animate(
			{scrollTop: $('#questions').position().top},
			2000
		);
    }
}
