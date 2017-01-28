from lib.utils.blueprintentity import BlueprintEntity, SHIP

__author__ = 'Peter Hofmann'


class BlockConfigHardcoded(object):
    """
    Hardcoded block config
    """

    _block_ids = dict()

    _block_ids["hull"] = {
        # Basic Hull
        598: "Grey Hull", 599: "Grey Hull Wedge", 600: "Grey Hull Corner", 602: "Grey Hull Tetra", 601: "Grey Hull Hepta",
        603: "Black Hull", 604: "Black Hull Wedge", 605: "Black Hull Corner", 607: "Black Hull Tetra", 606: "Black Hull Hepta",
        608: "White Hull", 609: "White Hull Wedge", 610: "White Hull Corner", 612: "White Hull Tetra", 611: "White Hull Hepta",
        613: "Purple Hull", 614: "Purple Hull Wedge", 615: "Purple Hull Corner", 617: "Purple Hull Tetra", 616: "Purple Hull Hepta",
        618: "Blue Hull", 619: "Blue Hull Wedge", 620: "Blue Hull Corner", 622: "Blue Hull Tetra", 621: "Blue Hull Hepta",
        623: "Green Hull", 624: "Green Hull Wedge", 625: "Green Hull Corner", 627: "Green Hull Tetra", 626: "Green Hull Hepta",
        628: "Yellow Hull", 629: "Yellow Hull Wedge", 630: "Yellow Hull Corner", 632: "Yellow Hull Tetra", 631: "Yellow Hull Hepta",
        633: "Orange Hull", 634: "Orange Hull Wedge", 635: "Orange Hull Corner", 637: "Orange Hull Tetra", 636: "Orange Hull Hepta",
        638: "Red Hull", 639: "Red Hull Wedge", 640: "Red Hull Corner", 642: "Red Hull Tetra", 641: "Red Hull Hepta",
        643: "Brown Hull", 644: "Brown Hull Wedge", 645: "Brown Hull Corner", 647: "Brown Hull Tetra", 646: "Brown Hull Hepta",
        828: "Dark Grey Hull", 829: "Dark Grey Hull Wedge", 830: "Dark Grey Hull Corner", 832: "Dark Grey Hull Tetra", 831: "Dark Grey Hull Hepta",
        878: "Teal Hull", 879: "Teal Hull Wedge", 880: "Teal Hull Corner", 882: "Teal Hull Tetra", 881: "Teal Hull Hepta",
        912: "Pink Hull", 913: "Pink Hull Wedge", 914: "Pink Hull Corner", 916: "Pink Hull Tetra", 915: "Pink Hull Hepta",
        63: "Glass", 329: "Glass Wedge", 330: "Glass Corner", 368: "Glass Tetra", 367: "Glass Hepta",

        # Standard Armor
        5: "Grey Standard Armor", 293: "Grey Standard Armor Wedge", 302: "Grey Standard Armor Corner", 348: "Grey Standard Armor Tetra", 357: "Grey Standard Armor Hepta",
        69: "Purple Standard Armor", 294: "Purple Standard Armor Wedge", 303: "Purple Standard Armor Corner", 395: "Purple Standard Armor Tetra", 387: "Purple Standard Armor Hepta",
        70: "Brown Standard Armor", 295: "Brown Standard Armor Wedge", 304: "Brown Standard Armor Corner", 404: "Brown Standard Armor Tetra", 403: "Brown Standard Armor Hepta",
        75: "Black Standard Armor", 296: "Black Standard Armor Wedge", 305: "Black Standard Armor Corner", 393: "Black Standard Armor Tetra", 385: "Black Standard Armor Hepta",
        76: "Red Standard Armor", 297: "Red Standard Armor Wedge", 306: "Red Standard Armor Corner", 394: "Red Standard Armor Tetra", 386: "Red Standard Armor Hepta",
        77: "Blue Standard Armor", 298: "Blue Standard Armor Wedge", 307: "Blue Standard Armor Corner", 396: "Blue Standard Armor Tetra", 388: "Blue Standard Armor Hepta",
        78: "Green Standard Armor", 299: "Green Standard Armor Wedge", 308: "Green Standard Armor Corner", 397: "Green Standard Armor Tetra", 389: "Green Standard Armor Hepta",
        79: "Yellow Standard Armor", 300: "Yellow Standard Armor Wedge", 309: "Yellow Standard Armor Corner", 398: "Yellow Standard Armor Tetra", 391: "Yellow Standard Armor Hepta",
        81: "White Standard Armor", 301: "White Standard Armor Wedge", 310: "White Standard Armor Corner", 400: "White Standard Armor Tetra", 392: "White Standard Armor Hepta",
        426: "Orange Standard Armor", 427: "Orange Standard Armor Wedge", 428: "Orange Standard Armor Corner", 430: "Orange Standard Armor Tetra", 429: "Orange Standard Armor Hepta",
        436: "Yellow Hazard Armor", 437: "Yellow Hazard Armor Wedge", 648: "Yellow Hazard Armor Corner", 650: "Yellow Hazard Armor Tetra", 649: "Yellow Hazard Armor Hepta",
        438: "Green Hazard Armor", 439: "Green Hazard Armor Wedge", 651: "Green Hazard Armor Corner", 653: "Green Hazard Armor Tetra", 652: "Green Hazard Armor Hepta",
        818: "Dark Grey Standard Armor", 819: "Dark Grey Standard Armor Wedge", 820: "Dark Grey Standard Armor Corner", 822: "Dark Grey Standard Armor Tetra", 821: "Dark Grey Standard Armor Hepta",
        868: "Teal Standard Armor", 869: "Teal Standard Armor Wedge", 870: "Teal Standard Armor Corner", 872: "Teal Standard Armor Tetra", 871: "Teal Standard Armor Hepta",
        902: "Pink Standard Armor", 903: "Pink Standard Armor Wedge", 904: "Pink Standard Armor Corner", 906: "Pink Standard Armor Tetra", 905: "Pink Standard Armor Hepta",

        # Advanced Armor
        263: "Grey Advanced Armor", 311: "Grey Advanced Armor Wedge", 320: "Grey Advanced Armor Corner", 402: "Grey Advanced Armor Tetra", 401: "Grey Advanced Armor Hepta",
        264: "Black Advanced Armor", 312: "Black Advanced Armor Wedge", 321: "Black Advanced Armor Corner", 377: "Black Advanced Armor Tetra", 369: "Black Advanced Armor Hepta",
        265: "Red Advanced Armor", 313: "Red Advanced Armor Wedge", 322: "Red Advanced Armor Corner", 378: "Red Advanced Armor Tetra", 370: "Red Advanced Armor Hepta",
        266: "Purple Advanced Armor", 314: "Purple Advanced Armor Wedge", 323: "Purple Advanced Armor Corner", 379: "Purple Advanced Armor Tetra", 371: "Purple Advanced Armor Hepta",
        267: "Blue Advanced Armor", 315: "Blue Advanced Armor Wedge", 324: "Blue Advanced Armor Corner", 380: "Blue Advanced Armor Tetra", 372: "Blue Advanced Armor Hepta",
        268: "Green Advanced Armor", 316: "Green Advanced Armor Wedge", 325: "Green Advanced Armor Corner", 381: "Green Advanced Armor Tetra", 373: "Green Advanced Armor Hepta",
        269: "Brown Advanced Armor", 317: "Brown Advanced Armor Wedge", 326: "Brown Advanced Armor Corner", 382: "Brown Advanced Armor Tetra", 374: "Brown Advanced Armor Hepta",
        270: "Yellow Advanced Armor", 318: "Yellow Advanced Armor Wedge", 327: "Yellow Advanced Armor Corner", 383: "Yellow Advanced Armor Tetra", 375: "Yellow Advanced Armor Hepta",
        271: "White Advanced Armor", 319: "White Advanced Armor Wedge", 328: "White Advanced Armor Corner", 384: "White Advanced Armor Tetra", 376: "White Advanced Armor Hepta",
        431: "Orange Advanced Armor", 432: "Orange Advanced Armor Wedge", 433: "Orange Advanced Armor Corner", 435: "Orange Advanced Armor Tetra", 434: "Orange Advanced Armor Hepta",
        823: "Dark Grey Advanced Armor", 824: "Dark Grey Advanced Armor Wedge", 825: "Dark Grey Advanced Armor Corner", 827: "Dark Grey Advanced Armor Tetra", 826: "Dark Grey Advanced Armor Hepta",
        873: "Teal Advanced Armor", 874: "Teal Advanced Armor Wedge", 875: "Teal Advanced Armor Corner", 877: "Teal Advanced Armor Tetra", 876: "Teal Advanced Armor Hepta",
        907: "Pink Advanced Armor", 908: "Pink Advanced Armor Wedge", 909: "Pink Advanced Armor Corner", 911: "Pink Advanced Armor Tetra", 910: "Pink Advanced Armor Hepta",

        # Crystal Armor
        507: "White Crystal Armor", 508: "White Crystal Armor Wedge", 509: "White Crystal Armor Corner", 511: "White Crystal Armor Tetra", 510: "White Crystal Armor Hepta",
        512: "Red Crystal Armor", 513: "Red Crystal Armor Wedge", 514: "Red Crystal Armor Corner", 516: "Red Crystal Armor Tetra", 515: "Red Crystal Armor Hepta",
        517: "Orange Crystal Armor", 518: "Orange Crystal Armor Wedge", 519: "Orange Crystal Armor Corner", 521: "Orange Crystal Armor Tetra", 520: "Orange Crystal Armor Hepta",
        522: "Yellow Crystal Armor", 523: "Yellow Crystal Armor Wedge", 524: "Yellow Crystal Armor Corner", 526: "Yellow Crystal Armor Tetra", 525: "Yellow Crystal Armor Hepta ",
        527: "Green Crystal Armor", 528: "Green Crystal Armor Wedge", 529: "Green Crystal Armor Corner", 531: "Green Crystal Armor Tetra", 530: "Green Crystal Armor Hepta",
        532: "Blue Crystal Armor", 533: "Blue Crystal Armor Wedge", 534: "Blue Crystal Armor Corner", 536: "Blue Crystal Armor Tetra", 535: "Blue Crystal Armor Hepta",
        537: "Purple Crystal Armor", 538: "Purple Crystal Armor Wedge", 539: "Purple Crystal Armor Corner", 541: "Purple Crystal Armor Tetra", 540: "Purple Crystal Armor Hepta",
        593: "Black Crystal Armor", 594: "Black Crystal Armor Wedge", 595: "Black Crystal Armor Corner", 597: "Black Crystal Armor Tetra", 596: "Black Crystal Armor Hepta",
        690: "Brown Crystal Armor", 691: "Brown Crystal Armor Wedge", 692: "Brown Crystal Armor Corner", 694: "Brown Crystal Armor Tetra", 693: "Brown Crystal Armor Hepta",
        883: "Teal Crystal Armor", 884: "Teal Crystal Armor Wedge", 885: "Teal Crystal Armor Corner", 887: "Teal Crystal Armor Tetra", 886: "Teal Crystal Armor Hepta",
        917: "Pink Crystal Armor", 918: "Pink Crystal Armor Wedge", 919: "Pink Crystal Armor Corner", 921: "Pink Crystal Armor Tetra", 920: "Pink Crystal Armor Hepta",

        # slabs
        698: "Gray Hull 1/4", 699: "Gray Hull 1/2", 700: "Gray Hull 3/4",
        701: "Gray Standard Armor 1/4", 702: "Gray Standard Armor 1/2", 703: "Gray Standard Armor 3/4",
        704: "Gray Advanced Armor 1/4", 705: "Gray Advanced Armor 1/2", 706: "Gray Advanced Armor 3/4",
        707: "White Hull 1/4", 708: "White Hull 1/2", 709: "White Hull 3/4",
        710: "White Standard Armor 1/4", 711: "White Standard Armor 1/2", 712: "White Standard Armor 3/4",
        713: "White Advanced Armor 1/4", 714: "White Advanced Armor 1/2", 715: "White Advanced Armor 3/4",
        716: "White Crystal Armor 1/4", 717: "White Crystal Armor 1/2", 718: "White Crystal Armor 3/4",
        719: "Black Hull 1/4", 720: "Black Hull 1/2", 721: "Black Hull 3/4",
        722: "Black Standard Armor 1/4", 723: "Black Standard Armor 1/2", 724: "Black Standard Armor 3/4",
        725: "Black Advanced Armor 1/4", 726: "Black Advanced Armor 1/2", 727: "Black Advanced Armor 3/4",
        728: "Black Crystal Armor 1/4", 729: "Black Crystal Armor 1/2", 730: "Black Crystal Armor 3/4",
        731: "Yellow Hull 1/4", 732: "Yellow Hull 1/2", 733: "Yellow Hull 3/4",
        734: "Yellow Standard Armor 1/4", 735: "Yellow Standard Armor 1/2", 736: "Yellow Standard Armor 3/4",
        737: "Yellow Advanced Armor 1/4", 738: "Yellow Advanced Armor 1/2", 739: "Yellow Advanced Armor 3/4",
        740: "Yellow Crystal Armor 1/4", 741: "Yellow Crystal Armor 1/2", 742: "Yellow Crystal Armor 3/4",
        743: "Orange Hull 1/4", 744: "Orange Hull 1/2", 745: "Orange Hull 3/4",
        746: "Orange Standard Armor 1/4", 747: "Orange Standard Armor 1/2", 748: "Orange Standard Armor 3/4",
        749: "Orange Advanced Armor 1/4", 750: "Orange Advanced Armor 1/2", 751: "Orange Advanced Armor 3/4",
        752: "Orange Crystal Armor 1/4", 753: "Orange Crystal Armor 1/2", 754: "Orange Crystal Armor 3/4",
        755: "Red Hull 1/4", 756: "Red Hull 1/2", 757: "Red Hull 3/4",
        758: "Red Standard Armor 1/4", 759: "Red Standard Armor 1/2", 760: "Red Standard Armor 3/4",
        761: "Red Advanced Armor 1/4", 762: "Red Advanced Armor 1/2", 763: "Red Advanced Armor 3/4",
        764: "Red Crystal Armor 1/4", 765: "Red Crystal Armor 1/2", 766: "Red Crystal Armor 3/4",
        767: "Purple Hull 1/4", 768: "Purple Hull 1/2", 769: "Purple Hull 3/4",
        770: "Purple Standard Armor 1/4", 771: "Purple Standard Armor 1/2", 772: "Purple Standard Armor 3/4",
        773: "Purple Advanced Armor 1/4", 774: "Purple Advanced Armor 1/2", 775: "Purple Advanced Armor 3/4",
        776: "Purple Crystal Armor 1/4", 777: "Purple Crystal Armor 1/2", 778: "Purple Crystal Armor 3/4",
        779: "Blue Hull 1/4", 780: "Blue Hull 1/2", 781: "Blue Hull 3/4",
        782: "Blue Standard Armor 1/4", 783: "Blue Standard Armor 1/2", 784: "Blue Standard Armor 3/4",
        785: "Blue Advanced Armor 1/4", 786: "Blue Advanced Armor 1/2", 787: "Blue Advanced Armor 3/4",
        788: "Blue Crystal Armor 1/4", 789: "Blue Crystal Armor 1/2", 790: "Blue Crystal Armor 3/4",
        791: "Green Hull 1/4", 792: "Green Hull 1/2", 793: "Green Hull 3/4",
        794: "Green Standard Armor 1/4", 795: "Green Standard Armor 1/2", 796: "Green Standard Armor 3/4",
        797: "Green Advanced Armor 1/4", 798: "Green Advanced Armor 1/2", 799: "Green Advanced Armor 3/4",
        800: "Green Crystal Armor 1/4", 801: "Green Crystal Armor 1/2", 802: "Green Crystal Armor 3/4",
        803: "Green Hull 1/4", 804: "Green Hull 1/2", 805: "Green Hull 3/4",
        806: "Green Standard Armor 1/4", 807: "Green Standard Armor 1/2", 808: "Green Standard Armor 3/4",
        809: "Green Advanced Armor 1/4", 810: "Green Advanced Armor 1/2", 811: "Green Advanced Armor 3/4",
        812: "Green Crystal Armor 1/4", 813: "Green Crystal Armor 1/2", 814: "Green Crystal Armor 3/4",
        815: "Glass 1/4", 816: "Glass 1/2", 817: "Glass 3/4",
        833: "Dark Gray Hull 1/4", 834: "Dark Gray Hull 1/2", 835: "Dark Gray Hull 1/4",
        836: "Dark Gray Standard Armor 1/4", 837: "Dark Gray Standard Armor 1/2", 838: "Dark Gray Standard Armor 3/4",
        839: "Dark Gray Advanced Armor 1/4", 840: "Dark Gray Advanced Armor 1/2", 841: "Dark Gray Advanced Armor 3/4",
        851: "Green Hazard Armor 1/4", 852: "Green Hazard Armor 1/2", 853: "Green Hazard Armor 3/4",
        863: "Yellow Hazard Armor 1/4", 864: "Yellow Hazard Armor 1/2", 865: "Yellow Hazard Armor 3/4",
        890: "Teal Hull 1/4", 891: "Teal Hull 1/2", 892: "Teal Hull 3/4",
        893: "Teal Standard Armor 1/4", 894: "Teal Standard Armor 1/2", 895: "Teal Standard Armor 3/4",
        896: "Teal Advanced Armor 1/4", 897: "Teal Advanced Armor 1/2", 898: "Teal Advanced Armor 3/4",
        899: "Teal Crystal Armor 1/4", 900: "Teal Crystal Armor 1/2", 901: "Teal Crystal Armor 3/4",
        924: "Pink Crystal Armor 1/4", 925: "Pink Crystal Armor 1/2", 926: "Pink Crystal Armor 3/4",
        927: "Pink Standard Armor 1/4", 928: "Pink Standard Armor 1/2", 929: "Pink Standard Armor 3/4",
        930: "Pink Advanced Armor 1/4", 931: "Pink Advanced Armor 1/2", 932: "Pink Advanced Armor 3/4",
        933: "Pink Hull 1/4", 934: "Pink Hull 1/2", 935: "Pink Hull 3/4",
        }

    _block_ids["systems"] = {
        # Systems
        1: "Ship Core",
        2: "Power Reactor Module",
        331: "Power Capacitor",
        978: "Power Auxiliary",
        3: "Shield Capacitor",
        478: "Shield-Recharger",
        8: "Thruster Module",
        544: "Jump Drive Computer",
        545: "Jump Drive Module",
        681: "Jump Inhibitor Computer",
        682: "Jump Inhibitor Module",
        687: "Transporter Controller",
        688: "Transporter Module",
        654: "Scanner Computer",
        655: "Scanner Antenna",
        56: "Gravity Unit",
        120: "Storage",
        689: "Cargo Space",
        123: "Build Block",
        22: "Cloaker",
        15: "RadarJammer",
        47: "Camera",
        121: "BOBBY AI Module",
        671: "Rail Mass Enhancer",
        672: "Rail Speed Controller",
        291: "Faction Module",
        }

    _block_ids["doors"] = {
        # Doors
        122: "Plex Door", 588: "Plex Door Wedge",
        589: "Glass Door", 590: "Glass Door Wedge",
        591: "Blast Door", 592: "Blast Door Wedge",
        842: "Plex Door 1/4", 843: "Plex Door 1/2", 844: "Plex Door 3/4",
        845: "Glass Door 1/4", 846: "Glass Door 1/2", 847: "Glass Door 3/4",
        848: "Blast Door 1/4", 849: "Blast Door 1/2", 850: "Blast Door 3/4",
        659: "Forcefield (Red)", 673: "Forcefield Wedge (Red)",
        660: "Forcefield (Blue)", 674: "Forcefield Wedge (Blue)",
        661: "Forcefield (Yellow)", 675: "Forcefield Wedge (Yellow)",
        854: "Forcefield (Red) 1/4", 855: "Forcefield (Red) 1/2", 856: "Forcefield (Red) 3/4",
        857: "Forcefield (Blue) 1/4", 858: "Forcefield (Blue) 1/2", 859: "Forcefield (Blue) 3/4",
        860: "Forcefield (Yellow) 1/4", 861: "Forcefield (Yellow) 1/2", 862: "Forcefield (Yellow) 3/4",
        }

    _block_ids["docking"] = {
        # Docking
        # #Old Docking
        7: "Turret Docking Unit",
        88: "Turret Docking Enhancer Unit",
        289: "Docking Module",
        290: "Docking Enhancer",
        }

    docking_to_rails = {
        7: 665,  # "Turret Docking Unit" -> "Rail Turret Axis"
        88: None,
        289: 662,  # "Docking Module" -> "Rail Basic"
        290: None
    }

    _block_ids["rails"] = {
        # #Rails
        662: "Rail Basic",
        663: "Rail Docker",
        664: "Rail Rotator Clock Wise",
        665: "Rail Turret Axis",
        669: "Rail Rotator Counter Clock Wise",
        937: "Pickup Point",
        938: "Pickup Rail",
        939: "Shootout Rail",
        }

    _block_ids["effects"] = {
        # Effects
        418: "Piercing Effect Computer", 419: "Piercing Effect Module",
        420: "Explosive Effect Computer", 421: "Explosive Effect Module",
        422: "Punch-Through Effect Computer", 423: "Punch-Through Effect Module",
        424: "EMP Effect Computer", 425: "EMP Effect Module",
        460: "Stop Effect Computer", 461: "Stop Effect Module",
        462: "Push Effect Computer", 463: "Push Effect Module",
        464: "Pull Effect Computer", 465: "Pull Effect Module",
        466: "Ion Effect Computer", 467: "Ion Effect Module",
        476: "Overdrive Effect Computer", 477: "Overdrive Effect Module",
        }

    _block_ids["weapons"] = {
        # Weapons
        14: "Warhead",
        6: "Cannon Computer", 16: "Cannon Barrel",
        38: "Missile Computer", 32: "Missile Tube",
        414: "Damage Beam Computer", 415: "Damage Beam Module",
        416: "Damage Pulse Computer", 417: "Damage Pulse Module",
        }

    _block_ids["tools"] = {
        # Support Tools
        4: "Salvage Computer", 24: "Salvage Module",
        39: "Astrotech Computer", 30: "Astrotech Module",
        46: "Shield Drain Computer", 40: "Shield Drain Module",
        54: "Shield Supply Computer", 48: "Shield Supply Module",
        332: "Power Drain Computer", 333: "Power Drain Module",
        334: "Power Supply Computer", 335: "Power Supply Module",
        344: "Push Pulse Computer", 345: "Push Pulse Module",
        }

    _block_ids["logic"] = {
        # Logic
        405: "Activation Module", 406: "Signal (Delay-Non-Repeating)",
        413: "Trigger (Area) Controller", 407: "DELAY-Signal",
        411: "Trigger (Area)", 408: "AND-Signal",
        412: "Trigger (Step On)", 409: "OR-Signal",
        668: "Wireless Logic Module", 410: "NOT-Signal",
        666: "Button", 667: "Flip Flop",
        670: "Inner Ship Remote", 979: "Randomizer",
        685: "Activation Gate Controller",
        686: "Activation Gate Module",
        980: "Sensor",
        }

    _block_ids["crafting"] = {
        999: "Blueprint Empty",
        # Crafting Materials
        341: "Bronze Bar", 342: "Silver Bar", 343: "Gold Bar",
        144: "Larimar Capsule", 238: "Orange Paint", 440: "Alloyed Metal Mesh",
        152: "Chabaz Capsule", 239: "Red Paint", 220: "Crystal Composite",
        156: "Lukrah Capsule", 240: "Purple Paint", 546: "Scrap Alloy",
        160: "Dolom Capsule", 241: "Brown Paint", 547: "Scrap Composite",
        164: "Sugil Capsule", 242: "Green Paint", 866: "Standard Hardener",
        172: "Cinnabar Capsule", 243: "Yellow Paint", 867: "Advanced Hardener",
        180: "Varis Capsule", 246: "Blue Paint",
        204: "Tekt Capsule", 244: "Black Paint",
        245: "White Paint",
        }

    _block_ids["shards"] = {
        # Shards
        480: "Hattel Shard Raw", 182: "Hattel Capsule",
        481: "Sintyr Shard Raw", 146: "Sintyr Capsule",
        482: "Mattise Shard Raw", 194: "Mattise Capsule",
        483: "Rammet Shard Raw", 174: "Rammet Capsule",
        484: "Varat Shard Raw", 190: "Varat Capsule",
        485: "Bastyn Shard Raw", 186: "Bastyn Capsule",
        486: "Parseen Shard Raw", 166: "Parseen Capsule",
        487: "Nocx Shard Raw", 198: "Nocx Capsule",
        }

    _block_ids["ores"] = {
        # Ores
        488: "Threns Ore Raw", 154: "Threns Capsule",
        489: "Jisper Ore Raw", 150: "Jisper Capsule",
        490: "Zercaner Ore Raw", 170: "Zercaner Capsule",
        491: "Sertise Ore Raw", 162: "Sertise Capsule",
        492: "Hylat Ore Raw", 142: "Hylat Capsule",
        493: "Fertikeen Ore Raw", 178: "Fertikeen Capsule",
        494: "Sapsun Ore Raw", 158: "Sapsun Capsule",
        495: "Macet Ore Raw", 202: "Macet Capsule",
        }

    _block_ids["permissions"] = {
        # permissions
        346: "Public Permission Module",
        936: "Faction Permission Module",
        }

    _block_ids["station"] = {
        # Station only
        94: "Undeathinator",
        113: "Plex Lift",
        211: "Basic Factory",
        217: "Standard Factory",
        259: "Advanced Factory",
        213: "Capsule Refinery",
        215: "Micro Assembler",
        212: "Factory Enhancer",
        347: "Shop Module",
        542: "Warp Gate Computer",
        543: "Warp Gate Module",
        677: "Shipyard Computer",
        678: "Shipyard Module",
        679: "Shipyard Core Anchor",
        683: "Race Gate Controller",
        684: "Race Gate Module",
        }

    _block_ids["decorative"] = {
        # Decorative
        479: "Display Module",
        336: "Decorative Switchboard",
        337: "Decorative Server",
        338: "Decorative Pipes",
        339: "Decorative Panel",
        447: "Decorative Screen (Red)",
        448: "Decorative Screen (Blue)",
        449: "Decorative Computer (Green)",
        450: "Decorative Computer (Orange)",
        451: "Personal Computer (Blue)",
        657: "Decorative Charts",
        658: "Conduit (Blue)",
        680: "Decorative Fan",
        941: "Girder",
        145: "Carved Larimar",
        153: "Carved Chabaz",
        157: "Carved Lukrah",
        161: "Carved Dolom",
        165: "Carved Sugil",
        173: "Carved Cinnabar",
        181: "Carved Varis",
        205: "Carved Tekt",
        656: "Scaffold",
        676: "Scaffold Wedge",
        219: "Crystal Composite Wedge",
        441: "Alloyed Metal Mesh Wedge",
        442: "Metal Grill",
        443: "Metal Grill Wedge",
        444: "Ice Crystal Wedge",
        940: "Ice Wedge",
        975: "Decorative Console (Blue)",
        976: "Pipe",
        1000: "Pipe Tee",
        1001: "Pipe Elbow",
        1006: "Pipe Cross",
        1003: "Grate",
        1004: "Grate Corner",
        1005: "Grate Wedge",
        }

    _block_ids["lighting"] = {
        # Lighting
        977: "White Light Bar",
        1007: "White Light Corner",
        62: "Beacon", 503: "Beacon Rod",
        55: "White Light", 499: "White Rod Light",
        498: "Black Light", 500: "Black Rod Light",
        282: "Red Light", 501: "Red Rod Light",
        283: "Blue Light", 505: "Blue Rod Light",
        284: "Green Light", 504: "Green Rod Light",
        285: "Yellow Light", 340: "Yellow Rod Light",
        496: "Purple Light", 506: "Purple Rod Light",
        497: "Orange Light", 502: "Orange Rod Light",
        888: "Teal Light", 889: "Teal Rod Light",
        922: "Pink Light", 923: "Pink Rod Light",

        # slab
        942: "White Light 1/4", 943: "White Light 1/2", 944: "White Light 3/4",
        945: "Beacon 1/4", 946: "Beacon 1/2", 947: "Beacon 3/4",
        948: "Yellow Light 1/4", 949: "Yellow Light 1/2", 950: "Yellow Light 3/4",
        951: "Orange Light 1/4", 952: "Orange Light 1/2", 953: "Orange Light 3/4",
        954: "Red Light 1/4", 955: "Red Light 1/2", 956: "Red Light 3/4",
        957: "Pink Light 1/4", 958: "Pink Light 1/2", 959: "Pink Light 3/4",
        960: "Purple Light 1/4", 961: "Purple Light 1/2", 962: "Purple Light 3/4",
        963: "Blue Light 1/4", 964: "Blue Light 1/2", 965: "Blue Light 3/4",
        966: "Teal Light 1/4", 967: "Teal Light 1/2", 968: "Teal Light 3/4",
        969: "Green Light 1/4", 970: "Green Light 1/2", 971: "Green Light 3/4",
        972: "Black Light 1/4", 973: "Black Light 1/2", 974: "Black Light 3/4",
        }

    _block_ids["crystals"] = {
        # Crystals
        452: "Rammet Crystal", 550: "Rammet Crystal Wedge",
        453: "Nocx Crystal", 548: "Nocx Crystal Wedge",
        454: "Parseen Crystal", 549: "Parseen Crystal Wedge",
        455: "Hattel Crystal", 553: "Hattel Crystal Wedge",
        456: "Mattise Crystal", 555: "Mattise Crystal Wedge",
        457: "Sintyr Crystal", 554: "Sintyr Crystal Wedge",
        458: "Bastyn Crystal", 552: "Bastyn Crystal Wedge",
        459: "Varat Crystal", 551: "Varat Crystal Wedge",
        }

    _block_ids["ingots"] = {
        # Ingots
        468: "Sertise Ingot", 558: "Sertise Ingot Wedge",
        469: "Macet Ingot", 556: "Macet Ingot Wedge",
        470: "Sapsun Ingot", 557: "Sapsun Ingot Wedge",
        471: "Threns Ingot", 561: "Threns Ingot Wedge",
        472: "Zercaner Ingot", 563: "Zercaner Ingot Wedge",
        473: "Jisper Ingot", 562: "Jisper Ingot Wedge",
        474: "Fertikeen Ingot", 560: "Fertikeen Ingot Wedge",
        475: "Hylat Ingot", 559: "Hylat Ingot Wedge",
        }

    _block_ids["motherboards"] = {
        # Motherboards
        223: "Fertikeen Motherboard", 576: "Fertikeen Motherboard Wedge",
        226: "Zercaner Motherboard", 579: "Zercaner Motherboard Wedge",
        229: "Hylat Motherboard", 575: "Hylat Motherboard Wedge",
        232: "Sapsun Motherboard", 573: "Sapsun Motherboard Wedge",
        235: "Threns Motherboard", 577: "Threns Motherboard Wedge",
        247: "Jisper Motherboard", 578: "Jisper Motherboard Wedge",
        250: "Sertise Motherboard", 574: "Sertise Motherboard Wedge",
        254: "Macet Motherboard", 572: "Macet Motherboard Wedge",
        }

    _block_ids["circuits"] = {
        # Circuits
        224: "Bastyn Circuit", 568: "Bastyn Circuit Wedge", 225: "Bastyn Charged Circuit", 584: "Bastyn Charged Circuit Wedge",
        227: "Mattise Circuit", 571: "Mattise Circuit Wedge", 228: "Mattise Charged Circuit", 587: "Mattise Charged Circuit Wedge",
        230: "Varat Circuit", 567: "Varat Circuit Wedge", 231: "Varat Charged Circuit", 583: "Varat Charged Circuit Wedge",
        233: "Parseen Circuit", 565: "Parseen Circuit Wedge", 234: "Parseen Charged Circuit", 581: "Parseen Charged Circuit Wedge",
        236: "Hattel Circuit", 569: "Hattel Circuit Wedge", 237: "Hattel Charged Circuit", 585: "Hattel Charged Circuit Wedge",
        248: "Sintyr Circuit", 570: "Sintyr Circuit Wedge", 249: "Sintyr Charged Circuit", 586: "Sintyr Charged Circuit Wedge",
        251: "Rammet Circuit", 566: "Rammet Circuit Wedge", 252: "Rammet Charged Circuit", 582: "Rammet Charged Circuit Wedge",
        272: "Nocx Circuit", 564: "Nocx Circuit Wedge", 273: "Nocx Charged Circuit", 580: "Nocx Charged Circuit Wedge",
        253: "Beacon Charged Circuit",
        }

    _block_ids["medical"] = {
        # Medical
        445: "Medical Supplies",
        446: "Medical Cabinet",
        }

    _block_ids["nature"] = {
        # Nature
        64: "Ice",
        73: "Rock",
        74: "Sand",
        80: "Lava",
        82: "Grass",
        83: "Grassy Rock",
        84: "Wood",
        85: "Foliage",
        86: "Water",
        87: "Soil",
        89: "Cactus",
        90: "Purple Top Stuff",
        91: "Purple Rock Stuff",
        92: "Purple Vine Stuff",
        138: "Red Planet Terrain",
        139: "Blue Rock",
        140: "Red Dirt",
        141: "Rock Red Planet Terrain",
        274: "Snowy Rock Surface",
        275: "Frozen Rock",
        276: "Frozen Wood",
        277: "Frozen Leaves",
        286: "Ice Crystal",
        287: "Red Wood",
        288: "Red Wood Leaves",
        93: "Blue Flowers",
        95: "Small Cactus",
        96: "Coral",
        97: "Fan Flower",
        98: "Long Grass",
        99: "Desert Flowers",
        100: "Fungal Growth",
        101: "Glow Trap",
        102: "Small Berry Bush",
        103: "Arched Cactus",
        104: "Mushroom",
        105: "Purple Weeds",
        106: "Yellow Flowers",
        107: "Stone Fragment",
        108: "Funal Trap",
        109: "Yhole",
        278: "Ice Fan Flower",
        279: "Ice Crag",
        280: "Ice Coral",
        281: "Snowbuds",
        }

    _block_ids["plants"] = {
        # Subset of Nature
        93: "Blue Flowers",
        95: "Small Cactus",
        96: "Coral",
        97: "Fan Flower",
        98: "Long Grass",
        99: "Desert Flowers",
        100: "Fungal Growth",
        101: "Glow Trap",
        102: "Small Berry Bush",
        103: "Arched Cactus",
        105: "Purple Weeds",
        106: "Yellow Flowers",
        107: "Stone Fragment",
        108: "Funal Trap",
        109: "Yhole",
        278: "Ice Fan Flower",
        279: "Ice Crag",
        280: "Ice Coral",
        281: "Snowbuds",
        104: "Mushroom",
        1000: "Pipe Tee",
        1001: "Pipe Elbow",
        }

    _block_ids["minerals"] = {
        # Minerals
        143: "Larimar",
        151: "Chabaz",
        155: "Lukrah",
        159: "Dolom",
        163: "Sugil",
        171: "Cinnabar",
        179: "Varis",
        203: "Tekt",
        }

    _block_ids["outdated"] = {
        1002: "Extended Texture Test",
        # Out Of Use
        65: "Death Star Core",
        210: "Burnt Black Dirt",
        72: "Black Dirt",
        199: "Black Lava",
        200: "Black Water",
        201: "Black Posion",
        208: "Burnt Blue Dirt",
        128: "Blue Dirt",
        191: "Blue Lava",
        192: "Blue Water",
        193: "Blue Poison",
        129: "Burnt Orange Dirt",
        130: "Orange Dirt",
        147: "Orange Lava",
        148: "Orange Water",
        149: "Orange Poison",
        134: "Burnt White Dirt",
        132: "White Dirt",
        167: "White Lava",
        168: "White Water",
        169: "White Poison",
        136: "Burnt Purple Dirt",
        133: "Purple Dirt",
        175: "Purple Lava",
        176: "Purple Water",
        177: "Purple Poison",
        209: "Burnt Red Dirt",
        135: "Red Dirt",
        195: "Red Lava",
        196: "Red Water",
        197: "Red Poison",
        207: "Burnt Green Dirt",
        137: "Green Dirt",
        187: "Green Lava",
        188: "Green Water",
        189: "Green Poison",
        206: "Burnt Yellow Dirt",
        183: "Yellow Lava",
        184: "Yellow Water",
        185: "Yellow Poison",
        112: "PlexLander",
        114: "Recycler",
        131: "Placeholder",
        214: "Capsule Refinery Enhancer",
        216: "Micro Assembler Enhancer",
        218: "PowerBlockFactoryEnhancer",
        222: "PARTICLE PRESS",
        255: "SCHEMADYNE 10000",
        256: "SCHEMADYNE 20000",
        257: "SCHEMADYNE 30000",
        258: "SCHEMADYNE ADVANCED",
        260: "SCHEMADYNE 2000",
        261: "SCHEMADYNE 3000",
        262: "MINERAL SEPERATOR",
        292: "Faction Hub",
    }

    _hp_by_hull_type = {
        0: 75,
        1: 100,
        2: 250,
        3: 250,
        4: 100,
    }

    _block_shapes = {
        "": 0,
        "1/4": 1,
        "1/2": 2,
        "3/4": 3,
        "Wedge": 4,
        "Corner": 5,
        "Tetra": 6,
        "Hepta": 7,
    }

    @staticmethod
    def get_hp_by_hull_type(hull_type):
        return BlockConfigHardcoded._hp_by_hull_type[hull_type]

    @staticmethod
    def get_hull_details(block_id):
        # "White Standard Armor Corner"
        hull_name = BlockConfigHardcoded.get_block_name_by_id(block_id)
        if "Hull" in hull_name:
            hull_type = 0
            color, shape = hull_name.split('Hull', 1)
        elif "Standard Armor" in hull_name:
            hull_type = 1
            color, shape = hull_name.split('Standard Armor')
        elif "Advanced Armor" in hull_name:
            hull_type = 2
            color, shape = hull_name.split('Advanced Armor')
        elif "Crystal Armor" in hull_name:
            hull_type = 3
            color, shape = hull_name.split('Crystal Armor')
        elif "Hazard Armor" in hull_name:
            hull_type = 4
            color, shape = hull_name.split('Hazard Armor')
        else:
            raise Exception("Unknown Hull: '{}'".format(hull_name))
        shape = shape.strip()
        assert shape in BlockConfigHardcoded._block_shapes, "Unknown Shape: '{}'".format(shape)
        return hull_type, color.strip(), BlockConfigHardcoded._block_shapes[shape]

    _glass_ids = {63, 329, 330, 368, 367, 815, 816, 817}

    @staticmethod
    def is_rail(block_id):
        """
        @type block_id: int
        @rtype: bool
        """
        if block_id == 663:
            # exclude rail docker
            return False
        return block_id in BlockConfigHardcoded._block_ids["rails"]

    @staticmethod
    def is_station(block_id):
        """
        @type block_id: int
        @rtype: bool
        """
        if block_id == 663:
            # exclude rail docker
            return False
        return block_id in BlockConfigHardcoded._block_ids["station"]

    @staticmethod
    def is_hull(block_id):
        """
        @type block_id: int
        @rtype: bool
        """
        if block_id in BlockConfigHardcoded._glass_ids:
            return False
        return block_id in BlockConfigHardcoded._block_ids["hull"]

    _hulls_dict = None

    @staticmethod
    def _is_slab(block_id):
        """
        Return True if it is a slap
        Slab have block style 0

        @param block_id:
        @type block_id: int

        @return:
        @rtype: bool
        """
        slab_shapes = ["1/4", "1/2", "3/4"]
        block_name = BlockConfigHardcoded.get_block_name_by_id(block_id)
        for shape in slab_shapes:
            if shape in block_name:
                return True
        return False

    @staticmethod
    def _is_block_style_6(block_id):
        """
        # 6: rails/White Light Bar/Pipe/Decorative Console/Shipyard Module/Core Anchor/Mushroom/

        @param block_id:
        @type block_id: int

        @return:
        @rtype: bool
        """
        if block_id in BlockConfigHardcoded._block_ids["rails"]:
            return True
        type_6_set = {
            977,   # White Light Bar
            976,   # Pipe
            1000,  # Pipe Tee
            1001,  # Pipe Elbow
            1006,  # Pipe Cross
            975,   # Decorative Console (Blue)
            678,   # Shipyard Module
            679,   # Shipyard Core Anchor
            104,   # Mushroom
            1003,  # Grate
            1004,  # Grate Corner
            1005,  # Grate Wedge
            1007,  # White Light Corner
        }
        if block_id in type_6_set:
            return True
        return False

    @staticmethod
    def _is_block_style_3(block_id):
        """
        # 3: Rod/Paint/Capsules/Hardener/Plants/Shards

        @param block_id:
        @type block_id: int

        @return:
        @rtype: bool
        """
        style_3_categories = ["ores", "shards", "crafting"]
        for category in style_3_categories:
            if block_id in BlockConfigHardcoded._block_ids[category]:
                if block_id in {440, 220}:
                    return False
                return True
        if block_id in BlockConfigHardcoded._block_ids["plants"] and block_id != 104:  # and not Mushroom
            return True

        if block_id in BlockConfigHardcoded._block_ids["lighting"]:
            block_name = BlockConfigHardcoded.get_block_name_by_id(block_id).lower()
            if "Rod".lower() in block_name:
                return True
        return False

    @staticmethod
    def _is_block_style_0(block_id):
        """
        # 0: slabs
        #    activatable: doors/weapons/station/logic/medical/permissions/systems/effects/tools/lighting*:
        #        lights blocks and slabs but not light rods or 'White Light Bar'
        #    nature blocks, except plants
        #    standard armor/hull

        @param block_id:
        @type block_id: int

        @return:
        @rtype: bool
        """
        # if block_id in BlockConfigHardcoded._block_ids["effects"]:
        #     return True
        # if block_id in BlockConfigHardcoded._block_ids["systems"]:
        #     return True
        # if block_id in BlockConfigHardcoded._block_ids["tools"]:
        #     return True
        # if block_id in BlockConfigHardcoded._block_ids["medical"]:
        #     return True

        style_0_categories = ["hull", "circuits", "motherboards", "ingots", "crystals", "decorative",
                              "minerals", "weapons", "effects", "systems", "tools", "medical", "logic",
                              "doors", "lighting", "permissions", "weapons", "station", "docking"]
        if BlockConfigHardcoded._is_slab(block_id):
            return True
        if block_id in BlockConfigHardcoded._block_ids["nature"] and block_id not in BlockConfigHardcoded._block_ids["plants"]:
            return True

        if block_id == 976:  # Pipe
            return False
        if block_id == 975:  # Decorative Console (Blue)
            return False
        if block_id in {440, 220}:
            return True

        for category in style_0_categories:
            if block_id in BlockConfigHardcoded._block_ids[category]:
                shapes = ["wedge", "corner", "tetra", "hepta"]
                block_name = BlockConfigHardcoded.get_block_name_by_id(block_id).lower()
                for shape in shapes:
                    if shape in block_name:
                        return False
                return True
        return False

    @staticmethod
    def get_block_style(block_id):
        """
        Return style of block

        # 0: slabs/doors/weapons/station/logic/lighting/medical/permissions/systems/effects/tools:
        # 1: Wedge
        # 2: Corner
        # 3: Rod/Paint/Capsules/Hardener/Plants/Shards
        # 4: Tetra
        # 5: Hepta
        # 6: Rail/Pickup/White Light Bar/Pipe/Decorative Console/Shipyard Module/Core Anchor/Mushroom/

        @param block_id:
        @type block_id: int

        @return: style
        @rtype: int
        """
        assert BlockConfigHardcoded.is_known_id(block_id), "Unknown block id: {}".format(block_id)
        if BlockConfigHardcoded.is_deprecated(block_id):
            return 0
        if BlockConfigHardcoded._is_block_style_6(block_id):
            return 6
        block_name = BlockConfigHardcoded.get_block_name_by_id(block_id).lower()
        if "wedge" in block_name:
            return 1
        if "corner" in block_name:
            return 2
        if "tetra" in block_name:
            return 4
        if "hepta" in block_name:
            return 5
        if BlockConfigHardcoded._is_block_style_3(block_id):
            return 3
        if BlockConfigHardcoded._is_block_style_0(block_id):
            return 0
        raise Exception("Unknown block style for id: {}".format(block_id))

    @staticmethod
    def are_compatible_blocks(block_id_1, block_id_2):
        """
        Return True if two blocks can be replace each other without orientation issues

        @param block_id_1:
        @type block_id_1: int
        @param block_id_2:
        @type block_id_2: int

        @return:
        @rtype: bool
        """
        if BlockConfigHardcoded.get_block_style(block_id_1) == BlockConfigHardcoded.get_block_style(block_id_2):
                return True
        return False

    @staticmethod
    def is_known_id(block_id):
        """
        Return block name of a block id

        @param block_id:
        @type block_id: int

        @return: block name
        @rtype: str
        """
        for category_name, category_ids in BlockConfigHardcoded._block_ids.items():
            if block_id in category_ids:
                return True
        return False

    @staticmethod
    def get_block_name_by_id(block_id):
        """
        Return block name of a block id

        @param block_id:
        @type block_id: int

        @return: block name
        @rtype: str
        """
        for category_name, category_ids in BlockConfigHardcoded._block_ids.items():
            if block_id in category_ids:
                return category_ids[block_id]
        return "unknown ({})".format(block_id)

    @staticmethod
    def items():
        """
        Iterate over all block ids

        @return: Tuple[int, str]
        """
        for category_name, category_ids in BlockConfigHardcoded._block_ids.items():
            for block_id, name in category_ids.items():
                yield block_id, name

    @staticmethod
    def is_deprecated(block_id):
        """
        Return True if block id is no longer up to date

        @type block_id: int
        @rtype: bool
        """
        return block_id in BlockConfigHardcoded._block_ids["outdated"]

    @staticmethod
    def is_valid_block_id(block_id, entity_type=0):
        """
        Test if an id is outdated or not valid for a specific entity type

        @param block_id:
        @type block_id: int
        @param entity_type:
        @type entity_type: int

        @return:
        @rtype: bool
        """
        assert entity_type in BlueprintEntity.entity_types
        if BlockConfigHardcoded.is_deprecated(block_id):
            return False
        if entity_type == SHIP and block_id in BlockConfigHardcoded._block_ids["station"]:
            return False
        if entity_type != SHIP and block_id == 1:
            return False
        return True

    activatable_ids = {
        2, 7, 8, 14, 16, 24, 30, 32, 40, 48, 55, 56, 62, 588, 589, 590, 591, 592, 94, 113, 114, 120, 121, 122,
        654, 659, 660, 661, 666, 667, 668, 670, 673, 674, 675, 677, 685, 687, 211, 213, 215, 217, 222, 255, 256,
        257, 258, 259, 260, 261, 262, 282, 283, 284, 285, 289, 291, 842, 843, 844, 845, 846, 333, 335, 847, 848,
        849, 340, 850, 854, 855, 856, 345, 857, 858, 859, 860, 861, 862, 888, 889, 405, 406, 407, 408, 409, 410,
        922, 923, 415, 417, 942, 943, 944, 945, 946, 947, 948, 949, 950, 951, 952, 953, 954, 955, 956, 957, 958,
        959, 960, 961, 962, 963, 964, 965, 966, 967, 968, 969, 970, 971, 972, 973, 974, 977, 979, 479, 1007, 496,
        497, 498, 499, 500, 501, 502, 503, 504, 505, 506}

    @staticmethod
    def is_activatable_block(block_id):
        """
        Test if an id is of am activatable block (style 0 block)

        @param block_id:
        @type block_id: int

        @return:
        @rtype: bool
        """
        assert isinstance(block_id, int)
        if block_id in BlockConfigHardcoded.activatable_ids:
            return True
        return False
