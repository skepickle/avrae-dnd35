embed
<drac2>
out = []
out.append(f'-title "Saving throw bonuses for {name}"')
# Retreive list of all saving throws that are explicitly set as being trained, because they have a cvar defined with a name of the pattern "savebonus_*"
allSavingThrows = list(character().cvars.keys())
allSavingThrows.sort()
output = ""
for cvarName in allSavingThrows:
	if cvarName.startswith("savebonus_"):
		saveName = cvarName.replace("savebonus_", "").replace("_"," ")
		saveName = saveName.title()
		saveBonus = get(cvarName,None)
		if (output != ""):
			output = output + "\n"
		output = output + f'    {saveName}: {saveBonus}'
out.append(f'-f "Saving Throw Bonuses|{output}"')
out.append(f'-footer "Avrae 3.5e; Made by siliceous#5311"')
return "\n".join(out)
</drac2>