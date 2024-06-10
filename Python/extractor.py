# Libraries
import re

from browser import Browser


class Extractor:
    # Attributes
    _error_first_hp_cell_flag = "FIRST_HP_CELL_ERROR"
    _error_last_hp_cell_flag = "LAST_HP_CELL_FLAG"
    _no_personal_section_flag = "NO_PERSONAL_SECTION"
    _no_stats_section_flag = "NO_STATS_SECTION"
    _no_set_recommendations_section_flag = "NO_SET_RECOMMENDATIONS_SECTION"
    _raw_html = ""

    # Constructors
    def __init__(self, raw_html):
        self._raw_html = raw_html

    # Methods
    def extract_patch_notes(self):
        pattern = '<a href=".*?" title=".*?">Patch Notes/.*?</a>'
        match_results_list = re.findall(pattern, self._raw_html, re.IGNORECASE)
        patch_notes_list = [re.sub('<a .*?>', '', line)
                            for line in match_results_list]
        patch_notes_list = [re.sub('</a>', '', line)
                            for line in patch_notes_list]

        return patch_notes_list

    def extract_rarities(self):
        legendary_rarity = "Legendary"
        epic_rarity = "Epic"
        rare_rarity = "Rare"
        pattern = '<a href="/wiki/Esper/.*?" title="Esper/.*?">List of .*?</a>'
        match_results_list = re.findall(pattern, self._raw_html, re.IGNORECASE)
        rarities_list = [re.sub('<a .*? of ', '', line)
                         for line in match_results_list]
        rarities_list = [re.sub(' Espers</a>', '', line)
                         for line in rarities_list]

        # Add the missing information based on the rarity for the database
        detailed_rarities_list = list()
        [detailed_rarities_list.append([rarity, 5])
         for rarity in rarities_list if rarity == legendary_rarity]
        [detailed_rarities_list.append([rarity, 4])
         for rarity in rarities_list if rarity == epic_rarity]
        [detailed_rarities_list.append([rarity, 3])
         for rarity in rarities_list if rarity == rare_rarity]

        if len(rarities_list) != len(detailed_rarities_list):
            print(" >> WARNING <<")
            print(" One or more rarities are missing !")
            exit()

        return detailed_rarities_list

    def extract_elements(self):
        flow_element = "Flow"
        inferno_element = "Inferno"
        shimmer_element = "Shimmer"
        wind_element = "Wind"
        pattern = ('<a href="/wiki/.*?" class="category-page__member-link" '
                   'title=".*?">.*?</a>')
        match_results_list = re.findall(pattern, self._raw_html, re.IGNORECASE)
        elements_list = [re.sub('<a href=".*?" .*?">', '', line)
                         for line in match_results_list]
        elements_list = [re.sub('</a>', '', line)
                         for line in elements_list]

        # Add the missing information based on the rarity for the database
        detailed_elements_list = list()
        [detailed_elements_list.append([element, "purple"])
         for element in elements_list if element == flow_element]
        [detailed_elements_list.append([element, "orange"])
         for element in elements_list if element == inferno_element]
        [detailed_elements_list.append([element, "white"])
         for element in elements_list if element == shimmer_element]
        [detailed_elements_list.append([element, "aqua"])
         for element in elements_list if element == wind_element]

        return detailed_elements_list

    def extract_affiliations(self):
        pattern = ('<a href=".*? class="category-page__member-link" '
                   'title=".*?">.*?</a>')
        match_results_list = re.findall(pattern, self._raw_html, re.IGNORECASE)
        affiliations_list = [re.sub('<a href=".*?" .*?">', '', line)
                             for line in match_results_list]
        affiliations_list = [re.sub('</a>', '', line)
                             for line in affiliations_list]

        return affiliations_list

    def extract_espers_data(self, rarity_name):
        raw_html = self._raw_html.replace('\n', '')
        pattern = '<tr><td width="1%">.*?</td></tr>'
        match_results_list = re.findall(pattern, raw_html, re.IGNORECASE)
        all_results = list()

        for match_result in match_results_list:
            temp_esper_data = self._extract_esper_data(match_result,
                                                       rarity_name)
            all_results.append(temp_esper_data)

        return all_results

    def _extract_esper_data(self, esper_data, rarity_name):
        results_dict = dict()

        # Esper's data from the "List of ... Espers"
        results_dict = self._extract_esper_data_from_list_page(
            esper_data, rarity_name, results_dict)

        # Esper's webpage
        pattern = '<a href="/wiki/.*?" title=".*?">'
        match_result = re.search(pattern, esper_data, re.IGNORECASE)
        match_result_grouped = match_result.group()
        esper_href = re.sub('<a href="', '', match_result_grouped)
        esper_href = re.sub('".*">', '', esper_href)
        esper_url = "https://dislyte.fandom.com/{}".format(esper_href)
        esper_page_browser = Browser(esper_url)
        esper_raw_html = (esper_page_browser.get_html_from_url()
                          .replace('\n', ''))
        esper_raw_html = esper_raw_html.replace('\t', '')

        # Esper's webpage section "Personal"
        results_dict = self._extract_esper_data_from_personal_section(
            esper_raw_html, results_dict)

        if results_dict == self._no_personal_section_flag:
            return None

        # Esper's webpage section "Stats"
        results_dict = self._extract_esper_data_from_stats_section(
            esper_raw_html, results_dict)

        if results_dict == self._no_stats_section_flag:
            return None

        # Esper's webpage section "Set Recommendations"
        results_dict = (
            self._extract_esper_data_from_set_recommendations_section(
                esper_raw_html, results_dict))

        if results_dict == self._no_set_recommendations_section_flag:
            return None

        return results_dict

    def _extract_esper_data_from_list_page(self,
                                           esper_data,
                                           esper_rarity,
                                           results_dict):
        pattern = '<a href="/wiki/.*?" .*?</a></td>'
        match_results_list = re.findall(pattern, esper_data, re.IGNORECASE)

        (raw_esper_name, raw_esper_element,
         raw_esper_mythology, raw_esper_affiliation) = match_results_list

        pattern = '<td><span .*?">.*?</span></td>'
        match_results_list = re.findall(pattern, esper_data, re.IGNORECASE)
        raw_esper_role, raw_esper_version = match_results_list

        # Esper's name
        pattern = '<a href="/wiki/.*?".*?">.*?</a></td>'
        match_results_list = re.findall(pattern, raw_esper_name, re.IGNORECASE)
        esper_name = [re.sub('<.*?>', '', line)
                      for line in match_results_list][0]

        # Function definitions
        def __extract_data_with_href_tag(_raw_esper_data):
            _pattern = '<a href="/wiki/.*?".*?">.*?</a></td>'
            _match_results_list = re.findall(_pattern, _raw_esper_data,
                                             re.IGNORECASE)
            _esper_data = [re.sub('</a> <.*?>', '', line)
                           for line in _match_results_list]
            _esper_data = [re.sub('<.*?>', '', line)
                           for line in _esper_data][0]

            return _esper_data

        def __extract_data_with_span_tag(_raw_esper_data):
            _pattern = '<span .*?>.*?</span></td>'
            _match_results_list = re.findall(_pattern, _raw_esper_data,
                                             re.IGNORECASE)
            _esper_data = [re.sub('<.*?>', '', line)
                           for line in _match_results_list][0]

            return _esper_data

        # Esper's element
        esper_element = __extract_data_with_href_tag(raw_esper_element)

        # Esper's mythology
        esper_mythology = __extract_data_with_href_tag(raw_esper_mythology)

        # Esper's affiliation
        esper_affiliation = __extract_data_with_href_tag(raw_esper_affiliation)

        # Esper's role
        esper_role = __extract_data_with_span_tag(raw_esper_role)

        # Esper's appearance version
        esper_version = __extract_data_with_span_tag(raw_esper_version)

        results_dict["name"] = esper_name
        results_dict["rarity"] = esper_rarity
        results_dict["element"] = esper_element
        results_dict["mythology"] = esper_mythology
        results_dict["affiliation"] = esper_affiliation
        results_dict["role"] = esper_role
        results_dict["version"] = esper_version

        return results_dict

    def _extract_esper_data_from_personal_section(self,
                                                  esper_raw_html,
                                                  results_dict):
        pattern = ('<div class="pi-item pi-data pi-item-spacing '
                   'pi-border-color" .*?>.*?</div>')
        match_results_list = re.findall(pattern, esper_raw_html, re.IGNORECASE)

        if len(match_results_list) == 0:
            print(" WARNING: No personal section for {}".format(
                results_dict["name"]))
            return self._no_personal_section_flag

        # Esper's age
        raw_esper_age = [line for line in match_results_list
                         if line.find("Age") != -1][0]
        esper_age = re.sub('<.*?>', '', raw_esper_age)
        esper_age = re.sub('Age', '', esper_age)

        # Esper's birthday
        raw_esper_birthday = [line for line in match_results_list
                              if line.find("Birthday") != -1][0]
        esper_birthday = re.sub('<.*?>', '', raw_esper_birthday)
        esper_birthday = re.sub('Birthday', '', esper_birthday)

        results_dict["age"] = esper_age
        results_dict["birthday"] = esper_birthday

        return results_dict

    def _extract_esper_data_from_stats_section(self,
                                               esper_raw_html,
                                               results_dict):
        pattern = ('<span class="mw-headline" id="Stats">Stats</span></h3>'
                   '<table .*?>.*?</table>')
        match_results_list = re.findall(pattern, esper_raw_html,
                                        re.IGNORECASE)
        if len(match_results_list) > 0:
            match_results_list = match_results_list[0]
        else:
            print(" WARNING: No stats section for {}".format(
                results_dict["name"]))
            return self._no_stats_section_flag

        pattern = '<tr>.*?</tr>'
        match_results_list = re.findall(pattern, match_results_list,
                                        re.IGNORECASE)

        # Function definitions
        def __extract_variable_stat_from_table(name, match_results):
            raw_esper_stat = [line for line in match_results
                              if line.find(name) != -1][0]
            raw_esper_stat = raw_esper_stat.split("</td><td>")[1]
            raw_esper_stat = raw_esper_stat.replace(",", "")
            raw_esper_stat = raw_esper_stat.replace(".", "")

            return raw_esper_stat

        def __extract_constant_stat_from_table(name, match_results):
            raw_esper_stat = [line for line in match_results
                              if line.find(name) != -1][0]
            raw_esper_stat = raw_esper_stat.split("</td>")[0]
            raw_esper_stat = raw_esper_stat.split('<td colspan="2">')[-1]
            raw_esper_stat = raw_esper_stat.replace("%", "")

            return raw_esper_stat

        def __check_exceptions_and_errors(match_results, _results_dict):
            # Check HP
            hp_row = [line for line in match_results
                      if line.find("HP") != -1][0]
            hp_cells = hp_row.split("</td><td>")
            hp_cells = [re.sub('<.*?>', '', cell)
                        for cell in hp_cells]
            (hp_first_cell_value, hp_second_cell_value,
             _, hp_last_cell_value) = hp_cells
            hp_first_cell_value = hp_first_cell_value.split("/")
            hp_last_cell_value = hp_last_cell_value.split("/")

            # Check ATK
            atk_row = [line for line in match_results
                       if line.find("ATK") != -1][0]
            atk_cells = atk_row.split("</td><td>")
            atk_cells = [re.sub('<.*?>', '', cell)
                         for cell in atk_cells]
            atk_second_cell_value = atk_cells[1]

            if atk_second_cell_value == ascii_dash_symbol:
                if len(hp_first_cell_value) == 4:
                    hp_value = hp_first_cell_value[1].replace(",", "")
                    hp_value = hp_value.replace(".", "")
                    hp_value = hp_value.replace(" ", "")
                    _results_dict["HP"] = hp_value

                    atk_value = hp_second_cell_value.replace(",", "")
                    atk_value = atk_value.replace(".", "")
                    _results_dict["ATK"] = atk_value

                    return _results_dict, self._error_first_hp_cell_flag

                elif len(hp_last_cell_value) == 2:
                    atk_value = hp_last_cell_value[0].replace(",", "")
                    atk_value = atk_value.replace(".", "")
                    _results_dict["ATK"] = atk_value

                    return _results_dict, self._error_last_hp_cell_flag

        # Esper's HP
        stat_name = "HP"
        results_dict[stat_name] = __extract_variable_stat_from_table(
            stat_name, match_results_list)

        # Esper's ATK
        ascii_dash_symbol = "&#8211;"
        stat_name = "ATK"
        results_dict[stat_name] = __extract_variable_stat_from_table(
            stat_name, match_results_list)

        # Check for data errors on the stats HP and ATK
        if results_dict[stat_name] == ascii_dash_symbol:
            __check_exceptions_and_errors(match_results_list, results_dict)

        # Esper's DEF
        stat_name = "DEF"
        results_dict[stat_name] = __extract_variable_stat_from_table(
            stat_name, match_results_list)

        # Esper's SPD
        stat_name = "SPD"
        results_dict[stat_name] = __extract_constant_stat_from_table(
            stat_name, match_results_list)

        # Esper's C.RATE
        stat_name = "C RATE"
        results_dict[stat_name] = __extract_constant_stat_from_table(
            stat_name, match_results_list)

        # Esper's C.DMG
        stat_name = "C DMG"
        results_dict[stat_name] = __extract_constant_stat_from_table(
            stat_name, match_results_list)

        # Esper's ACC
        stat_name = "ACC"
        results_dict[stat_name] = __extract_constant_stat_from_table(
            stat_name, match_results_list)

        # Esper's RESIST
        stat_name = "RESIST"
        results_dict[stat_name] = __extract_constant_stat_from_table(
            stat_name, match_results_list)

        return results_dict

    def _extract_esper_data_from_set_recommendations_section(self,
                                                             esper_raw_html,
                                                             results_dict):
        pattern = ('<caption id="Equipment" style=".*?">'
                   '<b>Set Recommendations</b></caption>'
                   '<tbody>.*?</tbody')
        match_results_list = re.findall(pattern, esper_raw_html,
                                        re.IGNORECASE)

        if len(match_results_list) > 0:
            match_results_list = match_results_list[0]
        else:
            print(" WARNING: No set recommendations for {}".format(
                results_dict["name"]))
            return self._no_set_recommendations_section_flag

        pattern = '</span> <b>Popular Choice</b></th></tr><tr>.*?</tr>'
        match_results_list = re.findall(pattern, match_results_list,
                                        re.IGNORECASE)

        # Function definition
        def __extract_esper_sets(match_result_str):
            _pattern = '<a href=".*?">.*?</a><div style=".*?">.*?</div>'
            _match_results_list = re.findall(_pattern, match_result_str,
                                             re.IGNORECASE)
            _esper_raw_sets = [re.sub('</a><.*?>', '|', line)
                               for line in _match_results_list]
            _esper_raw_sets = [re.sub('<.*?>', '', line)
                               for line in _esper_raw_sets]
            _esper_raw_sets = "&".join(_esper_raw_sets)

            return _esper_raw_sets

        for index in range(len(match_results_list)):
            set_number = "Set{}".format(index + 1)
            results_dict[set_number] = __extract_esper_sets(
                match_results_list[index])

        return results_dict

    def extract_bosses_data(self):
        result_dict = dict()
        raw_html = self._raw_html.replace('\n', '')
        pattern = '<h2 class=".*?" data-source="title1">.*?</h2>'
        match_results_list = re.findall(pattern, raw_html, re.IGNORECASE)
        raw_boss_name = match_results_list[0]

        pattern = ('<section class="pi-item pi-group pi-border-color '
                   'pi-collapse pi-collapse-open">.*?</div></div></section>')
        match_results_list = re.findall(pattern, raw_html, re.IGNORECASE)
        raw_boss_gameplay, raw_boss_mythology = match_results_list

        # Boss' name
        boss_name = re.sub('<.*?>', '', raw_boss_name).split(" ")[0]

        # Boss' element
        pattern = ' <a href="/wiki/.*?" .*?>.*?</a>'
        match_results_list = re.findall(pattern, raw_boss_gameplay,
                                        re.IGNORECASE)[0]
        boss_element = re.sub(' <a href="/wiki/.*?" .*?>', '',
                              match_results_list)
        boss_element = re.sub('</a>', '', boss_element)

        # Boss' mythology
        pattern = '<div class="pi-data-value pi-font">.*?</div>'
        match_results_list = re.findall(pattern, raw_boss_mythology,
                                        re.IGNORECASE)[0]
        boss_mythology = re.sub('<div .*?>', '', match_results_list)
        boss_mythology = re.sub('</div>', '', boss_mythology)

        result_dict["name"] = boss_name
        result_dict["element"] = boss_element
        result_dict["mythology"] = boss_mythology

        return result_dict

    def extract_relics_data(self):
        results_list = list()
        raw_html = self._raw_html.replace('\n', '')
        pattern = '<tbody>.*?</tbody>'
        match_results_list = re.findall(pattern, raw_html, re.IGNORECASE)
        four_piece_sets, two_piece_sets = match_results_list[:2]

        # Function definitions
        def __extract_p_piece_sets_for_boss(_p_piece_sets_boss, _label):
            _results_dict = dict()
            _p_piece_sets_boss = _p_piece_sets_boss.replace(
                '</tr_end>', '</tr>')

            # Boss name
            _pattern = '<tr><td rowspan="3">.*?</a></td>'
            _match_results_list = re.findall(_pattern, _p_piece_sets_boss,
                                             re.IGNORECASE)[0]
            _boss_name = re.sub('.*? title=".*?">', '', _match_results_list)
            _boss_name = re.sub('</a></td>', '', _boss_name)

            # All four piece sets
            _pattern = '<td><a .*?>.*?</td></tr>'
            _match_results_list = re.findall(_pattern, _p_piece_sets_boss,
                                             re.IGNORECASE)
            _four_piece_sets = ["|".join(line.split("</td><td>")[1:3])
                                for line in _match_results_list]
            _four_piece_sets = [re.sub('<.*?>', '', line)
                                for line in _four_piece_sets]
            _four_piece_sets = ["|".join((line.split("|")[0].title(),
                                          line.split("|")[1]))
                                for line in _four_piece_sets]

            _results_dict["boss"] = _boss_name
            _results_dict["{}_piece_set_1".format(_label)] = (
                _four_piece_sets)[0]
            _results_dict["{}_piece_set_2".format(_label)] = (
                _four_piece_sets)[1]
            _results_dict["{}_piece_set_3".format(_label)] = (
                _four_piece_sets)[2]

            return _results_dict

        # Four piece sets
        four_piece_set_results_list = list()
        four_piece_sets = four_piece_sets.replace(
            '<td>Unobtainable', '<td rowspan="3">Unobtainable')
        four_piece_sets = four_piece_sets.replace(
            '</tr><tr><td rowspan="3">', '</tr_end><tr><td rowspan="3">')
        pattern = '<tr><td rowspan="3">.*?</td></tr_end>'
        four_piece_sets_bosses = re.findall(pattern, four_piece_sets,
                                            re.IGNORECASE)

        for four_piece_sets_boss in four_piece_sets_bosses:
            four_piece_set_results_list.append(
                __extract_p_piece_sets_for_boss(four_piece_sets_boss, "four"))

        # Two piece sets
        two_piece_set_results_list = list()
        two_piece_sets = two_piece_sets.replace(
            '</tr></tbody>', '</tr><tr><td rowspan="3"></tbody>')
        two_piece_sets = two_piece_sets.replace(
            '</tr><tr><td rowspan="3">', '</tr_end><tr><td rowspan="3">')
        pattern = '<tr><td rowspan="3">.*?</td></tr_end>'
        two_piece_sets_bosses = re.findall(pattern, two_piece_sets,
                                           re.IGNORECASE)

        for two_piece_sets_boss in two_piece_sets_bosses:
            two_piece_set_results_list.append(
                __extract_p_piece_sets_for_boss(two_piece_sets_boss, "two"))

        # Merge the two dictionaries (4-piece sets + 2-piece sets)
        for four_piece_sets_boss in four_piece_set_results_list:
            boss_name = four_piece_sets_boss["boss"]

            for two_piece_sets_boss in two_piece_set_results_list:
                temp_dict = dict()

                if boss_name == two_piece_sets_boss["boss"]:
                    temp_dict.update(four_piece_sets_boss)
                    temp_dict.update(two_piece_sets_boss)
                    results_list.append(temp_dict)

        return results_list
