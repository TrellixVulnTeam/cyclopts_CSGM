################################################
#                 WARNING!                     #
# This file has been auto-generated by xdress. #
# Do not modify!!!                             #
#                                              #
#                                              #
#                    Come on, guys. I mean it! #
################################################


from libcpp.string cimport string as std_string

cdef extern from "problem.h" namespace "cyclopts":

    cdef cppclass ProbSolution:
        # constructors
        ProbSolution() except +
        ProbSolution(double) except +
        ProbSolution(double, double) except +
        ProbSolution(double, double, std_string) except +

        # attributes
        double objective
        double time
        std_string type

        # methods

        pass



cdef extern from "problem.h" namespace "cyclopts":

    cdef cppclass Solver:
        # constructors
        Solver() except +
        Solver(std_string) except +

        # attributes
        std_string type

        # methods

        pass




{'cpppxd_footer': '', 'pyx_header': '', 'pxd_header': '', 'pxd_footer': '', 'cpppxd_header': '', 'pyx_footer': ''}