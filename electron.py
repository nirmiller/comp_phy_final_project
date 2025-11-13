
class ClassicElectron:
    def __init__(self, x, y, spin):

        self.FermionSpin = 1/2
        
        self.x = x
        self.y = y

        self.spin = spin

        self.G_factor = 2

        # For electrons 
        self.Bohr_Magneton = 9.274*(10**-24)  # J/T

    ### overloaded methods ###

    def __str__(self):
        return f"Electron at ({self.x}, {self.y}) with spin {self.spin*self.FermionSpin}"
    def __repr__(self):
        return f"ClassicElectron(x={self.x}, y={self.y}, spin={self.spin})"
    def __add__(self, other):
        if other.__class__ == int or other.__class__ == float:
            return self.spin + other
        if other == None:
            return self.spin
        return self.spin + other.spin
    def __radd__(self, other):
        if other.__class__ == int or other.__class__ == float:
            return self.spin + other
        if other == None:
            return self.spin
        return self.spin + other.spin
    def _iadd__(self, other):
        if other == None:
            return self
        if other.__class__ == int or other.__class__ == float:
            self.spin += other
            return self
        self.spin += other.spin
        return self
    def __riadd__(self, other):
        if other == None:
            return self
        if other.__class__ == int or other.__class__ == float:
            self.spin += other
            return self
        self.spin += other.spin
        return self

    ### class methods ###

    def getSpin(self):
        return self.spin*self.FermionSpin
    
    def changeSpin(self, newSpin):
        self.spin = newSpin

    def calculateEnergy(self, effectiveMagneticField):
        return self.spin*self.FermionSpin*self.G_factor*self.Bohr_Magneton*effectiveMagneticField
        
    def changeInEnergy(self, effectiveMagneticField):
        mu_eff = self.FermionSpin * self.G_factor * self.Bohr_Magneton
        deltaE = 2 * self.spin * mu_eff * effectiveMagneticField
        return deltaE