embed
<drac2>
out = []
# Grab list of previously sheet-stats extracted from description
prvSkillBonuses = []
for descToken in get("prev_update_sheet_cvars","").split("~"):
	if descToken.count(" ") != 0:
		continue
	if descToken.count("=") != 1:
		continue
	descToken = descToken.split("=",1)[0]
	if descToken.startswith("skillbonus_") or descToken.startswith("savebonus_"):
		prvSkillBonuses.append(descToken)
# Grab list of NEW sheet-stats extracted from description
newSkillBonuses = []
for descToken in get("description","").split("~"):
	if descToken.count(" ") != 0:
		continue
	if descToken.count("=") != 1:
		continue
	if descToken.startswith("skillbonus_") or descToken.startswith("savebonus_"):
		newSkillBonuses.append(descToken)
# Set them-there cvars!
for descToken in newSkillBonuses:
	newCvarName  = descToken.split("=",1)[0]
	newCvarValue = descToken.split("=",1)[1]
	character().set_cvar(newCvarName,newCvarValue)
	if prvSkillBonuses.count(newCvarName) > 0:
		prvSkillBonuses.remove(newCvarName)
# Store new list of sheet-stats extracted from new description for the next time 3update is called!
character().set_cvar("prev_update_sheet_cvars", "~".join(newSkillBonuses))
# Delete any old cvars that are not longer part of the sheet!
for staleSkill in prvSkillBonuses:
	character().delete_cvar(staleSkill)
out.append(f'-title "Updated sheet for {name}"')
out.append(f'-footer "Avrae 3.5e; Made by siliceous#5311"')
return "\n".join(out)
</drac2>