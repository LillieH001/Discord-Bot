const { SlashCommandBuilder, EmbedBuilder } = require('discord.js');
var globalsaudio = require('../globals/audio.js');

module.exports = {
	data: new SlashCommandBuilder()
		.setName('pause')
		.setDescription('Pauses the current playing song')
        .setDMPermission(false),
	async execute(interaction) {
        await interaction.deferReply();

        globalsaudio.player.pause();

        const embed = new EmbedBuilder()
            .setColor('#FFC0DD')
            .setTitle('Music Player')
            .setDescription('Paused playing audio')
            .setTimestamp()

        await interaction.editReply({ embeds: [embed] });
	},
};
