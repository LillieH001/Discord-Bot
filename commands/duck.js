const { SlashCommandBuilder } = require('@discordjs/builders');
const { MessageEmbed, MessageActionRow, MessageButton } = require('discord.js');

module.exports = {
	data: new SlashCommandBuilder()
		.setName('duck')
		.setDescription('Posts a random duck picture'),
	async execute(interaction) {
        await interaction.deferReply();
        const res = await fetch('https://random-d.uk/api/v2/random');
        if (res.ok) {
            const data = await res.json();
            const embed = new MessageEmbed()
                .setColor('#FFC0DD')
                .setTitle('Duck Pics')
                .setImage(data.url)
                .setTimestamp()
            const row = new MessageActionRow()
                .addComponents(
                    new MessageButton()
                        .setLabel('View Original Image')
                        .setStyle('LINK')
                        .setURL(data.url)
                );
            await interaction.editReply({ embeds: [embed], components: [row] });
        }
	},
};