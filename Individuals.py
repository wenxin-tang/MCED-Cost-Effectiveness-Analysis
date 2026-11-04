import math
from dataclasses import dataclass, field

@dataclass
class Individual:
   """Tracks demographic attributes, cancer state, and economic outcomes for one person in the microsimulation."""
  
    id: int
    age: float
    sex: str
    is_smoker: bool

    # Dynamic status flags (default values)
    alive: bool = True
    has_cancer: bool = False
    stage: int = 0 # 0: Healthy, 1: localised, 2: regional, 3: distant 
    detected: bool = False
    years_since_diagnosis: float = 0.0

    total_cost: float = field(default = 0.0)
    total_qaly: float = field(default = 0.0) # Quality-Adjusted Life Year, the denominator of ICER

    def get_age_group(self) -> str:
      """Maps continuous age to discrete SEER age brackets."""
        if self.age < 60:
            return "50-59"
        elif self.age < 70:
            return "60-69"
        else:
            return "70-79"

   
