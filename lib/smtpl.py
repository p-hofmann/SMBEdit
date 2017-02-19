__author__ = 'Peter Hofmann'


import sys
from lib.loggingwrapper import DefaultLogging
from lib.binarystream import BinaryStream
# from lib.utils.vector import Vector
from lib.utils.blocklist import BlockList
from lib.smblueprint.smdblock.blockpool import block_pool


class StarMadeTemplate(DefaultLogging):
    """
    @type _logic: dict[(int, (int, int, int)), list[(int, (int, int, int))]]
    """

    _file_name = ".smtpl"

    # version 0, 1 indicate chunk_16 blueprint
    _valid_versions = {1, 2, 3, 4}

    def __init__(self, logfile=None, verbose=False, debug=False):
        super(StarMadeTemplate, self).__init__(label="StarMadeTemplate", logfile=logfile, verbose=verbose, debug=debug)
        self._version = 0
        self.box_min = (0., 0., 0.)
        self.box_max = (0., 0., 0.)
        self._block_list = BlockList()
        self._logic = {}
        self._displays = {}
        self._storage = {}
        return

    # #######################################
    # ###  Read
    # #######################################

    @staticmethod
    def _read_dict_of_groups(input_stream):
        """
        Read controller group data from byte stream

        @param input_stream: input stream
        @type input_stream: BinaryStream

        @return: dict of block id to set of positions
        @rtype: list[tuple]
        """
        block_id_to_positions = []
        number_of_groups = input_stream.read_int32_unassigned()
        for entry_index in range(0, number_of_groups):
            unknown = input_stream.read_int16_unassigned()
            position = input_stream.read_vector_3_int16()
            block_id_to_positions.append(position)
            # block_id_to_positions[block_id] = self._read_set_of_positions(input_stream)
        return block_id_to_positions

    @staticmethod
    def _read_list_of_controllers(input_stream):
        """
        Read controller data from byte stream

        @param input_stream: input stream
        @type input_stream: BinaryStream

        @return: set of positions
        @rtype: dict[tuple, dict[int, set[tuple[int]]]]
        """
        controller_position_to_groups = {}
        number_of_controllers = input_stream.read_int32_unassigned()
        for entry_index in range(0, number_of_controllers):
            unknown = input_stream.read_int16_unassigned()
            position = tuple(reversed(input_stream.read_vector_3_int16()))
            controller_position_to_groups[position] = StarMadeTemplate._read_dict_of_groups(input_stream)
        return controller_position_to_groups

    def _read_blocks(self, input_stream):
        """
        Read block quantities from a byte stream

        @param input_stream: input stream
        @type input_stream: BinaryStream
        """
        assert isinstance(input_stream, BinaryStream)
        num_of_blocks = input_stream.read_int32_unassigned()
        for index in range(num_of_blocks):
            position = tuple(reversed(input_stream.read_vector_3_int32()))
            if self._version == 4:
                int_24 = input_stream.read_int24(True)
                self._block_list[position] = block_pool(int_24, 3)
            elif self._version == 3:
                int_24 = input_stream.read_int24()
                self._block_list[position] = block_pool(int_24, 2)
            else:
                int_24 = input_stream.read_int24()
                self._block_list[position] = block_pool(int_24, self._version)

    def _read_header(self, input_stream):
        """
        Read header data from a byte stream

        @param input_stream: input stream
        @type input_stream: BinaryStream
        """
        assert isinstance(input_stream, BinaryStream)
        self._version = input_stream.read_byte()
        assert self._version in self._valid_versions, "Unsupported version '{}' of '{}'.".format(
            self._version, self._file_name)
        self.box_min = input_stream.read_vector_3_int32()
        self.box_max = input_stream.read_vector_3_int32()

    def _read_file(self, input_stream):
        """
        Read blueprint header data from a byte stream

        @param input_stream: input stream
        @type input_stream: BinaryStream
        """
        assert isinstance(input_stream, BinaryStream)
        self._block_list = BlockList()
        self._read_header(input_stream)
        self._read_blocks(input_stream)
        self._logic = self._read_list_of_controllers(input_stream)
        # unknown_eof_vector = input_stream.read_vector_3_int32()
        # assert sum(unknown_eof_vector) == 0, unknown_eof_vector
        if self._version < 2:
            tail_data = input_stream.read()
            assert len(tail_data) == 0, (self._version, tail_data)
            return
        if self._version == 2:
            # 0_194_98
            number_of_unknown = input_stream.read_int32()
            # probably displays?
            tail_data = input_stream.read()
            assert len(tail_data) == 0, (self._version, len(tail_data), tail_data)
            return
        # print("Version:", self._version)
        number_of_displays = input_stream.read_int32()
        self._displays = self.get_displays(number_of_displays, input_stream)

        number_of_storage = input_stream.read_int32()
        self._storage = self.get_storage(number_of_storage, input_stream)
        # print(number_of_displays, number_of_storage)

        number_of_unknown = input_stream.read_int32()
        assert number_of_unknown == 0, number_of_unknown

        tail_data = input_stream.read()
        if tail_data:
            print("Tail", len(tail_data), tail_data)
        # assert len(tail_data) == 0, (self._version, len(tail_data), tail_data)

    @staticmethod
    def get_displays(number_of_displays, input_stream):
        """
        Read blueprint header data from a byte stream

        @param input_stream: input stream
        @type input_stream: BinaryStream
        """
        displays = {}
        # Displays
        for index in range(number_of_displays):
            unknown_int16 = input_stream.read_int16()
            position = tuple(reversed(input_stream.read_vector_3_int16()))
            text = input_stream.read_string()
            displays[position] = text
        return displays

    @staticmethod
    def get_storage(number_of_storage, input_stream):
        """
        Read blueprint header data from a byte stream

        @param input_stream: input stream
        @type input_stream: BinaryStream
        """
        # Storages
        storage = {}
        for index in range(number_of_storage):
            unknown_int16 = input_stream.read_int16()
            position = input_stream.read_vector_3_int16()
            number_of_pulls = input_stream.read_int32()
            storage[position] = {}
            for _ in range(number_of_pulls):
                block_id = input_stream.read_int16_unassigned()
                pull_quantity = input_stream.read_int32()
                storage[position][block_id] = pull_quantity
        return storage

    def read(self, file_path_template):
        """
        Read header data from the header file of a blueprint

        @param file_path_template: file_path
        @type file_path_template: str
        """
        # file_path = os.path.join(file_path_template, self._file_name)
        with open(file_path_template, 'rb') as input_stream:
            self._read_file(BinaryStream(input_stream))

    def to_stream(self, output_stream=sys.stdout):
        """
        Stream header values

        @param output_stream: Output stream
        @type output_stream: fileIO
        """
        output_stream.write("####\nTemplate v{}\n####\n\n".format(self._version))
        output_stream.write("Box min: {}, Box max: {}\n".format(
            self.box_min,
            self.box_max,
            ))
        output_stream.write("Blocks: {}\n".format(len(self._block_list)))
        for position, block in self._block_list.items():
            output_stream.write("{}\t".format(position))
            block.to_stream(output_stream)

        output_stream.write("Logic: {}\n".format(len(self._logic)))
        for position, slaves in self._logic.items():
            output_stream.write("{}\t".format(position))
            for sposition in slaves:
                output_stream.write("\t{}\n".format(sposition))

        output_stream.write("Display: {}\n".format(len(self._displays)))
        for position, text in self._displays.items():
            output_stream.write("{}: {}\n".format(position, text))

        output_stream.write("Storage: {}\n".format(len(self._storage)))
        for position, pulls in self._storage.items():
            output_stream.write("\n{}:\t".format(position))
            for block_id, quantity in pulls.items():
                output_stream.write("{}: {}, ".format(block_id, quantity))
