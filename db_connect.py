import asyncpg


class Request:
    def __init__(self, connector: asyncpg.pool.Pool):
        self.connector = connector

    async def add_user(self, user_id, user_name):
        query = '''insert into user_data (user_id, user_name)
                    values ($1, $2) 
                        on conflict (user_id) do update set user_name=$2;'''
        await self.connector.execute(query, user_id, user_name)

    async def add_word(self, user_id, word, translation):
        query = '''insert into word (english, translate)
                        values($1, $2);'''
        await self.connector.execute(query, word, translation)

        extra_query = '''select max(word_id) from word
                            where english = $1 and translate = $2'''
        row = await self.connector.fetch(extra_query, word, translation)
        data = [dict(i) for i in row]

        query = '''insert into users_word (user_id, word_id)
                        values($1, $2);'''
        await self.connector.execute(query, user_id, data[0].get('max'))

    async def delete_word(self, word):
        query = '''delete from word w
                        using users_word uw
                            where w.english = $1 and uw.word_id = w.word_id;'''
        await self.connector.execute(query, word)

    async def lets_start(self, user_id):
        query = '''select english from user_data ud
                    left join users_word uw on ud.user_id = uw.user_id
                        left join word w on uw.word_id = w.word_id
                            where ud.user_id = $1'''
        rows = await self.connector.fetch(query, user_id)
        data = [dict(i) for i in rows]
        print(data)
        return data

    async def get_description(self, user_id):
        query = '''select translate from user_data ud
                            left join users_word uw on ud.user_id = uw.user_id
                                left join word w on uw.word_id = w.word_id
                                    where ud.user_id = $1'''
        rows = await self.connector.fetch(query, user_id)
        data = [dict(i) for i in rows]
        print(data)
        return data

    async def get_translate(self, word):
        query = '''select translate from word where english = $1'''
        row = await self.connector.fetch(query, word)
        data = [dict(i) for i in row]
        return data

    async def check_add_word(self, word, user_id):
        query = '''select english from word w
                    left join users_word uw on uw.word_id = w.word_id
                        left join user_data ud on ud.user_id = uw.user_id
                            where ud.user_id = $1 and w.english = $2'''
        row = await self.connector.fetch(query, user_id, word)
        data = [dict(i) for i in row]
        return data
