#!/usr/bin/env python
# Copyright (C) 2017, Farrajota @ https://github.com/farrajota
# All rights reserved.
#
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.


"""
Cifar10 download/process functions.
"""


import os
import sys
import numpy as np

dir_path = os.path.dirname(os.path.realpath(__file__))
lib_path = os.path.abspath(os.path.join(dir_path, '..', '..', '..'))
sys.path.append(lib_path)
from dataset import utils, storage


class Cifar10:
    """ Cifar10 preprocessing/downloading functions """

    # download url
    url = 'https://www.cs.toronto.edu/~kriz/cifar-10-python.tar.gz'
    md5_checksum = 'c58f30108f718f92721af3b95e74349a'

    # extracted file names
    data_files = [
        "batches.meta",
        "data_batch_1",
        "data_batch_2",
        "data_batch_3",
        "data_batch_4",
        "data_batch_5",
        "test_batch"
    ]


    def __init__(self, data_path, cache_path, verbose=True, clean_cache=False):
        """
        Initialize class.
        """
        self.cache_manager = cache_path
        self.data_path = data_path
        self.verbose = verbose
        self.clean_cache = clean_cache


    def download(self):
        """
        Download and extract files to disk.
        """

        # download + extract data and remove temporary files
        utils.download_extract_all(self.url, self.md5_checksum, self.data_path, self.clean_cache, self.verbose)


    def get_object_list(self, data, labels):
        """
        Groups the data + labels info in a 'list' of indexes.
        """
        object_id = np.ndarray((data.shape[0], 2), dtype=int)
        for i in range(data.len):
            object_id[i][0] = i
            object_id[i][1] = labels[i][0]
        return object_id


    def load_data(self):
        """
        Load the data from the files.
        """

        # load classes name file
        class_names = utils.load_pickle(os.path.join(self.data_path, self.data_files[0]))

        # load train data files
        train_batch1 = utils.load_pickle(os.path.join(self.data_path, self.data_files[1]))
        train_batch2 = utils.load_pickle(os.path.join(self.data_path, self.data_files[2]))
        train_batch3 = utils.load_pickle(os.path.join(self.data_path, self.data_files[3]))
        train_batch4 = utils.load_pickle(os.path.join(self.data_path, self.data_files[4]))
        train_batch5 = utils.load_pickle(os.path.join(self.data_path, self.data_files[5]))

        # concatenate data
        train_data = np.concatenate((
            train_batch1['data'],
            train_batch2['data'],
            train_batch3['data'],
            train_batch4['data'],
            train_batch5['data']),
            axis=0)

        train_labels = np.concatenate((
            train_batch1['labels'],
            train_batch2['labels'],
            train_batch3['labels'],
            train_batch4['labels'],
            train_batch5['labels']),
            axis=0)

        train_data = train_data.reshape((50000, 3, 32, 32))
        train_object_list = self.get_object_list(train_data, train_labels)

        # load test data file
        test_batch = utils.load_pickle(os.path.join(self.data_path, self.data_files[6]))

        test_data = test_batch['data'].reshape(10000, 3, 32, 32)
        test_labels = test_batch['labels']
        test_object_list = self.get_object_list(test_data, test_labels)

        #return a dictionary
        return {
            "class_names": class_names,
            "train_data": train_data,
            "train_labels": train_labels,
            "train_object_id_list": train_object_list,
            "test_data": test_data,
            "test_labels": test_labels,
            "test_object_id_list": test_object_list
        }


    def metadata_process(self):
        """
        Process metadata and store it in a hdf5 file.
        """

        # load data to memory
        data = self.load_data()

        # create/open hdf5 file with subgroups for train/val/test
        fileh5 = storage.StorageHDF5(os.path.join(self.data_path, 'classification.h5'), 'w')

        # write data to the metadata file
        fileh5.add_data('train', 'data', data["class_names"])
        fileh5.add_data('train', 'class_name', data["train_data"])
        fileh5.add_data('train', 'class_id', data["train_labels"])
        fileh5.add_data('train', 'object_id', data["train_object_id_list"])

        fileh5.add_data('test', 'data', data["class_names"])
        fileh5.add_data('test', 'class_name', data["test_data"])
        fileh5.add_data('test', 'class_id', data["test_labels"])
        fileh5.add_data('test', 'object_id', data["test_object_id_list"])

        # close file
        fileh5.close()