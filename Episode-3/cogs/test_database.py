from re import L
import nextcord, aiosqlite

class database_commands(nextcord.ClientCog):
    def __init__(self, client):
        self.client = client
        
    @nextcord.slash_command(name="add_value", description="Add a value to the database")
    async def add_value(self, interaction: nextcord.Interaction, value: str):
        async with self.client.db.cursor() as cursor:
            cursor: aiosqlite.Cursor
            await cursor.execute("INSERT INTO test VALUES (?)", (value,)) #! The , has to be there after value
            await self.client.db.commit()
        await interaction.response.send_message(f"Added `{value}` to the database!", ephemeral=True)

    @nextcord.slash_command(name="get_values", description="Get all values from the database")
    async def get_values(self, interaction: nextcord.Interaction):
        async with self.client.db.cursor() as cursor:
            cursor: aiosqlite.Cursor
            await cursor.execute("SELECT value FROM test")
            values = await cursor.fetchall()
            embed = nextcord.Embed(title="Values")
            num = 0
            for value in values:
                num += 1
                embed.add_field(name=f"Value {num}", value=value[0])
            await interaction.response.send_message(embed=embed)

    @nextcord.slash_command(name="delete_value", description="Delete a value from the database")
    async def delete_value(self, interaction: nextcord.Interaction, value: str):
        async with self.client.db.cursor() as cursor:
            cursor: aiosqlite.Cursor
            await cursor.execute("SELECT value FROM test")
            values = await cursor.fetchall()
            
            for v in values:
                if v[0] == value:
                    await cursor.execute("DELETE FROM test WHERE value = ?", (value,))
                    await self.client.db.commit()
                    await interaction.response.send_message(f"Deleted `{value}` from the database!", ephemeral=True)
                    return 

            await interaction.response.send_message(f"Could not find `{value}` in the database!", ephemeral=True)
