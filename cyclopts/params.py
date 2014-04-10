"""Implements a robust interface for translating scaling parameters into a full
parameter definition of a resource exchange graph in Cyclus.

:author: Matthew Gidden <matthew.gidden@gmail.com>
"""

import random as rnd
import numpy as np
import copy as cp

from execute import ExecParams

class Incrementer(object):
    """A simple helper class to increment a value"""
    def __init__(self, start = 0):
        """Parameters
        ----------
        start : int, optional
            an initial value
        """
        self._val = start - 1

    def next(self):
        """Returns an incremented value"""
        self._val += 1
        return self._val

class Param(object):
    """A base class for sampled parameters.
    """
    def __init__(self, avg, dist = None, *args, **kwargs):
        self.avg = avg
        self.dist = dist

    def sample(self):
        # if self.dist is None:
        #     return self.avg
        return self.avg

class BoolParam(object):
    """A class to sample binary events
    """
    def __init__(self, cutoff, dist = None, *args, **kwargs):
        """Parameters
        ----------
        cutoff : float
            the probability cutoff
        """
        self.cutoff = cutoff
        self.dist = dist

    def sample(self):
        """Returns True if sampled below the cutoff, False otherwise"""
        # if self.dist is None:
        #     return self.avg
        return self.cutoff >= rnd.uniform(0, 1)

class CoeffParam(object):
    """A class to sample coefficient values
    """
    def __init__(self, lb = 0, ub = 1, dist = None, *args, **kwargs):
        """Parameters
        ----------
        lb : float
            the coefficient lower bound
        ub : float
            the coefficient upper bound
        dist : a distribution from the random module
            the distribution to use, default is uniform
        """
        self.lb = lb
        self.ub = ub
        self.dist = dist if dist is not None else rnd.uniform

    def sample(self):
        """Returns a sampled coefficient"""
        return self.dist(self.lb, self.ub)

class SupConstrParam(object):
    """A base class for sampled supply constraint values.
    """
    def __init__(self, cutoff, dist = False, fracs = None, *args, **kwargs):
        """Parameters
        ----------
        cutoff : float
            the lowest supply fraction
        dist : bool
            if True, a random supply fraction greater than or equal to the 
            cutoff is provided during sampling; if False, the cutoff fraction 
            is used
        fracs : list
            a collection of fractional values of commodity demand that the 
            supply constraint value could take; default is [0.25, 0.5, 0.75, 1]
        """
        self.cutoff = cutoff
        self.dist = dist
        # possible supply fractions
        fracs = fracs if fracs is not None else [0.25, 0.5, 0.75, 1] 
        self.fracs = [frac for frac in fracs if frac >= cutoff]

    def sample(self):
        """Returns a fractional supply constraint value for a commodity"""
        if self.dist:
            return self.cutoff
        else:
            return rnd.choice(self.fracs)

class ReactorRequestSampler(object):
    """A container class for holding all sampling objects for reactor request
    scenarios.
    """
    def __init__(self, n_commods = None, 
                 n_request = None, assem_per_req = None, assem_multi_commod = None, 
                 req_multi_commods = None, exclusive = None, n_req_constr = None, 
                 n_supply = None, sup_multi_frac = None, sup_multi_commods = None, 
                 n_sup_constr = None, sup_constr_val = None, 
                 connection = None, constr_coeff = None, pref_coeff = None,
                 *args, **kwargs):
        """Parameters
        ----------
        n_commods : Param or similar, optional
            the number of commodities
        n_request : Param or similar, optional
            the number of requesters (i.e., RequestGroups)
        assem_per_req : Param or similar, optional
            the number of assemblies in a request
        assem_multi_commod : BoolParam or similar, optional
            whether an assembly request can be satisfied by multiple 
            commodities
        req_multi_commods : Param or similar, optional
            the number of commodities in a multicommodity zone
        exclusive : BoolParam or similar, optional
            the probability that a reactor assembly request is exclusive
        n_req_constr : Param or similar, optional
            the number of constraints associated with a given request group
        n_supply : Param or similar, optional
            the number of suppliers (i.e., supply ExchangeNodeGroups)
        sup_multi : BoolParam or similar, optional
            whether a supplier supplies more than one commodity
        sup_multi_commods : Param or similar, optional
            the number of commodities a multicommodity supplier supplies
        n_sup_constr : Param or similar, optional
            the number of constraints associated with a given supply group
        sup_constr_val : SupConstrParam or similar, optional
            the supply constraint rhs value (as a fraction of the total request 
            amount for a commodity)
        connection : BoolParam or similar, optional
            the probability that a possible connection between supply and 
            request nodes is added
        constr_coeff : CoeffParam or similar, optional
            constraint coefficients
        pref_coeff : CoeffParam or similar, optional
            preference coefficients
        """
        self.n_commods = n_commods \
            if n_commods is not None else Param(1)
        self.n_request = n_request \
            if n_request is not None else Param(1)
        self.assem_per_req = assem_per_req \
            if assem_per_req is not None else Param(1)
        self.assem_multi_commod = assem_multi_commod \
            if assem_multi_commod is not None else BoolParam(-1) # never true
        self.req_multi_commods = req_multi_commods \
            if req_multi_commods is not None else Param(1)
        self.exclusive = exclusive \
            if exclusive is not None else BoolParam(-1) # never true
        self.n_req_constr = n_req_constr \
            if n_req_constr is not None else Param(0)
        self.n_supply = n_supply \
            if n_supply is not None else Param(1)
        self.sup_multi = sup_multi \
            if sup_multi is not None else BoolParam(-1) # never true
        self.sup_multi_commods = sup_multi_commods \
            if sup_multi_commods is not None else Param(1)
        self.n_sup_constr = n_sup_constr \
            if n_sup_constr is not None else Param(1)
        self.sup_constr_val = sup_constr_val \
            if sup_constr_val is not None else SupConstrParam(1)
        self.connection = connection \
            if connection is not None else BoolParam(1)
        self.constr_coeff = constr_coeff \
            if constr_coeff is not None else CoeffParam(np.nextafter(0, 1), 1)
        self.pref_coeff = pref_coeff \
            if pref_coeff is not None else CoeffParam(np.nextafter(0, 1), 1)

class ReactorRequestParams(object):
    """A helper class to translate sampling parameters for a reactor request
    scenario into an instance of ExecParams used by the cyclopts.execute
    module.

    params is populated by the various generate_* functions.
    """
    def __init__(self, sampler, commod_offset = 0, req_g_offset = 0, 
                 sup_g_offset = 0, req_n_offset = 0, sup_n_offset = 0, 
                 arc_offset = 0,
                 *args, **kwargs):
        """Parameters
        ----------
        sampler : ReactorRequestSampler
            a parameter sampling container
        commod_offset : int, optional
            an offset for commodity ids
        req_g_offset : int, optional
            an offset for request group ids
        sup_g_offset : int, optional
            an offset for supply group ids
        req_n_offset : int, optional
            an offset for request node ids
        sup_n_offset : int, optional
            an offset for supply node ids
        arc_offset : int, optional
            an offset for arc ids
        """
        self.sampler = sampler
        self.commod_offset = commod_offset

        self.commods = set(range(self.commod_offset, 
                                 self.commod_offset + self.n_commods.sample()))
        self.n_request = self.n_request.sample() # number of request groups
        self.n_supply = self.n_supply.sample() # number of supply groups
        
        self.req_g_offset = req_g_offset
        self.sup_g_offset = sup_g_offset
        self.req_n_offset = req_n_offset
        self.sup_n_offset = sup_n_offset
        self.arc_offset = arc_offset

        req_g_ids = Incrementer(req_g_offset)
        self.requesters = [req_g_ids.next() for i in range(self.n_request)] # request groups
        # include request values because ids are global
        sup_g_ids = Incrementer(req_g_offset + sup_g_offset + len(requesters))
        self.suppliers = [sup_g_ids.next() for i in range(self.n_supply)] # supply groups
        self.arc_ids = Incrementer(arc_offset)

        self.params = ExecParams()
        self.reqs_to_commods = {} # requests to their commodities
        self.commods_to_reqs = {} # commodities to all requests
        self.sup_node_commods = {} # supply to their commodities
    
    def generate_request(self, commods, requesters, *args, **kwargs):
        """Returns all requests as a dictionary of requester ids to a list of
        assembly requests, where each assembly request is a list of id-commodity
        two-tuples that can satisfy such a request.

        Parameters
        ----------
        commods : set
            the commodities
        requesters : list
            the requesters        
        """
        s = self.sampler
        n_ids = self.req_n_ids = Incrementer(req_n_offset)
        requests = {}
        for g_id in requesters:
            assems = s.assem_per_req.sample()
            primary_commod = rnd.choice(commods)
            # other commodities for assemblies that can be satisfied by 
            # multiple commodities
            multi_commods = rnd.sample(cp.copy(commods).remove(primary_commod), 
                                       s.req_multi_commods.sample())

            assem_reqs = []
            # add nodes
            for i in range(assems):
                assem_commods = [primary_commod]
                if s.assem_multi_commod.sample(): 
                    # multi commod assembly request
                    assem_commods += multi_commods
                for commod in assem_commods:
                    n_id = n_ids.next()
                    assem_reqs.append((n_id, commod))
                    self.reqs_to_commods[n_id] = commod
                    self.commods_to_reqs[commod] = n_id

            requests[g_id] = assem_reqs
        return requests
                
    def generate_supply(self, commods, suppliers, *args, **kwargs):
        """Returns all supply as a dictionary of supply group id to a list of
        3-tuples of supply node id, request node id, and commodity. Each
        possible connection is tested using the connection sampling of the
        sampler.

        Parameters
        ----------
        commods : set
            the commodities
        suppliers : list
            the suppliers        
        """
        s = self.sampler
        # include request values because ids are global
        sup_ids = self.sup_n_ids = Incrementer(req_n_offset + 
                                               sup_n_offset + 
                                               len(self.req_node_commods))
        commod_assign = self._assign_supply_commods(commods, suppliers)
        # checks s.connection.sample for each possible entry
        supply = {g_id : [(n_ids.next(), req_id, commod) \
                           for req_id in self.commods_to_reqs[commod] \
                           for commod in g_commods \
                           if s.connection.sample()] \
                      for g_id, g_commods in commod_assign.items()}
        return supply
    
    def populate_structure_params(self, request, supply):
        """Given known supply and request, the ExecParams structure is
        populated.

        Parameters
        ----------
        request : as returned by generate_request
        supply : as returned by generate_supply
        """
        p = self.params
        s = self.sampler

        # collect and remove non-matched request nodes
        # tup[1] is request_id
        matched = {tup[1] for tup in v for k, v in supply.items()}
        non_matched = \
            {k for k, v in self.reqs_to_commods.items()}.difference(matched)
        to_remove = {k: [req if req[0] in non_matched for req in v] \
                         for k, v in request}
        for k, v in request:
            for req in to_remove[k]:
                v.remove(req)
        
        # populate request params
        for g_id, reqs in request:
            p.AddRequestGroup(g_id)
            # assumes 1 assembly == 1 mass unit, all constr vals equivalent
            constr_val = len(reqs)
            p.req_qty[g_id] = constr_val
            p.constr_vals[g_id] = \
                [constr_val for i in range(s.n_req_constr.sample())]
            for n_id, commod in reqs:
                p.AddRequestNode(n_id, g_id)
                # change these if all assemblies have mass != 1
                p.node_qty[n_id] = 1
                p.def_constr_coeff[n_id] = 1
                excl = s.exclusive.sample() # exclusive or not
                p.node_excl[n_id] = excl
                if excl:
                    p.excl_req_nodes[g_id].append(n_id)

        # populate supply params and arcs
        arcs = {}
        a_ids = Incrementer(self.arc_offset)
        for g_id, sups in supply
            p.AddSupplyGroup(g_id)
            for s_id, r_id, commod in sups:
                arcs[a_ids.next()] = (r_id, s_id)
    
    def populate_coeffs(self, request, supply, *args, **kwargs):
        """Generates constraint and preference coefficients.
        """
        pass

    def generate(self, *args, **kwargs):
        """Returns a configured cyclopts.execute.ExecParams after calling each
        generation member function in order.
        """
        commods = self.commods
        requesters = self.requesters
        suppliers = self.suppliers

        request = self.generate_request(commods, requesters)
        supply = self.generate_supply(commods, suppliers)

        self.populate_structure_params(reqest, supply)
        self.populate_coeffs(request, supply)

        return self.params

    def _assign_supply_commods(self, exchng_commods, suppliers):
        """Returns a mapping from supplier to a list commodities it supplies

        Parameters
        ----------
        exchng_commods : set
            the commodities
        suppliers : list
            the suppliers
        """
        if len(commods) > len(suppliers):
            raise ValueError("There must be at least as many suppliers as commodities.")

        s = self.sampler
        commods = cp.copy(exchng_commods)
        rnd.shuffle(commods) # get a random ordering
        assign = {}
        i = 0
        # give each supplier a primary commodity, guaranteeing that all
        # commodities have at least one supplier, and some number of randomly
        # sampled secondary commodities if applicable
        for sup in suppliers:
            primary = commods[i % len(commods)]
            i += 1
            n_extra = s.sup_multi_commods.sample() \
                if s.sup_multi.sample() else 0 
            secondaries = rnd.sample(cp.copy(commods).remove(primary), n_extra)
            assign[sup] = [primary] + secondaries
        return assign

class ReactorSupplyParams(object):
    """A helper class to translate sampling parameters for a reactor supply
    scenario into an instance of ExecParams used by the cyclopts.execute
    module.
    """
    def __init__(self, *args, **kwargs):
        """Parameters
        ----------
        n_commods : Param or similar, optional
            the number of commodities in the exchange
        """
        self.n_commods = n_commods
        self.n_supply = n_supply
        self.n_request = n_request
        self.assem_per_sup = assem_per_sup
        self.commod_per_sup = commod_per_sup
        self.assem_commod = assem_commod
        self.p_excl = p_excl
        self.p_connect = p_connect
        self.u_caps = u_caps
        self.prefs = prefs
        self.sup_constr_val = sup_constr_val
        self.sup_n_constr = sup_n_constr
        self.dem_constr_val = dem_constr_val
        self.dem_multi_frac = dem_multi_frac
        self.dem_n_multi = dem_n_multi
        self.dem_n_constr = dem_n_constr

    def get():
        """Returns a configured cyclopts.execute.ExecParams."""
        params = ExecParams()
        return params        
