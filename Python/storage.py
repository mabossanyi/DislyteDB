class Storage:
    # Attributes
    _patch_notes = None
    _rarities = None
    _elements = None
    _affiliations = None
    _espers_data = None
    _bosses_data = None
    _relics_data = None
    _roles = None
    _mythologies = None
    _espers = None
    _bosses = None
    _relics = None
    _esper_relics = None

    # Constructors
    def __init__(self):
        self._patch_notes = list()
        self._rarities = list()
        self._elements = list()
        self._affiliations = list()
        self._espers_data = list()
        self._bosses_data = list()
        self._relics_data = list()
        self._roles = list()
        self._mythologies = list()
        self._espers = list()
        self._bosses = list()
        self._relics = list()
        self._esper_relics = list()

    # Getters
    def get_stored_patch_notes(self):
        return self._patch_notes

    def get_stored_rarities(self):
        return self._rarities

    def get_stored_elements(self):
        return self._elements

    def get_stored_affiliations(self):
        return self._affiliations

    def get_stored_espers_data(self):
        return self._espers_data

    def get_stored_bosses_data(self):
        return self._bosses_data

    def get_stored_relics_data(self):
        return self._relics_data

    def get_stored_roles(self):
        return self._roles

    def get_stored_mythologies(self):
        return self._mythologies

    def get_stored_espers(self):
        return self._espers

    def get_stored_bosses(self):
        return self._bosses

    def get_stored_relics(self):
        return self._relics

    def get_stored_esper_relics(self):
        return self._esper_relics

    # Methods
    def store_patch_notes(self, patch_notes):
        self._patch_notes = patch_notes

    def store_rarities(self, rarities):
        id_rarity = 1

        for rarity_name, number_stars in rarities:
            self._rarities.append([id_rarity, rarity_name, number_stars])
            id_rarity += 1

    def store_elements(self, elements):
        id_element = 1

        for element_name, color in elements:
            self._elements.append([id_element, element_name, color])
            id_element += 1

    def store_affiliations(self, affiliations):
        id_affiliation = 1

        for affiliation in affiliations:
            self._affiliations.append([id_affiliation, affiliation])
            id_affiliation += 1

    def store_espers_data(self, espers_data):
        self._espers_data.append(espers_data)

    def reorganize_espers_data(self):
        if len(self._espers_data) > 0:
            temp_espers_data = list()

            for data_list in self._espers_data:
                temp_espers_data += data_list

            self._espers_data = temp_espers_data
            self._espers_data = [esper_data
                                 for esper_data in self._espers_data
                                 if esper_data is not None]

    def store_bosses_data(self, bosses_data):
        self._bosses_data.append(bosses_data)

    def store_relics_data(self, relics_data):
        self._relics_data = relics_data

    def store_roles(self, roles):
        id_role = 1

        for role in roles:
            self._roles.append([id_role, role])
            id_role += 1

    def store_mythologies(self, mythologies):
        id_mythology = 1

        for mythology in mythologies:
            self._mythologies.append([id_mythology, mythology])
            id_mythology += 1

        # Add "Ars Goetia" for the Boss "Andras"
        self._mythologies.append([id_mythology, "Ars Goetia"])
        id_mythology += 1

    def store_espers(self, espers):
        id_esper = 1

        for esper in espers:
            (name, rarity, element, role, mythology, affiliation, version,
             age, birthday, maxHp, maxAtk, maxDef, spd, cRate, cDmg, acc,
             resist) = esper
            id_rarity = str([rarity_r[0]
                             for rarity_r in self.get_stored_rarities()
                             if rarity == rarity_r[1]][0])
            id_element = str([element_e[0]
                              for element_e in self.get_stored_elements()
                              if element == element_e[1]][0])
            id_role = str([role_r[0]
                           for role_r in self.get_stored_roles()
                           if role == role_r[1]][0])
            id_mythology = str(
                [mythology_m[0]
                 for mythology_m in self.get_stored_mythologies()
                 if mythology == mythology_m[1]][0]
            )
            id_affiliation = str([
                affiliation_a[0]
                for affiliation_a in self.get_stored_affiliations()
                if affiliation == affiliation_a[1]][0])
            self._espers.append([id_esper, name, id_rarity, id_element,
                                 id_role, id_mythology, id_affiliation,
                                 version, age, birthday, maxHp, maxAtk, maxDef,
                                 spd, cRate, cDmg, acc, resist])
            id_esper += 1

    def store_bosses(self, bosses):
        id_boss = 1

        for boss in bosses:
            name, element, mythology = boss
            id_element = str([element_e[0]
                              for element_e in self.get_stored_elements()
                              if element == element_e[1]][0])
            id_mythology = str(
                [mythology_m[0]
                 for mythology_m in self.get_stored_mythologies()
                 if mythology == mythology_m[1]][0]
            )
            self._bosses.append([id_boss, name, id_element, id_mythology])
            id_boss += 1

    def store_relics(self, relics):
        id_relic = 1

        for relic in relics:
            boss_name, relic_name, relic_description = relic
            id_boss = str([boss_b[0]
                           for boss_b in self.get_stored_bosses()
                           if boss_name == boss_b[1]][0])
            self._relics.append([id_relic, relic_name, relic_description,
                                 id_boss])
            id_relic += 1

    def store_esper_relics(self, esper_relics):
        id_esper_relic = 1

        for esper_relic in esper_relics:
            esper_name, four_pieces_set_name, two_pieces_set_name = esper_relic
            id_esper = str([esper_e[0]
                            for esper_e in self.get_stored_espers()
                            if esper_name == esper_e[1]][0])
            id_four_pieces_relic = str([
                relic_r[0] for relic_r in self.get_stored_relics()
                if four_pieces_set_name == relic_r[1]][0])
            id_two_pieces_relic = str([
                relic_r[0] for relic_r in self.get_stored_relics()
                if two_pieces_set_name == relic_r[1]][0])
            self._esper_relics.append([id_esper_relic,
                                       id_esper,
                                       id_four_pieces_relic,
                                       id_two_pieces_relic])
            id_esper_relic += 1
