embed
<drac2>
out = []
out.append(f'-title "Check bonuses for {name}"')
# Retreive list of all checks that are explicitly set as being trained, because they have a cvar defined with a name of the pattern "checkbonus_*"
trainedChecks = list(character().cvars.keys())
trainedChecks.sort()
output = ""
for cvarName in trainedChecks:
	if cvarName.startswith("checkbonus_"):
		checkName = cvarName.replace("checkbonus_", "").replace("_sub_", "(").replace("_"," ")
		checkName = (checkName+")") if ("(" in checkName) else checkName
		checkName = checkName.title()
		checkBonus = get(cvarName,None)
		if (output != ""):
			output = output + "\n"
		output = output + f'    {checkName}: {checkBonus}'
out.append(f'-f "Check Bonuses|{output}"')
out.append(f'-footer "Avrae 3.5e; Made by siliceous#5311"')
return "\n".join(out)
</drac2>