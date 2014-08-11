"""This module provides I/O classes and routines for Cyclopts-related functionality.

:author: Matthew Gidden
"""
import numpy as np
import tables as t
import math
    
_filters = t.Filters(complevel=4)
        
class Table(object):
    """A thin wrapper for a PyTables Table to be used by Cyclopts.
    """

    def __init__(self, h5file, path, dt, chunksize=None):
        """Parameters
        ----------
        h5file : PyTables File
            the hdf5 file
        path : string
            the absolute path to the table
        dt : np.dtype
            the dtype for the table
        chunksize : int, optional
            the table chunksize, Cyclopts will optimize for a 32Kb L1 cache by
            default
        """
        self.h5file = h5file
        self.path = path
        self.dt = dt
        # l1 cache size / row size / 2
        # factor of 2 is ideal for reading/writing speed (per @scopatz's advice)
        self.chunksize = chunksize if chunksize is not None \
            else math.floor(32 * 1024 / float(dt.itemsize)) / 2
        self.prefix = '/' + '/'.join(self.path.split('/')[:-1])
        self.name = self.path.split('/')[-1]
        self._data = np.empty(shape=(self.chunksize), dtype=self.dt)
        self._idx = 0
        self._tbl = self.h5file.get_node(self.path) if self.path in self.h5file \
            else None

    def __del__(self):
        del self._data

    def create(self):
        """Creates a table in the h5file. This must be called before writing."""
        self.h5file.create_table(self.prefix, 
                                 self.name, 
                                 description=self.dt, 
                                 filters=_filters, 
                                 chunkshape=(self.chunksize,))
        self._tbl = self.h5file.get_node(self.path)

    # def where(self, pred):
    #     """Parameters
    #     ---------
    #     pred : string
    #         the search predicate
        
    #     Return
    #     ------
    #     rows : Pytables.Row iterable
    #         the rows matching pred
    #     """
    #     return self._tbl.where(pred)

    def instid_rows(self, uuid):
        return self._tbl.where('instid == uuid')

    def append_data(self, data):
        """Appends data to the Table. If the chunksize limit is reached, data is
        written to disc.

        Parameters
        ----------
        data : np.ndarray
            data to append to the table
        """
        ndata = len(data)
        idx = self._idx
        chunksize = self.chunksize
        # just add data, no writing
        if ndata + idx < chunksize:
            self._idx += ndata
            self._data[idx:self._idx] = data
            return

        # writing
        space = chunksize - idx
        nwrites = 1 + int(math.floor(float(ndata - space) / chunksize))
        self._data[idx:chunksize] = data[:space]
        self._idx = chunksize
        self._write()
        for i in range(nwrites - 1):
            start = i * chunksize + space
            stop = (i + 1) * chunksize + space
            self._write(data[start:stop])
        self._idx = ndata - (nwrites - 1) * chunksize - space
        if self._idx > 0:
            self._data[:self._idx] = data[-self._idx:]
            
    def flush(self):
        """Writes any remaining data to the table. This must be called before
        closing the h5file."""
        self._write()

    def _write(self, data=None):
        """Writes data up to self.idx"""
        if self._tbl is None:
            raise IOError('Table must be created before it can be written to.')
        if data is None:
            self._tbl.append(self._data[:self._idx])
            self._idx = 0
        else:
            self._tbl.append(data)
        self._tbl.flush()        

class TableManager(object):
    """A managing class that performs RAII for its tables by creating them if
    needed upon acquisition and flushing them upon deletion. Tables can be
    accessed through the manager by its tables member, which is a dictionary
    from table names to Table objects."""

    def __init__(self, h5file, tables):
        """Parameters
        ----------
        h5file : PyTables File
            the hdf5 file
        tables : list of Tables
            the list of tables to manage
        """
        self.tables = {tbl.path.split('/')[-1]: tbl for tbl in tables}
        self.h5file = h5file
        for tbl in self.tables.values():
            if tbl.path not in self.h5file:
                tbl.create()

    def __del__(self):
        self.flush_tables()
    
    def flush_tables(self):
        for tbl in self.tables.values():
            tbl.flush()
