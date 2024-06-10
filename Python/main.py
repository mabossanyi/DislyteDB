# Libraries
from browser import Browser
import extractor
import processor
from storage import Storage
from writer import Writer


# Methods
def main():
    # Get the class "Storage"
    storage = Storage()

    # Get the class "Extractor" for the Patch Notes page using the URL
    # to extract the HTML
    patch_notes_url = "https://dislyte.fandom.com/wiki/Patch_Notes"
    patch_notes_extractor = get_page_extractor_from_url(patch_notes_url)
    latest_version = get_latest_version_from_patch_notes(
        patch_notes_extractor, storage)
    print("Running the Dislyte Database (DislyteDB) script using "
          "the version '{}'\n".format(latest_version))

    # Get the class "Extractor" for the List of Espers page using the URL
    # to extract the HTML
    print("Extracting and storing the rarities...")
    list_of_espers_url = "https://dislyte.fandom.com/wiki/Esper/List"
    list_of_espers_extractor = get_page_extractor_from_url(list_of_espers_url)
    extract_and_store_rarities(list_of_espers_extractor, storage)

    # Get the class "Extractor" for the Elemental Classes page using the URL
    # to extract the HTML
    print("Extracting and storing the elements...")
    elemental_classes_url = ("https://dislyte.fandom.com/wiki/Category:"
                             "Elemental_Classes")
    elemental_classes_extractor = get_page_extractor_from_url(
        elemental_classes_url)
    extract_and_store_elements(elemental_classes_extractor, storage)

    # Get the class "Extractor" for the Affiliations page using the URL
    # to extract the HTML
    print("Extracting and storing the affiliations...")
    affiliations_url = "https://dislyte.fandom.com/wiki/Category:Affiliations"
    affiliations_extractor = get_page_extractor_from_url(affiliations_url)
    extract_and_store_affiliations(affiliations_extractor, storage)

    # Get the class "Extractor" for all the Espers data using the URLs
    # to extract the HTML
    list_of_legendary_espers_url = ("https://dislyte.fandom.com/wiki"
                                    "/Esper/Legendary")
    list_of_epic_espers_url = ("https://dislyte.fandom.com/wiki"
                               "/Esper/Epic")
    list_of_rare_espers_url = ("https://dislyte.fandom.com/wiki"
                               "/Esper/Rare")

    urls_list = [[list_of_legendary_espers_url, "Legendary"],
                 [list_of_epic_espers_url, "Epic"],
                 [list_of_rare_espers_url, "Rare"]]

    for url, rarity_name in urls_list:
        list_of_espers_extractor = get_page_extractor_from_url(url)
        extract_and_store_espers_unprocessed_data(
            list_of_espers_extractor, rarity_name, storage)

    storage.reorganize_espers_data()

    # Get the class "Extractor" for all the Bosses data using the URLs
    # to extract the HTML
    krono_boss_url = "https://dislyte.fandom.com/wiki/Kronos"
    apep_boss_url = "https://dislyte.fandom.com/wiki/Apep"
    fafnir_boss_url = "https://dislyte.fandom.com/wiki/Fafnir"
    andras_boss_url = "https://dislyte.fandom.com/wiki/Andras"

    urls_list = [krono_boss_url, apep_boss_url, fafnir_boss_url,
                 andras_boss_url]

    for url in urls_list:
        boss_extractor = get_page_extractor_from_url(url)
        extract_and_store_bosses_unprocessed_data(
            boss_extractor, storage)

    # Get the class "Extractor" for all the Ritual Miracle page with the
    # relics using the URL to extract the HTML
    ritual_miracle_url = "https://dislyte.fandom.com/wiki/Ritual_Miracle"
    ritual_miracle_extractor = get_page_extractor_from_url(ritual_miracle_url)
    extract_and_store_relics_unprocessed_data(
        ritual_miracle_extractor, storage)

    # Get the class "Processor" from the Espers raw data
    espers_data_processor = processor.Processor(
        storage.get_stored_espers_data())

    # Preprocess and store the roles from the Espers raw data
    print("Preprocessing and storing the roles...")
    preprocess_and_store_roles(espers_data_processor, storage)

    # Preprocess and store the mythologies from the Espers raw data
    print("Preprocessing and storing the mythologies...")
    preprocess_and_store_mythologies(espers_data_processor, storage)

    # Preprocess and store the Espers from the Espers data in the storage
    print("Preprocessing and storing the espers...")
    preprocess_and_store_espers(espers_data_processor, storage)

    # Get the class "Processor" from the Bosses raw data
    bosses_data_processor = processor.Processor(
        storage.get_stored_bosses_data())

    # Preprocess and store the Bosses from the Bosses data in the storage
    print("Preprocessing and storing the bosses...")
    preprocess_and_store_bosses(bosses_data_processor, storage)

    # Get the class "Processor" from the relics raw data
    relics_data_processor = processor.Processor(
        storage.get_stored_relics_data())

    # Preprocess and store the relics from the relics data in the storage
    print("Preprocessing and storing the relics...")
    preprocess_and_store_relics(relics_data_processor, storage)

    # Preprocess and store the relics for each Esper from the Espers data and
    # the relics data in the storage
    print("Preprocessing and storing the espers-relics...")
    preprocess_and_store_esper_relics(espers_data_processor, storage)

    # Write the "INSERT.sql" file
    file_name = "INSERT.sql"
    print("Writting the 'INSERT.sql' file...")
    write_insert_sql_file(file_name, latest_version, storage)


def get_page_extractor_from_url(url_str):
    page_browser = Browser(url_str)
    raw_html = page_browser.get_html_from_url()
    page_extractor = extractor.Extractor(raw_html)

    return page_extractor


def get_latest_version_from_patch_notes(extractor_obj, storage_obj):
    patch_notes_list = extractor_obj.extract_patch_notes()
    storage_obj.store_patch_notes(patch_notes_list)
    latest_patch_notes = patch_notes_list[0]
    latest_version = latest_patch_notes.split('/')[-1]

    return latest_version


def extract_and_store_rarities(extractor_obj, storage_obj):
    rarities_list = extractor_obj.extract_rarities()
    storage_obj.store_rarities(rarities_list)
    print(" Completed.\n\t --> Total of {} rarities\n".format(
        len(rarities_list)))


def extract_and_store_elements(extractor_obj, storage_obj):
    elements_list = extractor_obj.extract_elements()
    storage_obj.store_elements(elements_list)
    print(" Completed.\n\t --> Total of {} elements\n".format(
        len(elements_list)))


def extract_and_store_affiliations(extractor_obj, storage_obj):
    affiliations_list = extractor_obj.extract_affiliations()
    storage_obj.store_affiliations(affiliations_list)
    print(" Completed.\n\t --> Total of {} affiliations\n".format(
        len(affiliations_list)))


def extract_and_store_espers_unprocessed_data(
        extractor_obj, rarity_name, storage_obj):
    print("Extracting and storing the {} espers unprocessed data...".format(
        rarity_name))
    espers_data = extractor_obj.extract_espers_data(rarity_name)
    storage_obj.store_espers_data(espers_data)
    print(" Completed.\n\t --> Total of {} {} espers unprocessed data\n"
          .format(len(espers_data), rarity_name))


def extract_and_store_bosses_unprocessed_data(extractor_obj, storage_obj):
    print("Extracting and storing the bosses unprocessed data...")
    bosses_data = extractor_obj.extract_bosses_data()
    storage_obj.store_bosses_data(bosses_data)
    print(" Completed.\n\t --> Total of {} bosses unprocessed data\n"
          .format(len(bosses_data)))


def extract_and_store_relics_unprocessed_data(extractor_obj, storage_obj):
    print("Extracting and storing the relics unprocessed data...")
    relics_data = extractor_obj.extract_relics_data()
    storage_obj.store_relics_data(relics_data)
    print(" Completed.\n\t --> Total of {} relics unprocessed data\n"
          .format(len(relics_data)))


def preprocess_and_store_roles(processor_obj, storage_obj):
    roles_list = processor_obj.preprocess_espers_data_for_role()
    storage_obj.store_roles(roles_list)
    print(" Completed.\n\t --> Total of {} roles\n".format(
        len(roles_list)))


def preprocess_and_store_mythologies(processor_obj, storage_obj):
    mythologies_list = processor_obj.preprocess_espers_data_for_mythology()
    storage_obj.store_mythologies(mythologies_list)
    print(" Completed.\n\t --> Total of {} mythologies\n".format(
        len(mythologies_list)))


def preprocess_and_store_espers(processor_obj, storage_obj):
    espers_list = processor_obj.preprocess_espers_data_for_esper()
    storage_obj.store_espers(espers_list)
    print(" Completed.\n\t --> Total of {} espers\n".format(
        len(espers_list)))


def preprocess_and_store_bosses(processor_obj, storage_obj):
    bosses_list = processor_obj.preprocess_bosses_data_for_boss()
    storage_obj.store_bosses(bosses_list)
    print(" Completed.\n\t --> Total of {} bosses\n".format(
        len(bosses_list)))


def preprocess_and_store_relics(processor_obj, storage_obj):
    relics_list = processor_obj.preprocess_relics_data_for_relic()
    storage_obj.store_relics(relics_list)
    print(" Completed.\n\t --> Total of {} relics\n".format(
        len(relics_list)))


def preprocess_and_store_esper_relics(processor_obj, storage_obj):
    esper_relics_list = processor_obj.preprocess_espers_data_for_esper_relic()
    storage_obj.store_esper_relics(esper_relics_list)
    print(" Completed.\n\t --> Total of {} espers-relics\n".format(
        len(esper_relics_list)))


def write_insert_sql_file(file_name, version, storage_obj):
    file_writer = Writer()
    file_writer.write_insert_sql_file(file_name, version, storage_obj)
    print(" Completed.")


if __name__ == '__main__':
    main()
