const { MessageEmbed } = require('discord.js');
var moment = require('moment');

module.exports = async(client) => {
    client.on('guildMemberAdd', async guildMember => {
        try {
            const createdDate = moment(guildMember.user.createdAt).format('MMMM D, YYYY');
            const embed = new MessageEmbed()
                .setColor('#FFC0DD')
                .setAuthor({ name: guildMember.user.username, iconURL: guildMember.user.displayAvatarURL() })
                .setTitle('Member Joined')
                .addField('Created At:', createdDate, false)
                .setFooter({ text: 'ID: ' + guildMember.user.id })
                .setTimestamp()
                const guild = guildMember.guild;
                guild.systemChannel.send({ embeds: [embed] });
        } catch (error) {
            console.error(error);
        }
    });
};