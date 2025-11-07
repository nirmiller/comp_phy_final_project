
class ClassicElectron:
    def __init__(self, y, x, spin):

        self.FermionSpin = 1/2
        self.x = x
        self.y = y

        self.spin = spin

        self.G_factor = 2

        # For electrons 
        self.Bohr_Magneton = 9.274*(10**-24) 


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