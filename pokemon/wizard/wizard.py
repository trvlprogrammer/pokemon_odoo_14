from odoo import models, api, fields, _

class catchPokeMon(models.TransientModel):
    _name = "interact.pokemon"
    
    result = fields.Text("Result")
    trainer = fields.Many2one("Trainer")
    pokemon_id = fields.Many2one("pokemon.trainer")
    catch = fields.Boolean("Catch",default=False)
    release = fields.Boolean("Release",default=False)
    nick_name = fields.Char("Nick name")
    
    def get_pokemon(self):
        
        self.pokemon_id.nick_name = self.nick_name