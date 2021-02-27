embed
<drac2>
out = []
# Grab list of previously sheet-stats extracted from description
prvCheckBonuses = []
for descToken in get("prev_update_sheet_cvars","").split("~"):
	if descToken.count(" ") != 0:
		continue
	if descToken.count("=") != 1:
		continue
	descToken = descToken.split("=",1)[0]
	prvCheckBonuses.append(descToken)
# Grab list of NEW sheet-stats extracted from description
newCheckBonuses = []
for descToken in get("description","").split("~"):
	if descToken.count(" ") != 0:
		continue
	if descToken.count("=") != 1:
		continue
	if descToken.startswith("checkbonus_") or descToken.startswith("savebonus_"):
		newCheckBonuses.append(descToken)
# Set them-there cvars!
for descToken in newCheckBonuses:
	newCvarName  = descToken.split("=",1)[0]
	newCvarValue = descToken.split("=",1)[1]
	character().set_cvar(newCvarName,newCvarValue)
	if prvCheckBonuses.count(newCvarName) > 0:
		prvCheckBonuses.remove(newCvarName)
# Store new list of sheet-stats extracted from new description for the next time 3update is called!
character().set_cvar("prev_update_sheet_cvars", "~".join(newCheckBonuses))
# Delete any old cvars that are not longer part of the sheet!
for staleCheck in prvCheckBonuses:
	character().delete_cvar(staleCheck)
out.append(f'-title "Updated sheet for {name}"')
out.append(f'-footer "Avrae 3.5e; Made by siliceous#5311"')
return "\n".join(out)
</drac2>