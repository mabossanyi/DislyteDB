class Processor:
    # Attributes
    _data = list()

    # Constructors
    def __init__(self, data):
        self._data = data

    # Methods
    def preprocess_espers_data_for_role(self):
        roles_set = set()

        for esper_data in self._data:
            roles_set.add(esper_data["role"])

        roles_list = sorted(list(roles_set))

        return roles_list

    def preprocess_espers_data_for_mythology(self):
        mythologies_set = set()

        for esper_data in self._data:
            mythologies_set.add(esper_data["mythology"])

        mythologies_list = sorted(list(mythologies_set))

        return mythologies_list

    def preprocess_espers_data_for_esper(self):
        espers_list = list()

        for esper_data in self._data:
            esper_name = (esper_data["name"]
                          .replace("'", "''")
                          .replace("&amp;", "&"))
            esper_birthday = (esper_data["birthday"]
                              .replace("，", ",")
                              .replace("th,", "")
                              .replace("st,", "")
                              .replace("nd,", "")
                              .replace("rd,", ""))

            if len(esper_birthday) == 4:
                esper_birthday = "January 1, 1990"

            espers_list.append([
                esper_name,
                esper_data["rarity"],
                esper_data["element"],
                esper_data["role"],
                esper_data["mythology"],
                esper_data["affiliation"],
                esper_data["version"],
                esper_data["age"],
                esper_birthday,
                esper_data["HP"],
                esper_data["ATK"],
                esper_data["DEF"],
                esper_data["SPD"],
                esper_data["C RATE"],
                esper_data["C DMG"],
                esper_data["ACC"],
                esper_data["RESIST"],
            ])

        espers_list = sorted(espers_list)

        return espers_list

    def preprocess_bosses_data_for_boss(self):
        bosses_list = list()

        for boss_data in self._data:
            bosses_list.append([
                boss_data["name"],
                boss_data["element"],
                boss_data["mythology"]
            ])

        return bosses_list

    def preprocess_relics_data_for_relic(self):
        four_label = "four"
        two_label = "two"

        # Function definition
        def _process_relics_per_number_pieces(_data, _label):
            _relics_list = list()

            for _relic_data in _data:
                _boss_name = _relic_data["boss"]

                for _dict_key in _relic_data:
                    if _dict_key.find(_label) != -1:
                        _dict_value = _relic_data[_dict_key]
                        _set_name, _set_description = _dict_value.split("|")
                        _set_description = _set_description.replace("'", "''")
                        _relics_list.append([
                            _boss_name, _set_name, _set_description])

            return _relics_list

        # Four piece sets
        four_piece_relics_list = _process_relics_per_number_pieces(
            self._data, four_label)

        # Two piece sets
        two_piece_relics_list = _process_relics_per_number_pieces(
            self._data, two_label)

        relics_list = four_piece_relics_list + two_piece_relics_list

        return relics_list

    def preprocess_espers_data_for_esper_relic(self):
        esper_relics_list = list()

        # Function definition
        def _process_esper_relic(_esper_data, _label):
            _esper_name = (_esper_data["name"]
                           .replace("'", "''")
                           .replace("&amp;", "&"))
            _esper_set = _esper_data[_label]
            _esper_set_four_piece, _esper_set_two_piece = _esper_set.split("&")
            _esper_set_four_piece_name = (_esper_set_four_piece.split("|")[0]
                                          .split(" ")[0])
            _esper_set_two_piece_name = (_esper_set_two_piece.split("|")[0]
                                         .split(" ")[0])
            _result_list = [_esper_name,
                            _esper_set_four_piece_name,
                            _esper_set_two_piece_name]

            return _result_list

        for esper_data in self._data:
            first_set_list = _process_esper_relic(esper_data, "Set1")
            second_set_list = _process_esper_relic(esper_data, "Set2")
            third_set_list = _process_esper_relic(esper_data, "Set3")
            esper_relics_list.append(first_set_list)
            esper_relics_list.append(second_set_list)
            esper_relics_list.append(third_set_list)

        return esper_relics_list
