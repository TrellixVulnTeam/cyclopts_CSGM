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

    cdef cppclass GraphParams:
        # constructors
        GraphParams() except +

        # attributes
        cpp_map[int, double] arc_pref
        cpp_map[int, int] arc_to_unode
        cpp_map[int, int] arc_to_vnode
        cpp_map[int, cpp_vector[double]] constr_vals
        cpp_map[int, double] def_constr_coeff
        cpp_map[int, cpp_vector[int]] excl_req_nodes
        cpp_map[int, cpp_vector[cpp_vector[int]]] excl_sup_nodes
        cpp_map[int, cpp_bool] node_excl
        cpp_map[int, double] node_qty
        cpp_map[int, cpp_map[int, cpp_vector[double]]] node_ucaps
        cpp_map[int, double] req_qty
        cpp_map[int, cpp_vector[int]] u_nodes_per_req
        cpp_map[int, cpp_vector[int]] v_nodes_per_sup

        # methods
        void AddRequestGroup() except +
        void AddRequestGroup(int) except +
        void AddRequestNode() except +
        void AddRequestNode(int) except +
        void AddRequestNode(int, int) except +
        void AddSupplyGroup() except +
        void AddSupplyGroup(int) except +
        void AddSupplyNode() except +
        void AddSupplyNode(int) except +
        void AddSupplyNode(int, int) except +
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



cdef extern from "execute.h" :

    cdef cppclass SolverParams:
        # constructors
        SolverParams() except +

        # attributes
        std_string type

        # methods

        pass



cdef extern from "execute.h" :

    cdef cppclass Solution:
        # constructors
        Solution() except +

        # attributes
        cpp_vector[ArcFlow] flows
        double time

        # methods

        pass



# function signatures
cdef extern from "execute.h" :

    Solution execute_exchange() except +
    Solution execute_exchange(GraphParams &) except +
    Solution execute_exchange(GraphParams &, SolverParams &) except +



# function signatures
cdef extern from "execute.h" :

    cpp_vector[ArcFlow] test() except +




{'cpppxd_footer': '', 'pyx_header': '', 'pxd_header': '', 'pxd_footer': '', 'cpppxd_header': '', 'pyx_footer': ''}