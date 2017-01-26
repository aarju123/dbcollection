"""
HDF5 storage class.
"""


import h5py


class StorageHDF5:
    """ Manage a HDF5 file """

    def __init__(self, filename, mode):
        """
        Initialize class.

        Parameters
        ----------
        filename : str
            File name + path for the target metadata file.
        mode : str
            File opem mode: r, r+, w , w+, x, a
        """
        self.fname = filename
        self.mode = mode

        # open a file (read or write mode)
        self.storage = self.open_file(filename, mode)

        # create train, val and test groups (most used groups)
        if mode in ['w', 'w+']:
            self.add_group('train')
            self.add_group('val')
            self.add_group('test')


    def open_file(self, name, mode, version='latest'):
        """
        Open a hdf5 file.
        """
        try:
            return h5py.File(name, mode, libver=version)
        except IOError:
            raise


    def close(self):
        """
        Close the file.
        """
        self.storage.close()


    def is_group(self, name):
        """
        Check if the group name exists.
        """
        if name in self.storage.keys():
            return True
        else:
            return False


    def add_group(self, name):
        """
        Create a group in the hdf5 file.
        """
        try:
            grp = self.storage.create_group(name)
        except ValueError: #group already exists
            pass
        else:
            setattr(self, name, grp)


    def delete_group(self, name):
        """
        Delete a group.
        """
        if self.is_group(name):
            del self.storage[name]


    def parse_str(self, group, field_name):
        """
        Concatenate two strings.
        """
        if group == '/':
            return field_name
        else:
            return group + '/' + field_name


    def is_data(self, group, field_name):
        """
        Check if the field_name exists.
        """
        # check if the group exists
        if not self.is_group(group):
            raise Exception('Group name not found: ' + group)

        if field_name in self.storage[group].keys():
            return True
        else:
            return False


    def add_data(self, group, field_name, data):
        """
        Add data to a hdf5 file.
        """
        # parse string
        field_str = self.parse_str(group, field_name)

        # add data to the file
        self.storage.create_dataset(field_str, data=data)


    def delete_data(self, group, field_name):
        """
        Delete a data field.
        """
        if self.is_data(group, field_name):
            # parse string
            field_str = self.parse_str(group, field_name)

            # delete data field
            del self.storage[field_str]