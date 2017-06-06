from .database import *


def command(bot, session, author, message):
    tokens  = message.tokens()
    command = tokens[0].split('@')

    try:
        if command[1] != bot.metadata.username:
            return None
    except:
        pass

    if command[0] == '/slap':
        return slap(session, author, tokens)

    elif command[0] == '/mind':
        return mind(bot)

    return None


def slap(session, author, tokens):
    if author.user_name != '':
        actor = '@' + author.user_name
    else:
        actor = author.first_name

    try:
        target = tokens[1]
    except:
        target = '#schizo'

    obj = ' '.join(tokens[2:])

    if obj != '':
        new_slap           = Slap()
        new_slap.author_id = author.id
        new_slap.object    = obj
        session.merge(new_slap)

    else:
        obj = Slap.fetch_random(session).object

    message         = Message()
    message.type    = Message.TYPE_TEXT
    message.content = '*{} slaps {} around a bit with {}'.format(actor, target, obj)
    return message


def mind(bot):
    mind = []
    for word, ttl in bot.mind.data.items():
        mind.append((ttl, word))
    mind.sort(key=lambda item: item[0], reverse=True)

    if len(mind) == 0:
        content = 'Calma aí, acabei de acordar!'

    else:
        content = 'TTL\tWORD\n'
        for (ttl, word) in mind:
            content += '{:02d}\t{}\n'.format(ttl, word)

    message         = Message()
    message.type    = Message.TYPE_TEXT
    message.content = content
    return message


