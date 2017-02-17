__author__ = 'Peter Hofmann'


SHIP = 0
SHOP = 1
SPACE_STATION = 2
ASTEROID = 3
MANAGED_ASTEROID = 4
PLANET = 5


class BlueprintEntity(object):

    """
    @type entity_classification: dict[int, dict[int, str]]
    """

    entity_types = {
        SHIP: "Ship",
        SHOP: "Shop",
        SPACE_STATION: "Space Station",
        ASTEROID: "Asteroid",
        MANAGED_ASTEROID: "Managed Asteroid",
        PLANET: "Planet",
    }

    entity_classification = {
        # Ship
        SHIP: {
            0: "General",
            1: "Mining",
            2: "Support",
            3: "Cargo",
            4: "Attack",
            5: "Defense",
            6: "Carrier",
            7: "Scout",
            8: "Scavenger",
            },
        # Station
        SPACE_STATION: {
            9: "General",
            10: "Shipyard",
            11: "Outpost",
            12: "Defense",
            13: "Mining",
            14: "Factory",
            15: "Trade",
            16: "Warp Gate",
            17: "Shopping",
            },
        ASTEROID: {
            18: "General",  # "NONE_ASTEROID",
            },
        MANAGED_ASTEROID: {
            19: "General",  # "NONE_ASTEROID_MANAGED",
            },
        PLANET: {
            20: "General"  # "NONE_PLANET"
            },
        SHOP: {
            21: "General"  # "NONE_SHOP"
            },
        '?': {
            22: "General"  # "NONE_ICO"
            }
        }

    @staticmethod
    def get_entity_classification_default(entity_type):
        """
        Return name of entity classification

        @param entity_type:
        @type entity_type: int

        @rtype: str
        """
        assert entity_type in BlueprintEntity.entity_classification, "Unknown entity type {}".format(entity_type)
        class_list_sorted = sorted(BlueprintEntity.entity_classification[entity_type].keys())
        return class_list_sorted[0]

    @staticmethod
    def get_entity_classification_name(entity_type, entity_classification=None):
        """
        Return name of entity classification

        @param entity_type:
        @type entity_type: int
        @param entity_classification:
        @type entity_classification: int

        @rtype: str
        """
        assert entity_type in BlueprintEntity.entity_classification
        if entity_classification is None:
            entity_classification = BlueprintEntity.get_entity_classification_default(entity_type)
        assert entity_classification in BlueprintEntity.entity_classification[entity_type]
        return BlueprintEntity.entity_classification[entity_type][entity_classification]
