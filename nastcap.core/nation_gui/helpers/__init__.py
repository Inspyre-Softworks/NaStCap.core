from box import Box


from inspyre_toolbox.humanize import Numerical

import nationstates

from nation_gui.logger import ISL

import requests
import shutil


class Region(object) :
    
    
    def __init__(self, name) :
        """
        
        A class that performs a lookup for a target region using the
        NationStates API. Once instantiated the resulting object will
        contain all the information regarding the target region.

        Args:
            name:
                The name of the region you'd like to lookup.
        """
        region = nationstates.Nationstates('NatPy').region(name)
        self.shards = region.get_shards(full_response=True)
    
    
    def __dict__(self) :
        return Box(self.shards)


class Nation(object) :
    
    class FlagImage(object):
        pass

    @property
    def GDP_numerical(self):
        if self.__gdp_numerical is None:
            raw_gdp = int(self.raw_GDP)
            self.__gdp_numerical = Numerical(raw_gdp, self.currency)

        return self.__gdp_numerical


    @property
    def GDP(self):
        gdp = self.GDP_numerical
        return gdp.count_noun()

    
    def __init__(self, name, password=None) :

        self.__gdp_numerical = None
        
        # Set up our logging
        log = ISL.device.add_child(f'NationGUI.helpers.Nation[{name}]')
        
        log.debug('Logging started')
        log.debug(f'Nation name: {name}')
        
        nation = nationstates.Nationstates('NatPy').nation(name, password=password)
        
        if password is not None :
            log.debug('A password was provided...')
        
        log.debug('Grabbing unprivileged information...')
        
        self.shards = nation.get_shards(
                'notables', 'fullname', 'admirables', 'capital',
                'population', 'category', 'gdp', 'currency', 'demonym',
                'demonym2', 'demonym2plural', 'motto', 'policies', 'animal',
                'animaltrait', 'region', 'sensibilities', 'tax', 'publicsector',
                'richest', 'poorest', 'founded', 'foundedtime', 'freedom',
                'govt', 'govtdesc', 'govtpriority', 'income', 'industrydesc',
                'happenings', 'majorindustry', 'legislation', 'flag', 'firstlogin',
                'lastlogin', 'lastactivity', 'type', 'deaths', 'sectors'
                )
        
        log.debug(f'Received the following data: {self.shards}')
        
        if password is not None and nation.is_auth :
            log.debug('I am auhenticated!')
            self.shards.update(nation.get_shards('issues', 'telegrams'))
        
        self.notables = self.shards['notables']['notable']
        self.full_name = self.shards['fullname']
        self.admirables = self.shards['admirables']['admirable']
        self.capital = self.shards['capital']
        self.population = self.shards['population'] + f' million {self.shards["demonym2plural"]}'
        self.currency = self.shards['currency']
        self.raw_GDP = self.shards['gdp']
        self.category = self.shards['category']
        self.motto = self.shards['motto']
        self.policies = self.shards['policies']
        self.animal = self.shards['animal']
        self.animal_trait = self.shards['animaltrait']
        self.region = Region(self.shards['region'])
        try:
            if self.shards['issues'] is not None:
                if 'issues' in self.shards.keys() :
                    self.issues = self.shards['issues']['issue']
            else:
                self.shards = None
        except KeyError:
            self.issues = None
        
            
        self.nation = nation
