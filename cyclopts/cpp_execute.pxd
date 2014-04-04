################################################
#                 WARNING!                     #
# This file has been auto-generated by xdress. #
# Do not modify!!!                             #
#                                              #
#                                              #
#                    Come on, guys. I mean it! #
################################################


from cyclopts cimport cpp_execute
from libcpp cimport bool as cpp_bool
from libcpp.map cimport map as cpp_map
from libcpp.string cimport string as std_string
from libcpp.vector cimport vector as cpp_vector

cdef extern from "execute.h" :

    cdef cppclass Params:
        # constructors
        Params() except +

        # attributes
        cpp_map[int, double] arc_pref
        cpp_map[int, int] arc_to_unode
        cpp_map[int, int] arc_to_vnode
        cpp_map[int, cpp_vector[double]] constr_vals
        cpp_map[int, double] def_constr_coeffs
        cpp_map[int, cpp_vector[cpp_vector[int]]] excl_req_nodes
        cpp_map[int, cpp_vector[int]] excl_sup_nodes
        cpp_map[int, cpp_bool] node_excl
        cpp_map[int, double] node_qty
        cpp_map[int, cpp_map[int, cpp_vector[double]]] node_ucaps
        cpp_map[int, double] req_qty
        cpp_map[int, cpp_vector[int]] u_nodes_per_req
        cpp_map[int, cpp_vector[int]] v_nodes_per_sup

        # methods

        pass



cdef extern from "execute.h" :

    cdef cppclass ArcFlow:
        # constructors
        ArcFlow() except +
        ArcFlow(int) except +
        ArcFlow(int, double) except +
        ArcFlow(const ArcFlow &) except +

        # attributes
        double flow
        int id

        # methods

        pass



# function signatures
cdef extern from "execute.h" :

    void execute_exchange() except +
    void execute_exchange(Params &) except +
    void execute_exchange(Params &, std_string) except +



# function signatures
cdef extern from "execute.h" :

    void test() except +




{'cpppxd_footer': '', 'pyx_header': '', 'pxd_header': '', 'pxd_footer': '', 'cpppxd_header': '', 'pyx_footer': ''}