from odoo import models, api, fields, _
import requests
import json
import base64
import random

class pokemon(models.Model):
    _name = "pokemon.pokemon"
    _description = "Master Data Pokemon"
    
    
    name = fields.Char(string="Name")
    image = fields.Image(string="Image")
    move_ids = fields.Many2many("pokemon.move","pokemon_move_rel","pokemon_id","move_id")
    type_ids = fields.Many2many("pokemon.type","pokemon_type_rel","pokemon_id","type_id")
    
    
    def get_master_data_pokemon(self):
        
        # get 100 pokemon data
        pokemon_list_result = requests.get("https://pokeapi.co/api/v2/pokemon?limit=100&offset=0")
        if pokemon_list_result.status_code == 200:
            
            pokemon_list = pokemon_list_result.json()                                                
            for pokemon in pokemon_list["results"]:                                                
                
                res = requests.get(pokemon["url"])
                result = res.json()
                
                move_ids = []
                type_ids = []
                
                for move in result["moves"]:
                    move_id = self.env["pokemon.move"].search([("name","=",move["move"]["name"])])
                    
                    if not move_id:
                        move_id = self.env["pokemon.move"].create({"name":move["move"]["name"]})
                    move_ids.append(move_id.id)
                    
                for type in result["types"]:
                    type_id = self.env["pokemon.type"].search([("name","=",type["type"]["name"])])                    
                    if not type_id:
                        type_id = self.env["pokemon.type"].create({"name":type["type"]["name"]})
                    type_ids.append(type_id.id)
                
                # check if pokemon already in master data        
                pokemon_id = self.search([("name","=",pokemon["name"])])                
                if not pokemon_id:
                    pokemon_id = self.create({"name":pokemon["name"]})
                
                # get pokemon image    
                image = requests.get(result["sprites"]["front_default"])
                image_content = base64.b64encode(image.content)
                
                #update pokemon data
                pokemon_id.write({"move_ids":[(6,0,move_ids)], "type_ids":[(6,0,type_ids)], "image":image_content})
                        
                        
    def catch_pokemon(self):        
        prime = False
        num = random.randint(0,9)
        if num > 1:
            for i in range(2, int(num/2)+1):
                if (num % i) == 0:                    
                    break
            else:
                prime = True
        
        if prime :
            pokemon_id = self.env["pokemon.trainer"].create({"pokemon_id":self.id, "trainer":self._uid})            
            wizard = self.env["interact.pokemon"].create({"pokemon_id" : pokemon_id.id, "catch": True, "result":"Congrats, You got new pokemon, You can give a nickname"})
            
            return {
            'name': _('Catch Pokemon'),
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'interact.pokemon',
            'target': 'new',
            'res_id': wizard.id,
            'context': self.env.context,
        }
        else :
            wizard = self.env["interact.pokemon"].create({"catch": False, "result":"Too Bad, its run a way. Try again later"})
            
            return {
            'name': _('Catch Pokemon'),
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'interact.pokemon',
            'target': 'new',
            'res_id': wizard.id,
            'context': self.env.context,
        }
        
class pokemonMove(models.Model):
    _name = "pokemon.move"
    _description = "Pokemon Move"
    
    
    name = fields.Char(string="Name")
    pokemon_id = fields.Many2one("pokemon.pokemon")
    
        
class pokemonType(models.Model):
    _name = "pokemon.type"
    _description = "Pokemon Type"
    
    name = fields.Char(string="Name")
    pokemon_id = fields.Many2one("pokemon.pokemon")


class trainerPokemon(models.Model):
    _name = "pokemon.trainer"
    _description = "Pokemon Trainer"
    _inherits = {"pokemon.pokemon" : "pokemon_id"}
    
    pokemon_id = fields.Many2one("pokemon.pokemon", string="Pokemon", auto_join=True, index=True, ondelete="cascade", required=True)
    trainer = fields.Many2one("res.user", string="Trainer")
    nick_name = fields.Char(string="Nick Name")
    
    
    
    def release_pokemon(self):
        prime = False
        num = random.randint(0,9)
        if num > 1:
            for i in range(2, int(num/2)+1):
                if (num % i) == 0:                    
                    break
            else:
                prime = True
        
        if prime :
            self.unlink()            
            wizard = self.env["interact.pokemon"].create({"release": True, "result":"Success release pokemon"})
            
            return {
            'name': _('Catch Pokemon'),
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'interact.pokemon',
            'target': 'new',
            'res_id': wizard.id,
            'context': self.env.context,
        }
        else :
            wizard = self.env["interact.pokemon"].create({"release": True, "result":"Failed release pokemon"})
            
            return {
            'name': _('Catch Pokemon'),
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'interact.pokemon',
            'target': 'new',
            'res_id': wizard.id,
            'context': self.env.context,
        }
    