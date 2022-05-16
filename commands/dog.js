const { SlashCommandBuilder } = require('@discordjs/builders');
const { MessageEmbed, MessageActionRow, MessageButton } = require('discord.js');
const axios = require('axios');

module.exports = {
	data: new SlashCommandBuilder()
		.setName('dog')
		.setDescription('Posts a random dog picture')
        .addStringOption(option =>
            option.setName('source')
                .setDescription('Choose the dog pictures source')
                .setRequired(true)
                .addChoices(
                    { name: 'Dog.Ceo', value: 'dog_ceo' },
                    { name: 'Nekos.Life',  value: 'nekos_life' },
                    { name: 'AlexFlipnote.Dev',  value: 'alexflipnote_dev' }
                )),
	async execute(interaction) {
        await interaction.deferReply();
        const source = interaction.options.getString('source');
        if (source == "dog_ceo") {
            const response = await axios.get('https://dog.ceo/api/breeds/image/random');
            if (response.status == 200) {
                const embed = new MessageEmbed()
                    .setColor('#FFC0DD')
                    .setTitle('Dog Pics')
                    .setImage(response.data.message)
                    .setTimestamp()
                const row = new MessageActionRow()
                    .addComponents(
                        new MessageButton()
                            .setLabel('View Original Image')
                            .setStyle('LINK')
                            .setURL(response.data.message)
                    );
                await interaction.editReply({ embeds: [embed], components: [row] });
            }
        }
        if (source == "nekos_life") {
            const response = await axios.get('https://nekos.life/api/v2/img/woof');
            if (response.status == 200) {
                const embed = new MessageEmbed()
                    .setColor('#FFC0DD')
                    .setTitle('Dog Pics')
                    .setImage(response.data.url)
                    .setTimestamp()
                const row = new MessageActionRow()
                    .addComponents(
                        new MessageButton()
                            .setLabel('View Original Image')
                            .setStyle('LINK')
                            .setURL(response.data.url)
                    );
                await interaction.editReply({ embeds: [embed], components: [row] });
            }
        }
        if (source == "alexflipnote_dev") {
            const response = await axios.get('https://api.alexflipnote.dev/dogs');
            if (response.status == 200) {
                const embed = new MessageEmbed()
                    .setColor('#FFC0DD')
                    .setTitle('Dog Pics')
                    .setImage(response.data.file)
                    .setTimestamp()
                const row = new MessageActionRow()
                    .addComponents(
                        new MessageButton()
                            .setLabel('View Original Image')
                            .setStyle('LINK')
                            .setURL(response.data.file)
                    );
                await interaction.editReply({ embeds: [embed], components: [row] });
            }
        }
	},
};