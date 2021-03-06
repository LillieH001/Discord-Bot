const { SlashCommandBuilder, EmbedBuilder } = require('discord.js');
var globalsaudio = require('../globals/audio.js');

module.exports = {
	data: new SlashCommandBuilder()
		.setName('stop')
		.setDescription('Stops the current playing song')
        .setDMPermission(false),
	async execute(interaction) {
        await interaction.deferReply();

        globalsaudio.connection.destroy();
        globalsaudio.queue = [];
        globalsaudio.titles = [];
        globalsaudio.nowplaying = '';
        globalsaudio.connectionstatus = 0;

        const embed = new EmbedBuilder()
            .setColor('#FFC0DD')
            .setTitle('Music Player')
            .setDescription('Stopped play audio and disconnected from voice chat')
            .setTimestamp()

        await interaction.editReply({ embeds: [embed] });
	},
};