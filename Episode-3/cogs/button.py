import nextcord

class ButtonView(nextcord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @nextcord.ui.button(label="Click me!", style=nextcord.ButtonStyle.green)
    async def click_me(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        
        button.disabled = True
        await interaction.response.edit_message(content="Thanks for clicking me! :)", view=self)


class Button(nextcord.ClientCog):
    def __init__(self, client: nextcord.Client):
        self.client = client
    
    @nextcord.slash_command(name="button", description="Button test")
    async def button(self, interaction: nextcord.Interaction):
        await interaction.response.send_message("Click the button!", view=ButtonView())
