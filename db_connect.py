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
                        values($1, $2)on conflict (english) do update set translate = $2 ;'''
        await self.connector.execute(query, word, translation)

        query = '''insert into users_word (user_id, word_id)
                        values($1, (select word_id from word where english = $2)) on conflict do nothing;'''
        await self.connector.execute(query, user_id, word)

    async def delete_word(self, user_id, word):
        query = '''delete from users_word 
                        where user_id = $1 and word_id=(select word_id from word where english = $2)'''
        await self.connector.execute(query, user_id, word)

    async def lets_start(self, user_id):
        query = '''select english from user_data ud
                    left join users_word uw on ud.user_id = uw.user_id
                        left join word w on uw.word_id = w.word_id
                            where ud.user_id = $1'''
        rows = await self.connector.fetch(query, user_id)
        data = [dict(i) for i in rows]
        return data

    async def get_description(self, user_id):
        query = '''select translate from user_data ud
                            left join users_word uw on ud.user_id = uw.user_id
                                left join word w on uw.word_id = w.word_id
                                    where ud.user_id = $1'''
        rows = await self.connector.fetch(query, user_id)
        data = [dict(i) for i in rows]
        return data

    async def get_translate(self, word):
        query = '''select translate from word where english = $1'''
        row = await self.connector.fetch(query, word)
        data = [dict(i) for i in row]
        return data
