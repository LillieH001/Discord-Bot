const { createAudioPlayer } = require('@discordjs/voice');

var connection;
var player = createAudioPlayer();
var resource;
var connectionstatus = 0;
var queue = [];
var titles = [];
var nowplaying = '';

module.exports = {
    connection,
    player,
    resource,
    connectionstatus,
    queue,
    titles,
    nowplaying
};