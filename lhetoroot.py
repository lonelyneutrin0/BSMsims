import uproot
import numpy as np
import ROOT

# Input LHE file
lhe_file = "PROC_sm_0/Events/run_01/unweighted_events.lhe"

# Open LHE file
with open(lhe_file, "r", encoding="latin-1", errors="ignore") as f:
    lines = f.readlines()

# Extract momenta (px, py, pz, E)
momenta = []
for line in lines:
    parts = line.strip().split()

    # Check if the line contains valid particle data
    if len(parts) == 13 and parts[0].isdigit():  
        try:
            px, py, pz, E = map(float, parts[6:10])
            momenta.append([px, py, pz, E])
        except ValueError:
            continue  # Skip lines that can't be converted

# Convert to numpy array
momenta = np.array(momenta)

# Create a ROOT file
file = ROOT.TFile("events.root", "RECREATE")
tree = ROOT.TTree("tree", "MadGraph Events")

# Define branches
px, py, pz, E = (ROOT.std.vector('float')() for _ in range(4))
tree.Branch("px", px)
tree.Branch("py", py)
tree.Branch("pz", pz)
tree.Branch("E", E)

# Fill tree with momenta data
for p in momenta:
    px.push_back(p[0])
    py.push_back(p[1])
    pz.push_back(p[2])
    E.push_back(p[3])
    tree.Fill()

file.Write()
file.Close()

print("ROOT file 'events.root' created successfully.")
