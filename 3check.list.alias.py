embed
<drac2>
out = []
out.append(f'-title "Skill bonuses for {name}"')
# Retreive list of all skills that are explicitly set as being trained, because they have a cvar defined with a name of the pattern "skillbonus_*"
trainedSkills = list(character().cvars.keys())
trainedSkills.sort()
output = ""
for cvarName in trainedSkills:
	if cvarName.startswith("skillbonus_"):
		skillName = cvarName.replace("skillbonus_", "").replace("_sub_", "(").replace("_"," ")
		skillName = (skillName+")") if ("(" in skillName) else skillName
		skillName = skillName.title()
		skillBonus = get(cvarName,None)
		if (output != ""):
			output = output + "\n"
		output = output + f'    {skillName}: {skillBonus}'
out.append(f'-f "Skill Bonuses|{output}"')
out.append(f'-footer "Avrae 3.5e; Made by siliceous#5311"')
return "\n".join(out)
</drac2>