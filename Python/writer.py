from datetime import datetime
import os.path


class Writer:
    # Attributes
    _is_insert_file_written = None

    # Constructors
    def __init__(self):
        self._is_insert_file_written = False

    # Getters
    def get_is_insert_file_written(self):
        return self._is_insert_file_written

    # Methods
    def write_insert_sql_file(self, file_name, version, storage_obj):
        sql_folder_path = "./SQL/"
        file_path = os.path.join(sql_folder_path, file_name)
        file = open(file_path, "w")

        # Function definitions
        def _write_file_header(_file, _version):
            _file.write("/*\n")
            _file.write("\tAuthor: Marc-Andre Bossanyi\n")
            _file.write("\tEmail: ma.bossanyi@gmail.com\n")
            _file.write("\tCreation Date: 2024/06/09\n")
            _file.write("\tLast Updated: {}\n".
                        format(datetime.today().strftime('%Y/%m/%d')))
            _file.write("\tDislyte - {}\n".format(version))
            _file.write("*/\n\n")

        def _write_rarities_to_insert_sql_file(_file, _storage):
            _file.write('-- Script INSERT for the table "Rarity"\n')
            _stored_rarities = _storage.get_stored_rarities()

            for _stored_rarity in _stored_rarities:
                _id_rarity, _rarity_name, _number_stars = _stored_rarity
                _file.write("INSERT INTO Rarity (idRarity, name, numberStars, "
                            "isDeleted) VALUES ({}, '{}', {}, false);\n"
                            .format(_id_rarity, _rarity_name, _number_stars))

            _file.write("\n")

        def _write_elements_to_insert_sql_file(_file, _storage):
            _file.write('-- Script INSERT for the table "Element"\n')
            _stored_elements = _storage.get_stored_elements()

            for _stored_element in _stored_elements:
                _id_element, _name, _color = _stored_element
                _file.write("INSERT INTO Element (idElement, name, color, "
                            "isDeleted) VALUES ({}, '{}', '{}', false);\n"
                            .format(_id_element, _name, _color))

            _file.write("\n")

        def _write_affiliations_to_insert_sql_file(_file, _storage):
            _file.write('-- Script INSERT for the table "Affiliation"\n')
            _stored_affiliations = _storage.get_stored_affiliations()

            for _stored_affiliation in _stored_affiliations:
                _id_affiliation, _name = _stored_affiliation
                _file.write("INSERT INTO Affiliation (idAffiliation, name, "
                            "isDeleted) VALUES ({}, '{}', false);\n"
                            .format(_id_affiliation, _name))

            _file.write("\n")

        def _write_roles_to_insert_sql_file(_file, _storage):
            _file.write('-- Script INSERT for the table "Role"\n')
            _stored_roles = _storage.get_stored_roles()

            for _stored_role in _stored_roles:
                _id_role, _name = _stored_role
                _file.write("INSERT INTO Role (idRole, name, isDeleted) "
                            "VALUES ({}, '{}', false);\n"
                            .format(_id_role, _name))

            _file.write("\n")

        def _write_mythologies_to_insert_sql_file(_file, _storage):
            _file.write('-- Script INSERT for the table "Mythology"\n')
            _stored_mythologies = _storage.get_stored_mythologies()

            for _stored_mythology in _stored_mythologies:
                _id_mythology, _name = _stored_mythology
                _file.write("INSERT INTO Mythology (idMythology, name, "
                            "isDeleted) VALUES ({}, '{}', false);\n"
                            .format(_id_mythology, _name))

            _file.write("\n")

        def _write_espers_to_insert_sql_file(_file, _storage):
            _file.write('-- Script INSERT for the table "Esper"\n')
            _stored_espers = _storage.get_stored_espers()

            for _stored_esper in _stored_espers:
                (_id_esper, _name, _id_rarity, _id_element, _id_role,
                 _id_mythology, _id_affiliation, _version, _age, _birthday,
                 _max_hp, _max_atk, _max_def, _spd, _c_rate, _c_dmg, _acc,
                 _resist) = _stored_esper
                _file.write("INSERT INTO Esper (idEsper, name, idRarity, "
                            "idElement, idRole, idMythology, idAffiliation, "
                            "version, age, birthday, isOwned, isDeleted, "
                            "maxHp, maxAtk, maxDef, spd, cRate, cDmg, acc, "
                            "resist) VALUES ({}, '{}', {}, {}, {}, {}, {}, "
                            "'{}', {}, '{}', false, false, {}, {}, {}, {}, "
                            "{}, {}, {}, {});\n"
                            .format(_id_esper, _name, _id_rarity,
                                    _id_element, _id_role, _id_mythology,
                                    _id_affiliation, _version, _age, _birthday,
                                    _max_hp, _max_atk, _max_def, _spd, _c_rate,
                                    _c_dmg, _acc, _resist))

            _file.write("\n")

        def _write_bosses_to_insert_sql_file(_file, _storage):
            _file.write('-- Script INSERT for the table "Boss"\n')
            _stored_bosses = _storage.get_stored_bosses()

            for _stored_boss in _stored_bosses:
                _id_boss, _name, _id_element, _id_mythology = _stored_boss
                _file.write("INSERT INTO Boss (idBoss, name, idElement, "
                            "idMythology, isDeleted) VALUES ({}, '{}', {}, "
                            "{}, false);\n"
                            .format(_id_boss, _name, _id_element,
                                    _id_mythology))

            _file.write("\n")

        def _write_relics_to_insert_sql_file(_file, _storage):
            _file.write('-- Script INSERT for the table "Relic"\n')
            _stored_relics = _storage.get_stored_relics()

            for _stored_relic in _stored_relics:
                _id_relic, _name, _description, _id_boss = _stored_relic
                _file.write("INSERT INTO Relic (idRelic, name, description, "
                            "idBoss, isDeleted) VALUES ({}, '{}', '{}', {}, "
                            "false);\n"
                            .format(_id_relic, _name, _description,
                                    _id_boss))

            _file.write("\n")

        def _write_esper_relics_to_insert_sql_file(_file, _storage):
            _file.write('-- Script INSERT for the table "EsperRelic"\n')
            _stored_esper_relics = _storage.get_stored_esper_relics()

            for _stored_esper_relic in _stored_esper_relics:
                (_id_esper_relic, _id_esper, _id_four_pieces_relic,
                 _id_two_pieces_relic) = _stored_esper_relic
                _file.write("INSERT INTO EsperRelic (idEsperRelic, idEsper, "
                            "idFourPiecesRelic, idTwoPiecesRelic) VALUES "
                            "({}, {}, {}, {});\n"
                            .format(_id_esper_relic,
                                    _id_esper,
                                    _id_four_pieces_relic,
                                    _id_two_pieces_relic))

            _file.write("\n")

        def _locate_insert_file(_file_path):
            if os.path.isfile(_file_path):
                _file = open(_file_path, "r")
                _file_lines = _file.readlines()
                _file.close()

                if len(_file_lines) == 0:
                    self._is_insert_file_written = True
                    print("\t --> Error: The 'INSERT.sql' file is empty")
                else:
                    self._is_insert_file_written = True
                    print("\t --> Success: The 'INSERT.sql' file has been "
                          "written in the following path: {}"
                          .format(_file_path))
            else:
                self._is_insert_file_written = False
                print("\t --> Error: The 'INSERT.sql' file doesn't exist")

        _write_file_header(file, version)
        _write_rarities_to_insert_sql_file(file, storage_obj)
        _write_elements_to_insert_sql_file(file, storage_obj)
        _write_affiliations_to_insert_sql_file(file, storage_obj)
        _write_roles_to_insert_sql_file(file, storage_obj)
        _write_mythologies_to_insert_sql_file(file, storage_obj)
        _write_espers_to_insert_sql_file(file, storage_obj)
        _write_bosses_to_insert_sql_file(file, storage_obj)
        _write_relics_to_insert_sql_file(file, storage_obj)
        _write_esper_relics_to_insert_sql_file(file, storage_obj)
        file.close()
        _locate_insert_file(file_path)
