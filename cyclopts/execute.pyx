################################################
#                 WARNING!                     #
# This file has been auto-generated by xdress. #
# Do not modify!!!                             #
#                                              #
#                                              #
#                    Come on, guys. I mean it! #
################################################
"""
"""
cimport cpp_execute
from libc.stdlib cimport free



def run_rxtr_req(n_supply=1, n_demand=1, dem_node_avg=1, n_commods=1, dem_commod_avg=1, avg_commod_sup=1, excl_prob=0.0, connect_prob=1.0, avg_sup_caps=1, avg_dem_caps=1):
    """run_rxtr_req(n_supply=1, n_demand=1, dem_node_avg=1, n_commods=1, dem_commod_avg=1, avg_commod_sup=1, excl_prob=0.0, connect_prob=1.0, avg_sup_caps=1, avg_dem_caps=1)
    no docstring for run_rxtr_req, please file a bug report!"""
    cpp_execute.run_rxtr_req(<int> n_supply, <int> n_demand, <int> dem_node_avg, <int> n_commods, <int> dem_commod_avg, <int> avg_commod_sup, <double> excl_prob, <double> connect_prob, <int> avg_sup_caps, <int> avg_dem_caps)



def test():
    """test()
    no docstring for test, please file a bug report!"""
    cpp_execute.test()





cdef class RequestRC:
    """no docstring for {'tarbase': 'execute', 'tarname': 'RequestRC', 'language': 'c++', 'srcname': 'RequestRC', 'sidecars': (), 'incfiles': ('execute.h',), 'srcfiles': ('cpp/execute.cc', 'cpp/execute.h')}, please file a bug report!"""



    # constuctors
    def __cinit__(self, *args, **kwargs):
        self._inst = NULL
        self._free_inst = True

        # cached property defaults


    def __init__(self, ):
        """RequestRC(self, )
        """
        self._inst = new cpp_execute.RequestRC()
    
    
    def __dealloc__(self):
        if self._free_inst:
            free(self._inst)

    # attributes

    # methods
    def i(self, ):
        """i(self, )
        no docstring for i, please file a bug report!"""
        cdef int rtnval
        rtnval = (<cpp_execute.RequestRC *> self._inst).i()
        return int(rtnval)
    
    
    

    pass





cdef class SupplyRC:
    """no docstring for {'tarbase': 'execute', 'tarname': 'SupplyRC', 'language': 'c++', 'srcname': 'SupplyRC', 'sidecars': (), 'incfiles': ('execute.h',), 'srcfiles': ('cpp/execute.cc', 'cpp/execute.h')}, please file a bug report!"""



    # constuctors
    def __cinit__(self, *args, **kwargs):
        self._inst = NULL
        self._free_inst = True

        # cached property defaults


    def __init__(self, ):
        """SupplyRC(self, )
        """
        self._inst = new cpp_execute.SupplyRC()
    
    
    def __dealloc__(self):
        if self._free_inst:
            free(self._inst)

    # attributes

    # methods
    def i(self, ):
        """i(self, )
        no docstring for i, please file a bug report!"""
        cdef int rtnval
        rtnval = (<cpp_execute.SupplyRC *> self._inst).i()
        return int(rtnval)
    
    
    

    pass






{'cpppxd_footer': '', 'pyx_header': '', 'pxd_header': '', 'pxd_footer': '', 'cpppxd_header': '', 'pyx_footer': ''}
