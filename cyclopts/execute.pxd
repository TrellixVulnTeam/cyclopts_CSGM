################################################
#                 WARNING!                     #
# This file has been auto-generated by xdress. #
# Do not modify!!!                             #
#                                              #
#                                              #
#                    Come on, guys. I mean it! #
################################################


cimport dtypes
cimport numpy as np
cimport stlcontainers
from cyclopts cimport cpp_execute
from libcpp cimport bool as cpp_bool
from libcpp.map cimport map as cpp_map
from libcpp.vector cimport vector as cpp_vector



cdef class ArcFlow:
    cdef void * _inst
    cdef public bint _free_inst
    pass





cdef class GraphParams:
    cdef void * _inst
    cdef public bint _free_inst
    cdef public stlcontainers._MapIntDouble _arc_pref
    cdef public stlcontainers._MapIntInt _arc_to_unode
    cdef public stlcontainers._MapIntInt _arc_to_vnode
    cdef public stlcontainers._MapIntVectorDouble _constr_vals
    cdef public stlcontainers._MapIntDouble _def_constr_coeff
    cdef public stlcontainers._MapIntVectorInt _excl_req_nodes
    cdef public stlcontainers._MapIntVectorVectorInt _excl_sup_nodes
    cdef public stlcontainers._MapIntBool _node_excl
    cdef public stlcontainers._MapIntDouble _node_qty
    cdef public stlcontainers._MapIntMapIntVectorDouble _node_ucaps
    cdef public stlcontainers._MapIntDouble _req_qty
    cdef public stlcontainers._MapIntVectorInt _u_nodes_per_req
    cdef public stlcontainers._MapIntVectorInt _v_nodes_per_sup
    pass





cdef class SolverParams:
    cdef void * _inst
    cdef public bint _free_inst
    pass





cdef class Solution:
    cdef void * _inst
    cdef public bint _free_inst
    cdef public np.ndarray _flows
    pass




{'cpppxd_footer': '', 'pyx_header': '', 'pxd_header': '', 'pxd_footer': '', 'cpppxd_header': '', 'pyx_footer': ''}