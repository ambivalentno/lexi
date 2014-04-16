function onYouTubePlayerReady(playerId) {
    var player = $('#video-wrapper').find('embed').get(0);
    player.addEventListener('onStateChange', 'handler')
}

function handler(state) {
    if (state === 0) {
        $('#questions').slideDown();
    }
}
