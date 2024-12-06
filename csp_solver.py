from typing import Dict, List, Set, Tuple, Any, Callable
from collections import defaultdict

class CSP:
    def __init__(self):
        self.variables: List[str] = []
        self.domains: Dict[str, List[Any]] = {}
        self.constraints: Dict[str, List[Tuple[Tuple[str, ...], Callable]]] = defaultdict(list)
        
    def add_variable(self, var: str, domain: List[Any]) -> None:
        self.variables.append(var)
        self.domains[var] = domain.copy()
        
    def add_constraint(self, variables: Tuple[str, ...], constraint_fn: Callable) -> None:
        for var in variables:
            self.constraints[var].append((variables, constraint_fn))
            
    def is_consistent(self, var: str, assignment: Dict[str, Any], value: Any) -> bool:
        for variables, constraint_fn in self.constraints[var]:
            temp_assignment = assignment.copy()
            temp_assignment[var] = value
            
            assigned_vars = [v for v in variables if v in temp_assignment]
            if len(assigned_vars) == len(variables):
                values = tuple(temp_assignment[v] for v in variables)
                if not constraint_fn(*values):
                    return False
        return True
    
    def get_unassigned_var_mrv(self, assignment: Dict[str, Any]) -> str:
        """Get unassigned variable using Minimum Remaining Values (MRV) heuristic."""
        unassigned = [var for var in self.variables if var not in assignment]
        return min(unassigned, 
                  key=lambda var: (len([value for value in self.domains[var] 
                                      if self.is_consistent(var, assignment, value)]),
                                 -len(self.constraints[var]))) 
    
    def backtracking_search(self) -> Dict[str, Any]:
        """Perform backtracking search to find solution."""
        return self._backtrack({})
    
    def _backtrack(self, assignment: Dict[str, Any]) -> Dict[str, Any]:
        """Backtracking search helper function."""
        if len(assignment) == len(self.variables):
            return assignment
            
        var = self.get_unassigned_var_mrv(assignment)
        
        domain_values = sorted(
            self.domains[var],
            key=lambda value: sum(1 for v in self.variables 
                                if v not in assignment and 
                                not self.is_consistent(v, {**assignment, var: value}, value))
        )
        
        for value in domain_values:
            if self.is_consistent(var, assignment, value):
                assignment[var] = value
                result = self._backtrack(assignment)
                if result is not None:
                    return result
                assignment.pop(var)
                
        return None 